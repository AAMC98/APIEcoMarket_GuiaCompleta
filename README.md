# 🌱 EcoMarket - Sistema de Gestión de Inventario Multi-Sucursal

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple.svg)
![Status](https://img.shields.io/badge/Status-Funcional-brightgreen.svg)

## 📋 Descripción

**EcoMarket** es un sistema completo de gestión de inventario para múltiples sucursales desarrollado con **FastAPI** y **Bootstrap**. Permite administrar productos, ventas y notificaciones tanto en una central como en sucursales remotas de forma integrada.

## ✨ Características Principales

### 🏢 **API Central**
- ✅ Dashboard Bootstrap profesional
- ✅ CRUD completo de productos
- ✅ Sistema de notificaciones en tiempo real
- ✅ Gestión de ventas con métricas
- ✅ Interfaz responsiva moderna

### 🏪 **APIs de Sucursales**
- ✅ Inventario independiente por sucursal
- ✅ Sincronización con central
- ✅ Modal de edición elegante
- ✅ Monitoreo de conexiones
- ✅ Estadísticas de ventas locales

### 🎯 **Funcionalidades Destacadas**
- 🔄 **Sincronización automática** entre central y sucursales
- 📊 **Dashboard interactivo** con gráficos y métricas
- 🎨 **Diseño minimalista** y fácil de usar
- 📱 **Interfaz responsive** para cualquier dispositivo
- ⚡ **Edición rápida** con modal y atajos de teclado
- 🔍 **Monitoreo en tiempo real** del estado de sucursales

## 🚀 Instalación y Configuración

### **Prerrequisitos**
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### **1. Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/ecomarket.git
cd ecomarket
```

### **2. Crear entorno virtual**
```bash
python -m venv venv

# En Windows
venv\\Scripts\\activate

# En Linux/Mac
source venv/bin/activate
```

### **3. Instalar dependencias**
```bash
pip install -r requirements.txt
```

## 🎮 Uso del Sistema

### **Iniciar Servidor Central**
```bash
python central_api.py
```
- 🌐 Dashboard: `http://localhost:8000`
- 📚 API Docs: `http://localhost:8000/docs`

### **Iniciar Sucursales**
```bash
# Sucursal Norte (Puerto 8001)
python sucursal_api.py --port 8001

# Sucursal Sur (Puerto 8002)  
python sucursal_api.py --port 8002

# Sucursal Centro (Puerto 8003)
python sucursal_api.py --port 8003
```

## 📊 Funcionalidades del Dashboard

### **🏢 Inventario Central**
- Ver todos los productos con paginación
- Agregar nuevos productos con modal
- Editar productos existentes
- Eliminar productos con confirmación
- Filtros por stock (crítico, bajo, normal)

### **🏪 Inventario de Sucursales**
- Seleccionar sucursal del dropdown
- Ver inventario en tiempo real
- Editar stock con modal elegante
- Sincronizar productos con central
- Comparar diferencias de stock

### **🔔 Centro de Notificaciones**
- Notificaciones de ventas en tiempo real
- Alertas de stock bajo
- Historial de actividades
- Sistema de badges por importancia

## 🛠️ Tecnologías Utilizadas

### **Backend**
- **FastAPI 0.104.1** - Framework web moderno
- **Uvicorn** - Servidor ASGI de alto rendimiento
- **Pydantic** - Validación de datos
- **HTTPX** - Cliente HTTP asíncrono

### **Frontend**
- **Bootstrap 5.3.0** - Framework CSS
- **Bootstrap Icons** - Iconografía moderna
- **JavaScript ES6** - Funcionalidad interactiva
- **Jinja2** - Motor de plantillas

### **Herramientas**
- **Git** - Control de versiones
- **Python Virtual Environment** - Aislamiento de dependencias

## 📁 Estructura del Proyecto

```
ecomarket/
├── central_api.py              # API principal con dashboard
├── sucursal_api.py            # API de sucursales
├── requirements.txt           # Dependencias Python
├── templates/                 # Plantillas HTML
│   ├── central_dashboard.html # Dashboard principal
│   └── sucursal_dashboard.html# Dashboard de sucursal
├── static/                    # Archivos estáticos
│   ├── css/
│   └── js/
├── docs/                      # Documentación
│   ├── DISEÑO_INVENTARIO_SUCURSAL.md
│   ├── INTEGRACIÓN_API_REAL.md
│   └── DECISIONS.md
└── README.md                  # Este archivo
```

## 🎯 Endpoints de API

### **Central API (Puerto 8000)**
- `GET /` - Dashboard principal
- `GET /products` - Listar productos
- `POST /products` - Crear producto
- `PUT /products/{id}` - Actualizar producto
- `DELETE /products/{id}` - Eliminar producto
- `GET /notifications` - Obtener notificaciones
- `POST /sales` - Registrar venta

### **Sucursal API (Puertos 8001-8003)**
- `GET /` - Dashboard de sucursal
- `GET /inventory` - Inventario local
- `PUT /products/{id}` - Actualizar stock
- `GET /sales/stats` - Estadísticas de ventas
- `GET /health` - Estado de la sucursal

## 🎨 Capturas de Pantalla

### Dashboard Central
![Dashboard Central](docs/images/central-dashboard.png)

### Inventario de Sucursales
![Inventario Sucursales](docs/images/sucursal-inventory.png)

### Modal de Edición
![Modal Edición](docs/images/edit-modal.png)

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**Tu Nombre**
- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Email: tu-email@ejemplo.com

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- Bootstrap por el sistema de diseño
- La comunidad de Python por las librerías utilizadas

---

⭐ **¡Si te gusta este proyecto, dale una estrella!** ⭐