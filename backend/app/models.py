from django.db import models

"""
############################################################################################################
###################################  MODELO ESTADO - GENERAL - LOGÍSTICO- AGRÍCOLA  #########################
############################################################################################################
"""


# -------------------------------------------- MODELO ESTADO --------------------------------------------------
# El modelo Estado representa un estado general que puede aplicarse a otros modelos.
class Estado(models.Model):
    # ID autoincremental que sirve como clave primaria
    id = models.AutoField(primary_key=True)
    # Nombre del estado, opcional
    nombre = models.CharField(max_length=18, null=True, blank=True)

    # Se define el nombre de la tabla en la base de datos
    class Meta:
        db_table = "estado"


"""
############################################################################################################
#########################################  MODELOS GENERALES  ###############################################
############################################################################################################
"""


# -------------------------------------------- MODELO PAIS --------------------------------------------------
# El modelo País define los detalles básicos de un país.
class Pais(models.Model):
    # ID autoincremental que sirve como clave primaria
    id = models.AutoField(primary_key=True)
    # Nombre completo del país, opcional
    nombre = models.CharField(max_length=255, null=True, blank=True)
    # Abreviatura del país, opcional
    abreviatura = models.CharField(max_length=18, null=True, blank=True)
    # Relación con el modelo Estado, indica si el país está activo o inactivo
    estado = models.ForeignKey("Estado", on_delete=models.CASCADE)
    # Fecha de creación del registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Fecha de la última modificación del registro
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pais"



# -------------------------------------------- MODELO MONEDA --------------------------------------------------
# El modelo Moneda almacena los detalles de las monedas utilizadas en un país.
class Moneda(models.Model):
    # ID autoincremental que sirve como clave primaria
    id = models.AutoField(primary_key=True)
    # Nombre de la moneda, opcional
    nombre = models.CharField(max_length=18, null=True, blank=True)
    # Abreviatura de la moneda, opcional
    abreviatura = models.CharField(max_length=18, null=True, blank=True)
    # Relación con el modelo Estado, indica si la moneda está activa o inactiva
    estado = models.ForeignKey("Estado", on_delete=models.CASCADE)
    # Fecha de creación del registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Fecha de la última modificación del registro
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "moneda"


# -------------------------------------------- MODELO EMPRESA --------------------------------------------------
# El modelo Empresa almacena información relacionada con las empresas.
class Empresa(models.Model):
    # ID autoincremental que sirve como clave primaria
    id = models.AutoField(primary_key=True)
    # Nombre completo de la empresa, opcional
    nombre = models.CharField(max_length=255, null=True, blank=True)
    # Abreviatura de la empresa, opcional
    abreviatura = models.CharField(max_length=18, null=True, blank=True)
    # Número de Registro Único de Contribuyente, opcional
    ruc = models.CharField(max_length=18, null=True, blank=True)
    # Relación con el modelo País
    pais = models.ForeignKey("Pais", on_delete=models.CASCADE)
    # Relación con el modelo Moneda
    moneda = models.ForeignKey("Moneda", on_delete=models.CASCADE)
    # Relación con el modelo Estado, indica si la empresa está activa o inactiva
    estado = models.ForeignKey("Estado", on_delete=models.CASCADE)
    # Fecha de creación del registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Fecha de la última modificación del registro
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "empresa"


# -------------------------------------------- MODELO DEPARTAMENTO --------------------------------------------------
# El modelo Departamento almacena los detalles de los departamentos dentro de un país.
class Departamento(models.Model):
    # ID autoincremental que sirve como clave primaria
    id = models.AutoField(primary_key=True)
    # Nombre del departamento, opcional
    nombre = models.CharField(max_length=255, null=True, blank=True)
    # Abreviatura del departamento, opcional
    abreviatura = models.CharField(max_length=18, null=True, blank=True)
    # Relación con el modelo País
    pais = models.ForeignKey("Pais", on_delete=models.CASCADE)
    # Relación con el modelo Estado, indica si el departamento está activo o inactivo
    estado = models.ForeignKey("Estado", on_delete=models.CASCADE)
    # Fecha de creación del registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Fecha de la última modificación del registro
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "departamento"


# -------------------------------------------- MODELO PROVINCIA --------------------------------------------------
# El modelo Provincia almacena los detalles de las provincias dentro de un departamento.
class Provincia(models.Model):
    # ID autoincremental que sirve como clave primaria
    id = models.AutoField(primary_key=True)
    # Nombre de la provincia, opcional
    nombre = models.CharField(max_length=255, null=True, blank=True)
    # Abreviatura de la provincia, opcional
    abreviatura = models.CharField(max_length=18, null=True, blank=True)
    # Relación con el modelo Departamento
    departamento = models.ForeignKey("Departamento", on_delete=models.CASCADE)
    # Relación con el modelo Estado, indica si la provincia está activa o inactiva
    estado = models.ForeignKey("Estado", on_delete=models.CASCADE)
    # Fecha de creación del registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Fecha de la última modificación del registro
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "provincia"


# -------------------------------------------- MODELO DISTRITO --------------------------------------------------
# El modelo Distrito almacena los detalles de los distritos dentro de una provincia.
class Distrito(models.Model):
    # ID autoincremental que sirve como clave primaria
    id = models.AutoField(primary_key=True)
    # Nombre del distrito, opcional
    nombre = models.CharField(max_length=255, null=True, blank=True)
    # Abreviatura del distrito, opcional
    abreviatura = models.CharField(max_length=18, null=True, blank=True)
    # Relación con el modelo Provincia
    provincia = models.ForeignKey("Provincia", on_delete=models.CASCADE)
    # Relación con el modelo Estado, indica si el distrito está activo o inactivo
    estado = models.ForeignKey("Estado", on_delete=models.CASCADE)
    # Fecha de creación del registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Fecha de la última modificación del registro
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "distrito"



"""
############################################################################################################
#######################################  MODELOS LOGÍSTICOS ################################################
############################################################################################################
"""


# -------------------------------------------- MODELO CENTRO --------------------------------------------------
# El modelo Centro almacena información sobre los centros logísticos de una empresa.
class Centro(models.Model):
    # ID autoincremental que sirve como clave primaria
    id = models.AutoField(primary_key=True)
    # Nombre del centro logístico, opcional
    nombre = models.CharField(max_length=255, null=True, blank=True)
    # Abreviatura del centro logístico, opcional
    abreviatura = models.CharField(max_length=18, null=True, blank=True)
    # Relación con el modelo Empresa
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    # Relación con el modelo Estado, indica si el centro está activo o inactivo
    estado = models.ForeignKey("Estado", on_delete=models.CASCADE)
    # Fecha de creación del registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Fecha de la última modificación del registro
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "centro"


# -------------------------------------------- MODELO ALMACÉN --------------------------------------------------
# El modelo Almacén almacena información sobre los almacenes asociados a un centro logístico.
class Almacen(models.Model):
    # ID autoincremental que sirve como clave primaria
    id = models.AutoField(primary_key=True)
    # Nombre del almacén, opcional
    nombre = models.CharField(max_length=255, null=True, blank=True)
    # Abreviatura del almacén, opcional
    abreviatura = models.CharField(max_length=18, null=True, blank=True)
    # Relación con el modelo Centro
    centro = models.ForeignKey("Centro", on_delete=models.CASCADE)
    # Relación con el modelo Estado, indica si el almacén está activo o inactivo
    estado = models.ForeignKey("Estado", on_delete=models.CASCADE)
    # Fecha de creación del registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Fecha de la última modificación del registro
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "almacen"



# -------------------------------------------- MODELO PROVEEDOR --------------------------------------------------
# El modelo Proveedor almacena información sobre los proveedores que suministran productos a la empresa.
class Proveedor(models.Model):
    # ID autoincremental que sirve como clave primaria
    id = models.AutoField(primary_key=True)
    # Nombre del proveedor, opcional
    nombre = models.CharField(max_length=255, null=True, blank=True)
    # Abreviatura del proveedor, opcional
    abreviatura = models.CharField(max_length=18, null=True, blank=True)
    # Relación con el modelo Estado, indica si el proveedor está activo o inactivo
    estado = models.ForeignKey("Estado", on_delete=models.CASCADE)
    # Fecha de creación del registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Fecha de la última modificación del registro
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "proveedor"


# -------------------------------------------- MODELO GRUPO --------------------------------------------------
# El modelo Grupo almacena información sobre los diferentes grupos de productos.
class Grupo(models.Model):
    # ID autoincremental que sirve como clave primaria
    id = models.AutoField(primary_key=True)
    # Nombre del grupo de productos, opcional
    nombre = models.CharField(max_length=255, null=True, blank=True)
    # Abreviatura del grupo, opcional
    abreviatura = models.CharField(max_length=18, null=True, blank=True)
    # Relación con el modelo Estado, indica si el grupo está activo o inactivo
    estado = models.ForeignKey("Estado", on_delete=models.CASCADE)
    # Fecha de creación del registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Fecha de la última modificación del registro
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "grupo"


# -------------------------------------------- MODELO SUBGRUPO --------------------------------------------------
# El modelo Subgrupo almacena información sobre los subgrupos dentro de un grupo de productos.
class Subgrupo(models.Model):
    # ID autoincremental que sirve como clave primaria
    id = models.AutoField(primary_key=True)
    # Nombre del subgrupo de productos, opcional
    nombre = models.CharField(max_length=255, null=True, blank=True)
    # Abreviatura del subgrupo, opcional
    abreviatura = models.CharField(max_length=18, null=True, blank=True)
    # Relación con el modelo Grupo
    grupo = models.ForeignKey("Grupo", on_delete=models.CASCADE)
    # Relación con el modelo Estado, indica si el subgrupo está activo o inactivo
    estado = models.ForeignKey("Estado", on_delete=models.CASCADE)
    # Fecha de creación del registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Fecha de la última modificación del registro
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "subgrupo"


# -------------------------------------------- MODELO PRODUCTO --------------------------------------------------
# El modelo Producto almacena información sobre los productos específicos.
class Producto(models.Model):
    # ID autoincremental que sirve como clave primaria
    id = models.AutoField(primary_key=True)
    # Nombre del producto, opcional
    nombre = models.CharField(max_length=255, null=True, blank=True)
    # Abreviatura del producto, opcional
    abreviatura = models.CharField(max_length=18, null=True, blank=True)
    # Relación con el modelo Subgrupo
    subgrupo = models.ForeignKey("Subgrupo", on_delete=models.CASCADE)
    # Relación con el modelo Estado, indica si el producto está activo o inactivo
    estado = models.ForeignKey("Estado", on_delete=models.CASCADE)
    # Fecha de creación del registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Fecha de la última modificación del registro
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "producto"

# -------------------------------------------- MODELO TIPOINGRESO/SALIDA ----------------------------------------
# El modelo Tipoingsal almacena los tipos de ingresos o salidas de productos en el sistema.
class Tipoingsal(models.Model):
    # ID autoincremental que sirve como clave primaria
    id = models.AutoField(primary_key=True)
    # Nombre del tipo de ingreso o salida, opcional
    nombre = models.CharField(max_length=255, null=True, blank=True)
    # Abreviatura del tipo de ingreso o salida, opcional
    abreviatura = models.CharField(max_length=18, null=True, blank=True)
    # Relación con el modelo Estado, indica si el tipo está activo o inactivo
    estado = models.ForeignKey("Estado", on_delete=models.CASCADE)
    # Fecha de creación del registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Fecha de la última modificación del registro
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tipoingsal"

# -------------------------------------------- MODELO TIPOMOVIMIENTO ---------------------------------------------
# El modelo Tipomovimiento almacena los diferentes tipos de movimientos de inventario en la empresa.
class Tipomovimiento(models.Model):
    # ID autoincremental que sirve como clave primaria
    id = models.AutoField(primary_key=True)
    # Nombre del tipo de movimiento, opcional
    nombre = models.CharField(max_length=255, null=True, blank=True)
    # Abreviatura del tipo de movimiento, opcional
    abreviatura = models.CharField(max_length=18, null=True, blank=True)
    # Relación con el modelo Empresa
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    # Relación con el modelo Tipoingsal
    tipo_ing_sal = models.ForeignKey("Tipoingsal", on_delete=models.CASCADE)
    # Relación con el modelo Estado, indica si el tipo de movimiento está activo o inactivo
    estado = models.ForeignKey("Estado", on_delete=models.CASCADE)
    # Fecha de creación del registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Fecha de la última modificación del registro
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tipomovimiento"


# -------------------------------------------- MODELO TIPO DOCUMENTO ---------------------------------------------
# El modelo Tipodocumento almacena información sobre los diferentes tipos de documentos generados.
class Tipodocumento(models.Model):
    # ID autoincremental que sirve como clave primaria
    id = models.AutoField(primary_key=True)
    # Nombre del tipo de documento, opcional
    nombre = models.CharField(max_length=255, null=True, blank=True)
    # Abreviatura del tipo de documento, opcional
    abreviatura = models.CharField(max_length=18, null=True, blank=True)
    # Relación con el modelo Empresa
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    # Relación con el modelo Tipoingsal
    tipo_ing_sal = models.ForeignKey("Tipoingsal", on_delete=models.CASCADE)
    # Relación con el modelo Estado, indica si el documento está activo o inactivo
    estado = models.ForeignKey("Estado", on_delete=models.CASCADE)
    # Fecha de creación del registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Fecha de la última modificación del registro
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tipodocumento"



"""############################################################################################################
############################################################################################################

#------------------------------------------ MODELOS AGRICOLA -----------------------------------------------

############################################################################################################
############################################################################################################"""


# -------------------------------------------- MODELO AGRICOLA --------------------------------------------------
# El modelo Campania almacena información sobre las campañas agrícolas realizadas en la empresa.
class Campania(models.Model):
    # ID autoincremental que sirve como clave primaria
    id = models.AutoField(primary_key=True)
    # Nombre de la campaña agrícola, opcional
    nombre = models.CharField(max_length=255, null=True, blank=True)
    # Abreviatura de la campaña agrícola, opcional
    abreviatura = models.CharField(max_length=18, null=True, blank=True)
    # Relación con el modelo Estado, indica si la campaña está activa o inactiva
    estado = models.ForeignKey("Estado", on_delete=models.CASCADE)
    # Fecha de creación del registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Fecha de la última modificación del registro
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "campania"


# -------------------------------------------- MODELO CULTIVO --------------------------------------------------
# El modelo Cultivo almacena información sobre los diferentes cultivos agrícolas.
class Cultivo(models.Model):
    # ID autoincremental que sirve como clave primaria
    id = models.AutoField(primary_key=True)
    # Nombre del cultivo, opcional
    nombre = models.CharField(max_length=255, null=True, blank=True)
    # Abreviatura del cultivo, opcional
    abreviatura = models.CharField(max_length=18, null=True, blank=True)
    # Relación con el modelo Estado, indica si el cultivo está activo o inactivo
    estado = models.ForeignKey("Estado", on_delete=models.CASCADE)
    # Fecha de creación del registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Fecha de la última modificación del registro
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cultivo"



# -------------------------------------------- MODELO VARIEDAD --------------------------------------------------
# El modelo Variedad almacena información sobre las variedades dentro de un cultivo específico.
class Variedad(models.Model):
    # ID autoincremental que sirve como clave primaria
    id = models.AutoField(primary_key=True)
    # Nombre de la variedad, opcional
    nombre = models.CharField(max_length=255, null=True, blank=True)
    # Abreviatura de la variedad, opcional
    abreviatura = models.CharField(max_length=18, null=True, blank=True)
    # Relación con el modelo Cultivo
    cultivo = models.ForeignKey("Cultivo", on_delete=models.CASCADE)
    # Relación con el modelo Estado, indica si la variedad está activa o inactiva
    estado = models.ForeignKey("Estado", on_delete=models.CASCADE)
    # Fecha de creación del registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Fecha de la última modificación del registro
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "variedad"



"""############################################################################################################
############################################################################################################

#------------------------------------------ MODELOS AUDITORIA -----------------------------------------------

############################################################################################################
############################################################################################################"""


# -------------------------------------------- MODELO AUDITORIA --------------------------------------------------
# El modelo Auditoria almacena información sobre los eventos y acciones registradas en el sistema.
class Auditoria(models.Model):
    # ID autoincremental que sirve como clave primaria
    id = models.AutoField(primary_key=True)
    # Nombre de la tabla donde ocurrió el evento
    tabla = models.CharField(max_length=255)
    # Tipo de evento registrado (ej: INSERT, UPDATE, DELETE)
    evento = models.CharField(max_length=255)
    # Sentencia SQL que describe la operación realizada
    sentencia = models.TextField()
    # ID del registro afectado por el evento
    registro_id = models.BigIntegerField()
    # Nombre del usuario que realizó la acción, opcional
    usuario = models.CharField(max_length=255, null=True)
    # Fecha en que ocurrió el evento
    fecha = models.DateField(auto_now_add=True)
    # Hora en que ocurrió el evento
    hora = models.TimeField(auto_now_add=True)

    class Meta:
        db_table = "auditoria"

    # Método de clase para registrar un evento de auditoría en la base de datos
    @classmethod
    def registrar_evento(cls, tabla, evento, sentencia, registro_id, usuario):
        auditoria = cls(
            tabla=tabla,
            evento=evento,
            sentencia=sentencia,
            registro_id=registro_id,
            usuario=usuario,
        )
        auditoria.save()
