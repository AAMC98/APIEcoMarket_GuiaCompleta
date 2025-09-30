"""
EcoMarket Sucursal API
Esta API implementa el principio de AUTONOMÍA: puede operar 
independientemente del servidor central.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="EcoMarket Sucursal API",
    description="API de sucursal autónoma",
    version="1.0.0"
)

# Permitir CORS para el dashboard central
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== CONFIGURACIÓN =====
BRANCH_ID = "sucursal-001"
CENTRAL_API_URL = "http://localhost:8000"

# ===== MODELOS =====

class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int

class SaleRequest(BaseModel):
    product_id: int
    quantity: int
    customer_info: Optional[str] = None

class SaleResponse(BaseModel):
    sale_id: str
    product_name: str
    quantity_sold: int
    total_amount: float
    timestamp: datetime
    status: str

# ===== INVENTARIO LOCAL (AUTONOMÍA) =====
# CONCEPTO CLAVE: Cada sucursal mantiene su propia "verdad local"
local_inventory: Dict[int, Product] = {
    1: Product(id=1, name="Manzanas Orgánicas", price=2.50, stock=25),
    2: Product(id=2, name="Pan Integral", price=1.80, stock=15),
    3: Product(id=3, name="Leche Deslactosada", price=3.20, stock=8),
    4: Product(id=4, name="Café Premium", price=8.90, stock=6),
    5: Product(id=5, name="Quinoa", price=12.50, stock=3)
}

sales_history: List[SaleResponse] = []

# ===== ENDPOINTS =====

@app.get("/", tags=["General"])
async def root():
    return {
        "service": f"EcoMarket Sucursal",
        "branch_id": BRANCH_ID,
        "status": "operational - AUTONOMOUS",
        "local_inventory_items": len(local_inventory),
        "total_sales": len(sales_history)
    }

@app.get("/inventory", response_model=List[Product], tags=["Inventario"])
async def get_local_inventory():
    """
    CONCEPTO CLAVE: Consulta local instantánea
    
    Esta consulta no va al servidor central. Es inmediata
    porque consulta el inventario local de la sucursal.
    """
    logger.info("🏪 Consultando inventario LOCAL (operación autónoma)")
    return list(local_inventory.values())

@app.get("/inventario", tags=["Inventario"])
async def get_inventario_sucursal():
    """Obtiene inventario de sucursal (endpoint en español)"""
    logger.info("🏪 Consultando inventario de sucursal en español")
    products = []
    for product in local_inventory.values():
        products.append({
            "id": product.id,
            "nombre": product.name,  # Convertir name a nombre
            "precio": product.price,  # Convertir price a precio
            "stock": product.stock
        })
    return products

# Endpoint para consulta remota del inventario de sucursal
@app.get("/remote-inventory", response_class=JSONResponse, tags=["Remoto"])
async def get_remote_inventory():
    """Permite al servidor central consultar el inventario de la sucursal"""
    return [product.model_dump() for product in local_inventory.values()]

# Endpoint para modificar inventario de sucursal desde central
@app.put("/remote-inventory/{product_id}", response_class=JSONResponse, tags=["Remoto"])
async def update_remote_inventory(product_id: int, updated: Product):
    """Permite al servidor central actualizar el inventario de la sucursal"""
    if product_id not in local_inventory:
        raise HTTPException(status_code=404, detail="Producto no encontrado en sucursal")
    local_inventory[product_id] = updated
    logger.info(f"📦 Inventario actualizado remotamente: {updated.name} (ID: {product_id})")
    return updated.model_dump()

# Endpoint para actualizar solo el stock de un producto
@app.put("/products/{product_id}", tags=["Inventario"])
async def update_product_stock(product_id: int, stock_data: dict):
    """Actualiza solo el stock de un producto específico"""
    if product_id not in local_inventory:
        raise HTTPException(status_code=404, detail="Producto no encontrado en sucursal")
    
    # Si solo se envía stock, actualizar solo el stock
    if "stock" in stock_data:
        local_inventory[product_id].stock = stock_data["stock"]
        logger.info(f"📦 Stock actualizado para producto {product_id}: {stock_data['stock']}")
        return {
            "status": "success",
            "message": f"Stock actualizado para producto {product_id}",
            "new_stock": stock_data["stock"]
        }
    
    return {"status": "error", "message": "Datos de stock requeridos"}

@app.get("/sales", response_class=JSONResponse, tags=["Ventas"])
async def get_sales():
    """Obtiene el historial de ventas de la sucursal"""
    return [sale.model_dump() for sale in sales_history]

@app.post("/sales", response_model=SaleResponse, tags=["Ventas"])
async def process_sale(sale_request: SaleRequest, background_tasks: BackgroundTasks):
    """
    CONCEPTO CLAVE: Procesamiento autónomo de ventas
    
    Este es el corazón de la autonomía:
    1. Verifica stock LOCAL inmediatamente
    2. Procesa la venta SIN esperar al servidor central  
    3. Envía notificación al central de forma ASÍNCRONA
    """
    
    # PASO 1: Verificación inmediata contra inventario local
    if sale_request.product_id not in local_inventory:
        raise HTTPException(status_code=404, detail="Producto no disponible")
    
    product = local_inventory[sale_request.product_id]
    
    if product.stock < sale_request.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Stock insuficiente. Disponible: {product.stock}"
        )
    
    # PASO 2: Procesar la venta INMEDIATAMENTE
    product.stock -= sale_request.quantity
    sale_timestamp = datetime.now()
    total_amount = product.price * sale_request.quantity
    
    sale_response = SaleResponse(
        sale_id=f"{BRANCH_ID}_{sale_timestamp.isoformat()}",
        product_name=product.name,
        quantity_sold=sale_request.quantity,
        total_amount=total_amount,
        timestamp=sale_timestamp,
        status="completed"
    )
    
    sales_history.append(sale_response)
    
    logger.info(
        f"💰 Venta procesada LOCALMENTE: {sale_request.quantity}x {product.name} "
        f"por ${total_amount:.2f}. Stock restante: {product.stock}"
    )
    
    # PASO 3: Notificar al central de forma ASÍNCRONA
    # Esta operación NO bloquea la respuesta al cliente
    background_tasks.add_task(
        notify_central_about_sale,
        sale_request.product_id,
        sale_request.quantity,
        sale_timestamp,
        total_amount
    )
    
    return sale_response

@app.get("/sales/stats", tags=["Ventas"])
async def get_sales_stats():
    """Estadísticas de ventas de la sucursal"""
    if not sales_history:
        return {"total_sales": 0, "total_revenue": 0, "average_sale": 0}
    
    total_revenue = sum(sale.total_amount for sale in sales_history)
    return {
        "total_sales": len(sales_history),
        "total_revenue": round(total_revenue, 2),
        "average_sale": round(total_revenue / len(sales_history), 2)
    }

# Interfaz visual básica para ventas
@app.get("/dashboard", response_class=HTMLResponse, tags=["Visual"])
async def dashboard():
    """Dashboard básico de la sucursal"""
    try:
        with open("sucursal_dashboard.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        # Crear un dashboard básico si no existe el archivo
        basic_dashboard = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>EcoMarket - Dashboard Sucursal</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
        </head>
        <body class="bg-light">
            <div class="container mt-4">
                <div class="row">
                    <div class="col-12">
                        <div class="card">
                            <div class="card-header bg-success text-white">
                                <h2><i class="bi bi-shop"></i> EcoMarket - Sucursal Dashboard</h2>
                            </div>
                            <div class="card-body">
                                <p>Dashboard básico de la sucursal. Para funcionalidad completa, implementar sucursal_dashboard.html</p>
                                <div class="row">
                                    <div class="col-md-4">
                                        <a href="/inventory" class="btn btn-primary w-100 mb-2">
                                            <i class="bi bi-box"></i> Ver Inventario
                                        </a>
                                    </div>
                                    <div class="col-md-4">
                                        <a href="/sales" class="btn btn-info w-100 mb-2">
                                            <i class="bi bi-cash"></i> Ver Ventas
                                        </a>
                                    </div>
                                    <div class="col-md-4">
                                        <a href="/docs" class="btn btn-warning w-100 mb-2">
                                            <i class="bi bi-book"></i> API Docs
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=basic_dashboard)

async def notify_central_about_sale(
    product_id: int,
    quantity_sold: int,
    timestamp: datetime,
    sale_amount: float
):
    """
    CONCEPTO CLAVE: Comunicación asíncrona resiliente
    
    Esta función se ejecuta en segundo plano.
    Si falla, la venta ya está completada localmente.
    """
    notification = {
        "branch_id": BRANCH_ID,
        "product_id": product_id,
        "quantity_sold": quantity_sold,
        "timestamp": timestamp.isoformat(),
        "sale_price": sale_amount
    }
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            logger.info("📡 Enviando notificación al servidor central...")
            
            response = await client.post(
                f"{CENTRAL_API_URL}/sale-notification",
                json=notification
            )
            
            if response.status_code == 200:
                logger.info("✅ Notificación enviada exitosamente")
            else:
                logger.warning(f"⚠️ Respuesta inesperada: {response.status_code}")
                
    except Exception as e:
        logger.error(f"❌ Error al notificar al central: {e}")
        # IMPORTANTE: La venta YA está completada, esto es solo notificación

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)