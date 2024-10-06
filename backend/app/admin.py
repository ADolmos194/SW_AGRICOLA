from django.contrib import admin

from app.models import Auditoria, Estado, Pais, Pais, Moneda, Empresa, Departamento, Provincia, Distrito, Centro, Almacen, Proveedor,Grupo, Subgrupo, Producto, Tipoingsal, Tipomovimiento, Tipodocumento, Campania, Cultivo, Variedad

# Register your models here.
admin.site.register([Auditoria, 
                    Estado, Pais, Moneda, Empresa, Departamento,
                    Provincia, Distrito, Centro, Almacen, Proveedor,Grupo, 
                    Subgrupo, Producto, Tipoingsal, Tipomovimiento, Tipodocumento, 
                    Campania, Cultivo, Variedad])