# Principios de Diseño para EcoMarket

## 1. Principio de Autonomía de Sucursales (Offline-First)

* **Principio Clave que Adoptaremos**: Cada sucursal operará de forma autónoma, 
  manteniendo su propio inventario local y procesando ventas sin depender 
  de la conectividad con el servidor central.

* **Justificación**: Aprendimos de casos como el de Amazon en sus centros de 
  distribución que las fallas en la red central no pueden detener las 
  operaciones críticas del negocio. La venta debe completarse inmediatamente.

* **Riesgo que Mitigaremos**: Evitaremos las consultas de inventario síncronas 
  entre sucursales durante el proceso de venta.

* **Justificación**: Una espera de más de 2-3 segundos por una consulta de stock 
  es inaceptable en el punto de venta y genera una mala experiencia del cliente.

## 2. Principio de Consistencia Eventual

* **Principio Clave que Adoptaremos**: Implementaremos un modelo de "consistencia 
  eventual" donde las actualizaciones de inventario se propagan de forma 
  asíncrona entre sucursales.

* **Justificación**: Basado en el teorema CAP, priorizamos Disponibilidad 
  (Availability) y Tolerancia a Particiones (Partition Tolerance) sobre 
  Consistencia absoluta, ya que es más importante completar la venta que 
  tener datos perfectamente sincronizados en tiempo real.

* **Riesgo que Mitigaremos**: Posibles sobreventas temporales de productos 
  con stock limitado.

* **Justificación**: Es mejor manejar ocasionalmente una sobreventa (que se 
  puede resolver con el cliente) que perder ventas por un sistema no disponible.

## Estrategia de Consistencia

### Modelo Adoptado: Consistencia Eventual

**Trade-off Aceptado**: 
- ✅ **Ganamos**: Ventas rápidas, operación sin internet, mejor experiencia del cliente
- ⚠️ **Aceptamos**: Posibles discrepancias temporales en el inventario central