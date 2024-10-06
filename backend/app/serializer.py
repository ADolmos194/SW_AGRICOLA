import pytz
from rest_framework import serializers
from .models import Estado, Pais, Moneda, Empresa, Departamento, Provincia, Distrito, Centro, Almacen, Proveedor, Grupo, Subgrupo, Producto, Tipoingsal, Tipomovimiento, Tipodocumento, Campania, Cultivo, Variedad, Auditoria

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = '__all__'

class AuditoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditoria
        fields = '__all__'

class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = '__all__' 

class MonedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moneda
        fields = '__all__' 

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'

class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = '__all__'
        

class DistritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distrito
        fields = '__all__'  
        
class CentroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Centro
        fields = '__all__'  

class AlmacenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Almacen
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = '__all__'

class SubgrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subgrupo
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class TipoingsalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipoingsal
        fields = '__all__'

class TipomovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipomovimiento
        fields = '__all__'

class TipodocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipodocumento
        fields = '__all__'
    
            
class CampaniaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campania
        fields = '__all__'

class CultivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cultivo
        fields = '__all__'

class VariedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variedad
        fields = '__all__'
        

