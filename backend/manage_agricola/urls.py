from django.contrib import admin
from django.urls import path
from app.views import (
    actualizar_pais, crear_pais, eliminar_pais, listar_estados, listar_paises,listar_paises_activos,
    listar_empresas, crear_empresa, actualizar_empresa, eliminar_empresa, listar_empresas_activas,
    listar_monedas, crear_moneda, actualizar_moneda, eliminar_moneda, listar_monedas_activas,
    listar_departamentos, crear_departamento, actualizar_departamento, eliminar_departamento, listar_departamentos_activos,
    listar_provincias, crear_provincia, actualizar_provincia, eliminar_provincia, listar_provincias_activas,
    listar_distritos, crear_distrito, actualizar_distrito, eliminar_distrito,
    listar_centros, crear_centro, actualizar_centro, eliminar_centro, listar_centros_activos,
    listar_almacenes, crear_almacen, actualizar_almacen, eliminar_almacen,
    listar_proveedores, crear_proveedor, actualizar_proveedor, eliminar_proveedor,
    listar_grupos, crear_grupo, actualizar_grupo, eliminar_grupo, listar_grupos_activos,
    listar_subgrupos, crear_subgrupo, actualizar_subgrupo, eliminar_subgrupo, listar_subgrupos_activos,
    listar_productos, crear_producto, actualizar_producto, eliminar_producto, 
    listar_tipoingsal, #crear_tipoingsal, actualizar_tipoingsal, eliminar_tipoingsal,
    listar_tipomovimientos, crear_tipomovimiento, actualizar_tipomovimiento, eliminar_tipomovimiento,
    listar_tipodocumentos, crear_tipodocumento, actualizar_tipodocumento, eliminar_tipodocumento,
    listar_campanias, crear_campania, actualizar_campania, eliminar_campania,
    listar_cultivos,crear_cultivo, actualizar_cultivo, eliminar_cultivo, listar_cultivos_activos,
    listar_variedades,crear_variedad, actualizar_variedad, eliminar_variedad,
    listar_auditoria, listar_auditoria_pordia
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #------------------------------------------------- # URL GENERALES #---------------------------------------------------#
    
    #-------------------------------------------------- ESTADO ---------------------------------------------------------------#
    path('api/estado/', listar_estados, name="listar_estados"),
    
    #-------------------------------------------------- PAIS ---------------------------------------------------------------#
    path('api/paises/', listar_paises, name="listar_paises"),
    path('api/paises/crear/', crear_pais, name="crear_pais"),
    path('api/paises/actualizar/<int:id>/', actualizar_pais, name="actualizar_pais"),
    path('api/paises/eliminar/<int:id>/', eliminar_pais, name="eliminar_pais"),
    
    #---- PARA SELECCIONAR LOS ACTIVOS DE PAISES
    path('api/paisesactivos/', listar_paises_activos, name="listar_paise_activos"),

    #-------------------------------------------------- MONEDA ---------------------------------------------------------------#
    path('api/monedas/', listar_monedas, name="listar_monedas"),
    
    path('api/monedas/crear/', crear_moneda, name="crear_moneda"),
    path('api/monedas/actualizar/<int:id>/', actualizar_moneda, name="actualizar_moneda"),
    path('api/monedas/eliminar/<int:id>/', eliminar_moneda, name="eliminar_moneda"),
    
    
    #---- PARA SELECCIONAR LOS ACTIVOS DE MONEDAS
    path('api/monedasactivas/', listar_monedas_activas, name="listar_monedas_activas"),
    
    #-------------------------------------------------- EMPRESA ---------------------------------------------------------------#
    path('api/empresas/', listar_empresas, name="listar_empresas"),
    path('api/empresas/crear/', crear_empresa, name="crear_empresa"),
    path('api/empresas/actualizar/<int:id>/', actualizar_empresa, name="actualizar_empresa"),
    path('api/empresas/eliminar/<int:id>/', eliminar_empresa, name="eliminar_empresa"),
    
    #---- PARA SELECCIONAR LOS ACTIVOS DE EMPRESAS
    path('api/empresasactivas/', listar_empresas_activas, name="listar_empresas_activas"),
    #-------------------------------------------------- DEPARTAMENTO ---------------------------------------------------------------#
    path('api/departamentos/', listar_departamentos, name="listar_departamentos"),
    path('api/departamentos/crear/', crear_departamento, name="crear_departamento"),
    path('api/departamentos/actualizar/<int:id>/', actualizar_departamento, name="actualizar_departamento"),
    path('api/departamentos/eliminar/<int:id>/', eliminar_departamento, name="eliminar_departamento"),
    
    #---- PARA SELECCIONAR LOS ACTIVOS DE DEPARTAMENTOS
    path('api/departamentosactivos/', listar_departamentos_activos, name="listar_departamentos_activos"),
    
    #-------------------------------------------------- PROVINCIA ---------------------------------------------------------------#
    path('api/provincias/', listar_provincias, name="listar_provincias"),
    path('api/provincias/crear/', crear_provincia, name="crear_provincia"),
    path('api/provincias/actualizar/<int:id>/', actualizar_provincia, name="actualizar_provincia"),
    path('api/provincias/eliminar/<int:id>/', eliminar_provincia, name="eliminar_provincia"),
    
    #---- PARA SELECCIONAR LOS ACTIVOS DE PROVINCIAS
    path('api/provinciasactivas/', listar_provincias_activas, name="listar_provincias_activas"),
    
    #-------------------------------------------------- DISTRITO ---------------------------------------------------------------#
    path('api/distritos/', listar_distritos, name="listar_distritos"),
    path('api/distritos/crear/', crear_distrito, name="crear_distrito"),
    path('api/distritos/actualizar/<int:id>/', actualizar_distrito, name="actualizar_distrito"),
    path('api/distritos/eliminar/<int:id>/', eliminar_distrito, name="eliminar_distrito"),
    
    #------------------------------------------------- # URL LOGISTICOS #---------------------------------------------------#
    
    #-------------------------------------------------- CENTRO ---------------------------------------------------------------#
    path('api/centros/', listar_centros, name="listar_centros"),
    path('api/centros/crear/', crear_centro, name="crear_centro"),
    path('api/centros/actualizar/<int:id>/', actualizar_centro, name="actualizar_centro"),
    path('api/centros/eliminar/<int:id>/', eliminar_centro, name="eliminar_centro"),
    
    #---- PARA SELECCIONAR LOS ACTIVOS DE CENTROS
    path('api/centrosactivos/', listar_centros_activos, name="listar_centros_activos"),
    
    #-------------------------------------------------- ALMACEN ---------------------------------------------------------------#
    path('api/almacenes/', listar_almacenes, name="listar_almacenes"),
    path('api/almacenes/crear/', crear_almacen, name="crear_almacen"),
    path('api/almacenes/actualizar/<int:id>/', actualizar_almacen, name="actualizar_almacen"),
    path('api/almacenes/eliminar/<int:id>/', eliminar_almacen, name="eliminar_almacen"),
    
    #-------------------------------------------------- PROVEEDOR ---------------------------------------------------------------#
    path('api/proveedores/', listar_proveedores, name="listar_proveedores"),
    path('api/proveedores/crear/', crear_proveedor, name="crear_proveedor"),
    path('api/proveedores/actualizar/<int:id>/', actualizar_proveedor, name="actualizar_proveedor"),
    path('api/proveedores/eliminar/<int:id>/', eliminar_proveedor, name="eliminar_proveedor"),
    
    #-------------------------------------------------- GRUPO ---------------------------------------------------------------#
    path('api/grupos/', listar_grupos, name="listar_grupos"),
    path('api/grupos/crear/', crear_grupo, name="crear_grupo"),
    path('api/grupos/actualizar/<int:id>/', actualizar_grupo, name="actualizar_grupo"),
    path('api/grupos/eliminar/<int:id>/', eliminar_grupo, name="eliminar_grupo"),
    
    #---- PARA SELECCIONAR LOS ACTIVOS DE GRUPOS
    path('api/gruposactivos/', listar_grupos_activos, name="listar_grupos"),
    
    #-------------------------------------------------- SUBGRUPO ---------------------------------------------------------------#
    path('api/subgrupos/', listar_subgrupos, name="listar_subgrupos"),
    path('api/subgrupos/crear/', crear_subgrupo, name="crear_subgrupo"),
    path('api/subgrupos/actualizar/<int:id>/', actualizar_subgrupo, name="actualizar_subgrupo"),
    path('api/subgrupos/eliminar/<int:id>/', eliminar_subgrupo, name="eliminar_subgrupo"),
    
    
    
    path('api/subgruposactivos/', listar_subgrupos_activos, name="listar_subgrupos_activos"),
    #-------------------------------------------------- PRODUCTO ---------------------------------------------------------------#
    path('api/productos/', listar_productos, name="listar_productos"),
    path('api/productos/crear/', crear_producto, name="crear_producto"),
    path('api/productos/actualizar/<int:id>/', actualizar_producto, name="actualizar_producto"),
    path('api/productos/eliminar/<int:id>/', eliminar_producto, name="eliminar_producto"),
    
    #-------------------------------------------------- TIPO INGRESO/SALIDA ---------------------------------------------------#
    path('api/tipoingsal/', listar_tipoingsal, name="listar_tipoingsal"),
    #path('api/tipoingsal/crear/', crear_tipoingsal, name="crear_tipoingsal"),
    #path('api/tipoingsal/actualizar/<int:id>/', actualizar_tipoingsal, name="actualizar_tipoingsal"),
    #path('api/tipoingsal/eliminar/<int:id>/', eliminar_tipoingsal, name="eliminar_tipoingsal"),
    
    #-------------------------------------------------- TIPO MOVIMIENTO -------------------------------------------------------#
    path('api/movimientos/', listar_tipomovimientos, name="listar_tipomovimientos"),
    path('api/movimientos/crear/', crear_tipomovimiento, name="crear_tipomovimiento"),
    path('api/movimientos/actualizar/<int:id>/', actualizar_tipomovimiento, name="actualizar_tipomovimiento"),
    path('api/movimientos/eliminar/<int:id>/', eliminar_tipomovimiento, name="eliminar_tipomovimiento"),
    
    #-------------------------------------------------- TIPO DOCUMENTO -------------------------------------------------------#
    path('api/documentos/', listar_tipodocumentos, name="listar_tipodocumentos"),
    path('api/documentos/crear/', crear_tipodocumento, name="crear_tipodocumento"),
    path('api/documentos/actualizar/<int:id>/', actualizar_tipodocumento, name="actualizar_tipodocumento"),
    path('api/documentos/eliminar/<int:id>/', eliminar_tipodocumento, name="eliminar_tipodocumento"),
    
    #------------------------------------------------- # URL AGRICOLAS #---------------------------------------------------#
    
    #------------------------------------------------- # CAMPAÑIA #--------------------------------------------------------#
    path('api/campanias/', listar_campanias, name="listar_campanias"),
    path('api/campanias/crear/', crear_campania, name="crear_campania"),
    path('api/campanias/actualizar/<int:id>/', actualizar_campania, name="actualizar_campania"),
    path('api/campanias/eliminar/<int:id>/', eliminar_campania, name="eliminar_campania"),
    
    #------------------------------------------------- # CULTIVO #--------------------------------------------------------#
    path('api/cultivos/', listar_cultivos, name="listar_cultivos"),
    path('api/cultivos/crear/', crear_cultivo, name="crear_cultivo"),
    path('api/cultivos/actualizar/<int:id>/', actualizar_cultivo, name="actualizar_cultivo"),
    path('api/cultivos/eliminar/<int:id>/', eliminar_cultivo, name="eliminar_cultivo"),
    
    #---- PARA SELECCIONAR LOS ACTIVOS DE CULTIVOS
    path('api/cultivosactivos/', listar_cultivos_activos, name="listar_cultivos_activos"),
    #------------------------------------------------- # VARIEDAD #--------------------------------------------------------#
    path('api/variedades/', listar_variedades, name="listar_variedades"),
    path('api/variedades/crear/', crear_variedad, name="crear_variedad"),
    path('api/variedades/actualizar/<int:id>/', actualizar_variedad, name="actualizar_variedad"),
    path('api/variedades/eliminar/<int:id>/', eliminar_variedad, name="eliminar_variedad"),
    
    #------------------------------------------------- # AUDITORIA #--------------------------------------------------------#
    path('api/auditoria/', listar_auditoria, name="listar_auditoria"),
    
    path('api/auditoriapordia/', listar_auditoria_pordia, name='auditoria_pordia'),
    
]

