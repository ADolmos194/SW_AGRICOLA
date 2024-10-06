from datetime import datetime
from django.utils import timezone
import json
import logging
from django.db.models import Q
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.db import connection, transaction, DatabaseError

from app.serializer import (
    EstadoSerializer,
    AuditoriaSerializer,
    PaisSerializer,
    MonedaSerializer,
    EmpresaSerializer,
    DepartamentoSerializer,
    ProvinciaSerializer,
    DistritoSerializer,
    CentroSerializer,
    AlmacenSerializer,
    ProveedorSerializer,
    GrupoSerializer,
    SubgrupoSerializer,
    ProductoSerializer,
    TipoingsalSerializer,
    TipomovimientoSerializer,
    TipodocumentoSerializer,
    CampaniaSerializer,
    CultivoSerializer,
    VariedadSerializer,
)


from .models import (
    Auditoria,
    Estado,
    Pais,
    Moneda,
    Empresa,
    Departamento,
    Provincia,
    Distrito,
    Centro,
    Almacen,
    Proveedor,
    Grupo,
    Subgrupo,
    Producto,
    Tipoingsal,
    Tipomovimiento,
    Tipodocumento,
    Campania,
    Cultivo,
    Variedad,
)
import pytz
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from django.db import DatabaseError

from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger(__name__)


# ------------------------------------------------------ LISTA ESTADOS (TERMINADO SERIALIZER Y CURSOR) -----------------------------------------------------------
"""
# @api_view(["GET"])
# @transaction.atomic
# def listar_estados(request):
#     Esta función API permite listar los estados del sistema que no tengan el ID 3, ordenados de manera descendente. 
#     La función utiliza un cursor SQL para ejecutar la consulta directamente en la base de datos y luego 
#     serializa los resultados obtenidos. Si todo se ejecuta correctamente, retorna una lista de estados con sus IDs y nombres.
#
#     Parámetros:
#     - request: Solicitud HTTP recibida. Solo admite el método GET.
#
#     Respuesta:
#     - En caso de éxito:
#         Retorna un diccionario en formato JSON con la siguiente estructura:
#         {
#             "code": 200,
#             "status": "success",
#             "message": "Estados obtenidos correctamente",
#             "message_user": "Estados obtenidos correctamente",
#             "data": [ {"id": <id_estado>, "nombre": <nombre_estado>} ]
#         }
#
#     - En caso de error:
#         Si se produce un error en la base de datos, se captura la excepción DatabaseError y se registra un mensaje de error en el log.
#         La respuesta será un mensaje de error con un código 500:
#         {
#             "mensaje": "Error al listar los estados."
#         }
#
#     Funcionalidad adicional:
#     - Usa transacciones atómicas para asegurar la integridad de los datos.
#     - Emplea el serializer 'EstadoSerializer' para estructurar los datos en el formato correcto para la API.
#     - Si no se encuentran resultados, retorna un mensaje de error con código 400 y un arreglo vacío en la clave 'data'.

"""
@api_view(["GET"])
@transaction.atomic
def listar_estados(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Status system not found",
        "message_user": "Estados no encontrados",
        "data": [],
    }
    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                # Consulta SQL para obtener los estados
                cursor.execute("SELECT id, nombre FROM Estado WHERE id <> 3 ORDER BY id DESC")
                estados = cursor.fetchall()

                # Convertir las filas en diccionarios
                estados_data = [{"id": e[0], "nombre": e[1]} for e in estados]

            # Serialización de los datos obtenidos
            estado_serializer = EstadoSerializer(estados_data, many=True)

            # Configurar la respuesta con los datos serializados
            dic_response["data"] = estado_serializer.data
            dic_response["code"] = 200
            dic_response["status"] = "success"
            dic_response["message_user"] = "Estados obtenidos correctamente"
            dic_response["message"] = "Estados obtenidos correctamente"
            return Response(dic_response, status=status.HTTP_200_OK)

        except DatabaseError as e:
            logger.error(f"Error al listar los estados: {str(e)}")
            return Response(
                {"mensaje": "Error al listar los estados."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return Response([], status=status.HTTP_200_OK)


# ------------------------------------------------------ LISTA AUDITORIA (TERMINADO SERIALIZER Y CURSOR) -----------------------------------------------------------
""" 
# @api_view(["GET"])
# @transaction.atomic
# def listar_auditoria(request):
#     Esta función API lista los registros del sistema de auditoría, ordenados de manera descendente por el ID de auditoría. 
#     Utiliza un cursor SQL para ejecutar una consulta directamente en la base de datos que obtiene los detalles de las 
#     acciones realizadas, tales como la tabla afectada, el evento, la sentencia ejecutada, el ID del registro, el usuario 
#     responsable, la fecha y la hora del evento.
#
#     Parámetros:
#     - request: Solicitud HTTP recibida. Solo admite el método GET.
#
#     Respuesta:
#     - En caso de éxito:
#         Retorna un diccionario en formato JSON con la siguiente estructura:
#         {
#             "code": 200,
#             "status": "success",
#             "message": "Registros de auditoría obtenidos correctamente",
#             "message_user": "Registros de auditoría obtenidos correctamente",
#             "data": [
#                 {
#                     "id": <id_auditoria>,
#                     "tabla": <tabla_afectada>,
#                     "evento": <evento>,
#                     "sentencia": <sentencia_sql>,
#                     "registro_id": <id_registro>,
#                     "usuario": <usuario_responsable>,
#                     "fecha": <fecha_evento>,
#                     "hora": <hora_evento>
#                 }
#             ]
#         }
#
#     - En caso de error:
#         Si ocurre un error en la base de datos, se captura una excepción DatabaseError y se registra un mensaje de error en el log.
#         La respuesta será un mensaje de error con un código 500:
#         {
#             "mensaje": "Error al listar los registros de auditoría."
#         }
#
#     Funcionalidad adicional:
#     - Usa transacciones atómicas para asegurar que todas las operaciones sean consistentes.
#     - Serializa manualmente los datos obtenidos del cursor SQL utilizando el serializer 'AuditoriaSerializer'.
#     - Si no se encuentran registros, retorna un mensaje de error con código 400 y un arreglo vacío en la clave 'data'.
"""
@api_view(["GET"])
@transaction.atomic
def listar_auditoria(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Audit system not found",
        "message_user": "Auditoría no encontrada",
        "data": [],
    }
    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                # Consulta SQL personalizada
                cursor.execute(
                    """
                    SELECT id, tabla, evento, sentencia, registro_id, usuario, 
                            fecha,
                            TO_CHAR(hora, 'HH24:MI:SS') as hora
                    FROM auditoria
                    ORDER BY id DESC
                """
                )

                # Obtener todos los registros
                auditorias = cursor.fetchall()

                # Formato del resultado
                auditoria_data = [
                    {
                        "id": row[0],
                        "tabla": row[1],
                        "evento": row[2],
                        "sentencia": row[3],
                        "registro_id": row[4],
                        "usuario": row[5],
                        "fecha": row[6],
                        "hora": row[7],
                    }
                    for row in auditorias
                ]

            # Serialización manual de los datos
            auditoria_serializer = AuditoriaSerializer(auditoria_data, many=True)

            dic_response["data"] = auditoria_serializer.data
            dic_response["code"] = 200
            dic_response["status"] = "success"
            dic_response["message_user"] = (
                "Registros de auditoría obtenidos correctamente"
            )
            dic_response["message"] = "Registros de auditoría obtenidos correctamente"
            return Response(dic_response, status=status.HTTP_200_OK)

        except DatabaseError as e:
            logger.error(f"Error al listar los registros de auditoría: {str(e)}")
            return Response(
                {"mensaje": "Error al listar los registros de auditoría."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return Response([], status=status.HTTP_200_OK)


@api_view(["GET"])
@transaction.atomic
def listar_auditoria_pordia(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Audit system not found",
        "message_user": "Auditoría no encontrada",
        "data": [],
    }
    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                # Consulta SQL personalizada para contar eventos por tipo y día
                cursor.execute(
                    """
                    SELECT 
                        SUM(CASE WHEN LOWER(evento) = 'crear' THEN 1 ELSE 0 END) AS creaciones,
                        SUM(CASE WHEN LOWER(evento) = 'actualizar' THEN 1 ELSE 0 END) AS actualizaciones,
                        SUM(CASE WHEN LOWER(evento) = 'eliminar' THEN 1 ELSE 0 END) AS eliminaciones,
                        CURRENT_DATE AS fecha_actual
                    FROM auditoria
                    WHERE fecha = CURRENT_DATE
                    """
                )

                # Obtener los resultados
                resultados = cursor.fetchone()
                print(resultados)  # Debugging line

                dic_response["data"] = {
                    "creaciones": resultados[0],
                    "actualizaciones": resultados[1],
                    "eliminaciones": resultados[2],
                    "fecha_actual": resultados[3],
                }
                dic_response["code"] = 200
                dic_response["status"] = "success"
                dic_response["message_user"] = "Registros de auditoría obtenidos correctamente"
                dic_response["message"] = "Registros de auditoría obtenidos correctamente"
                return Response(dic_response, status=status.HTTP_200_OK)

        except DatabaseError as e:
            logger.error(f"Error al listar los registros de auditoría: {str(e)}")
            return Response(
                {"mensaje": "Error al listar los registros de auditoría."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return Response([], status=status.HTTP_200_OK)

# ------------------------------------------------------ CRUD PAISES (TERMINADO SERIALIZER Y CURSOR) -----------------------------------------------------------
@api_view(["GET"])
@transaction.atomic
def listar_paises(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Countries system not found",
        "message_user": "Paises no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT p.id, p.nombre, p.abreviatura, 
                        TO_CHAR(p.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(p.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE WHEN p.estado_id = 3 THEN 'Eliminado'
                                WHEN p.estado_id = 2 THEN 'Inactivo'
                                ELSE 'Activo' 
                        END as estado_nombre
                    FROM pais p
                    WHERE p.estado_id <> 3
                    ORDER BY p.id DESC
                """) ##paginado por reportes 
            
                paises = cursor.fetchall()
                paises_serializados = [
                    {**PaisSerializer(Pais(
                        id=p[0], nombre=p[1], abreviatura=p[2],
                        fecha_creacion=p[3], fecha_modificacion=p[4]
                    )).data, 'estado': p[5]} for p in paises
                ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Paises obtenidos correctamente",
                "message": "Paises obtenidos correctamente",
                "data": paises_serializados,
            })
            return JsonResponse(dic_response, status=200, safe=False)

        except DatabaseError as e:
            logger.error(f"Error al listar los paises: {str(e)}")
            return JsonResponse({"mensaje": "Error al listar los paises."}, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@transaction.atomic
def crear_pais(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error creating country",
        "message_user": "Error al crear el país",
        "data": [],
    }
    
    if request.method == 'POST':
        try:
            # Deserialize request data using the serializer
            serializer = PaisSerializer(data=request.data)
            if not serializer.is_valid():
                return JsonResponse({"message": "Datos inválidos.", "data": serializer.errors}, status=400)
            
            nombre = serializer.validated_data["nombre"]
            abreviatura = serializer.validated_data["abreviatura"]
            estado_id = 1
            fecha_actual = datetime.now()
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                    estado_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM Pais WHERE (nombre = %s OR abreviatura = %s) AND estado_id IN (1, 2)",
                    [nombre, abreviatura]
                    )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe un país con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)
            
    
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Pais (nombre, abreviatura, estado_id, fecha_creacion, fecha_modificacion) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                    [nombre, abreviatura, estado_id, fecha_actual, fecha_actual]
                )
                pais_id = cursor.fetchone()[0]

            Auditoria.registrar_evento(
                tabla="País", evento="Crear",
                sentencia=f"País creada: {nombre} - {abreviatura} - {estado_nombre}", registro_id=pais_id,
                usuario="Anonimo"
            )

            dic_response.update({
                "code": 201,
                "status": "success",
                "message_user": "País creado exitosamente",
                "message": "País saved successfully",
                "data": {"id": pais_id, "nombre": nombre, "abreviatura": abreviatura, "estado": estado_nombre},
            })
            logger.info(f"País creado: nombre '{nombre}' - abreviatura '{abreviatura}' - estado '{estado_nombre}' (ID: {pais_id})")
            return JsonResponse(dic_response, status=201)

        except Exception as e:
            logger.error(f"Error inesperado al crear el País: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
    
    return Response([], status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@transaction.atomic
def actualizar_pais(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error updating country",
        "message_user": "Error al actualizar el país",
        "data": [],
    }

    if request.method == "PUT":
        try:
            paises_data = json.loads(request.body)

            serializer = PaisSerializer(data=paises_data, partial=True)
            if not serializer.is_valid():
                return JsonResponse({"message_user": "Datos inválidos.", "data": serializer.errors}, status=400)

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Pais WHERE id = %s", [id])         
                if cursor.fetchone()[0] == 0:
                    return JsonResponse({"message_user": "El país no existe."}, status=400)

            # Verificar duplicado de nombre y abreviatura
            with connection.cursor() as cursor:
                cursor.execute(
                        """
                            SELECT COUNT(*) 
                            FROM Pais 
                            WHERE (nombre = %s OR abreviatura = %s) 
                            AND estado_id IN (1, 2)
                            AND id != %s  -- Excluir el registro actual del chequeo
                            """,
                        [serializer.validated_data["nombre"], serializer.validated_data["abreviatura"], id]
                )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe un país con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)

            validated_data = serializer.validated_data
            estado_id = validated_data.get("estado").id
            with connection.cursor() as cursor:
                cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                estado_nombre = cursor.fetchone()[0]
                
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Pais SET nombre=%s, abreviatura=%s, estado_id=%s, fecha_modificacion=%s WHERE id=%s",
                    [validated_data.get("nombre"), validated_data.get("abreviatura"),
                    validated_data.get("estado").id, datetime.now(), id]
                )

            # Registrar auditoría
            Auditoria.registrar_evento(
                tabla="País", evento="Actualizar",
                sentencia=f"País actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {estado_nombre}",
                registro_id=id, usuario="Anonimo"
            )

            dic_response.update({
                "code": 200, "status": "success",
                "message": "Country updated successfully",
                "message_user": "País actualizado exitosamente",
                "data": serializer.data,
            })

            logger.info(f"País actualizado: {validated_data['nombre']} - {validated_data['abreviatura']}  - {estado_nombre}(ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al actualizar el país: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)


@api_view(["PATCH"])
@transaction.atomic
def eliminar_pais(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error deleting country",
        "message_user": "Error al eliminar el país",
        "data": [],
    }

    if request.method == "PATCH":
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT estado_id FROM Pais WHERE id = %s", [id])
                resultado = cursor.fetchone()

            if not resultado:
                dic_response["message_user"] = " no encontrado."
                return JsonResponse(dic_response, status=404)

            if resultado[0] == 3:  # 3: Eliminado
                dic_response["message_user"] = "El país ya está eliminado."
                return JsonResponse(dic_response, status=400)

            # Actualizar el estado a 'Eliminado'
            fecha_modificacion = datetime.now()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Pais SET estado_id = 3, fecha_modificacion = %s WHERE id = %s",
                    [fecha_modificacion, id],
                )
                
            pais = Pais.objects.get(id=id)
            Auditoria.registrar_evento(
                tabla="País",
                evento="Eliminar",
                sentencia=f"Se eliminó lógicamente el país con id: {id}.",
                registro_id=id,
                usuario="Anonimo",  
            )

            serializer = PaisSerializer(pais)
            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "País eliminado lógicamente",
                    "message": "Country deleted logically",
                    "data": serializer.data,
                }
            )
        
            logger.info(f"País eliminado logicamente: (ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar el país: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)


# ------- PARA SELECCIONAR LOS ACTIVOS 
@api_view(["GET"])
@transaction.atomic
def listar_paises_activos(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "countries system not found",
        "message_user": "Países activos no encontrados",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    #"SELECT * FROM Pais WHERE estado_id <> 3 ORDER BY id DESC"
                    
                    """SELECT p.id, p.nombre, p.abreviatura, 
                            p.fecha_creacion, p.fecha_modificacion,
                            CASE
                                WHEN p.estado_id = 3 THEN 'Eliminado'
                                WHEN p.estado_id = 2 THEN 'Inactivo'
                                ELSE 'Activo'
                            END as estado_nombre
                    FROM Pais p
                    LEFT JOIN estado s ON p.estado_id = s.id
                    WHERE estado_id = 1
                    ORDER BY p.id DESC
                    """
                )
                paises = cursor.fetchall()

                # Serializa cada país usando el serializador
                paises_serializados = []
                for p in paises:
                    pais = Pais(
                        id=p[0],
                        nombre=p[1],
                        abreviatura=p[2],
                        fecha_creacion=p[3],
                        fecha_modificacion=p[4],
                        estado_id=p[5]
                    )
                    serializer = PaisSerializer(pais)
                    paises_serializados.append(serializer.data)

                dic_response["data"] = paises_serializados
                dic_response["code"] = 200
                dic_response["status"] = "success"
                dic_response["message_user"] = "Países obtenidos correctamente"
                dic_response["message"] = "Países obtenidos correctamente"
                return Response(dic_response, status=status.HTTP_200_OK)
        except Exception as e:  # Cambiado a Exception para capturar todos los errores
            logger.error(f"Error al listar los países: {str(e)}")
            return Response(
                {"mensaje": "Error al listar los países."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return Response(dic_response, status=status.HTTP_200_OK)



# ------------------------------------------------------ CRUD MONEDA (TERMINADO SERIALIZER Y CURSOR) -----------------------------------------------------------


@api_view(["GET"])
@transaction.atomic
def listar_monedas(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Monedas no encontradas",
        "message_user": "Monedas no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT m.id, m.nombre, m.abreviatura, 
                        TO_CHAR(m.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(m.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE WHEN m.estado_id = 3 THEN 'Eliminado'
                                WHEN m.estado_id = 2 THEN 'Inactivo'
                                ELSE 'Activo' 
                        END as estado_nombre
                    FROM moneda m
                    WHERE m.estado_id <> 3
                    ORDER BY m.id DESC
                """)
            
                monedas = cursor.fetchall()
                moneda_serializados = [
                    {**MonedaSerializer(Moneda(
                        id=m[0], nombre=m[1], abreviatura=m[2],
                        fecha_creacion=m[3], fecha_modificacion=m[4]
                    )).data, 'estado': m[5]} for m in monedas
                ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Monedas obtenidos correctamente",
                "message": "Monedas obtenidos correctamente",
                "data": moneda_serializados,
            })
            return JsonResponse(dic_response, status=200, safe=False)

        except DatabaseError as e:
            logger.error(f"Error al listar las monedas: {str(e)}")
            return JsonResponse({"mensaje": "Error al listar las monedas."}, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@transaction.atomic
def crear_moneda(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error creating currency",
        "message_user": "Error al crear la moneda",
        "data": [],
    }
    
    if request.method == 'POST':
        try:
            # Deserialize request data using the serializer
            serializer = MonedaSerializer(data=request.data)
            if not serializer.is_valid():
                return JsonResponse({"message": "Datos inválidos.", "data": serializer.errors}, status=400)
            
            nombre = serializer.validated_data["nombre"]
            abreviatura = serializer.validated_data["abreviatura"]
            estado_id = 1
            fecha_actual = datetime.now()
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                    estado_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM Moneda WHERE (nombre = %s OR abreviatura = %s) AND estado_id IN (1, 2)",
                    [nombre, abreviatura]
                    )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe una moneda con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)
            
    
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Moneda (nombre, abreviatura, estado_id, fecha_creacion, fecha_modificacion) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                    [nombre, abreviatura, estado_id, fecha_actual, fecha_actual]
                )
                moneda_id = cursor.fetchone()[0]

            Auditoria.registrar_evento(
                tabla="Moneda", evento="Crear",
                sentencia=f"Moneda creada: {nombre} - {abreviatura} - {estado_nombre}", registro_id=moneda_id,
                usuario="Anonimo"
            )

            dic_response.update({
                "code": 201,
                "status": "success",
                "message_user": "Moneda creado exitosamente",
                "message": "Moneda creado exitosamente",
                "data": {"id": moneda_id, "nombre": nombre, "abreviatura": abreviatura, "estado": estado_nombre},
            })
            logger.info(f"Moneda creado: nombre '{nombre}' - abreviatura '{abreviatura} - estado '{estado_nombre}' (ID: {moneda_id})")
            return JsonResponse(dic_response, status=201)

        except Exception as e:
            logger.error(f"Error inesperado al crear la moneda: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
    
    return Response([], status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@transaction.atomic
def actualizar_moneda(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error updating currency",
        "message_user": "Error al actualizar la moneda",
        "data": [],
    }

    if request.method == "PUT":
        try:
            moneda_data = json.loads(request.body)

            serializer = MonedaSerializer(data=moneda_data, partial=True)
            if not serializer.is_valid():
                return JsonResponse({"message_user": "Datos inválidos.", "data": serializer.errors}, status=400)

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Moneda WHERE id = %s", [id])         
                if cursor.fetchone()[0] == 0:
                    return JsonResponse({"message_user": "La moneda no existe."}, status=400)

            # Verificar duplicado de nombre y abreviatura
            with connection.cursor() as cursor:
                cursor.execute(
                        """
                            SELECT COUNT(*) 
                            FROM Moneda 
                            WHERE (nombre = %s OR abreviatura = %s) 
                            AND estado_id IN (1, 2)
                            AND id != %s  -- Excluir el registro actual del chequeo
                            """,
                        [serializer.validated_data["nombre"], serializer.validated_data["abreviatura"], id]
                )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe una moneda con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)

            validated_data = serializer.validated_data
            
            estado_id = validated_data.get("estado").id
            with connection.cursor() as cursor:
                cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                estado_nombre = cursor.fetchone()[0]
                
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Moneda SET nombre=%s, abreviatura=%s, estado_id=%s, fecha_modificacion=%s WHERE id=%s",
                    [validated_data.get("nombre"), validated_data.get("abreviatura"),
                    validated_data.get("estado").id, datetime.now(), id]
                )

            # Registrar auditoría
            Auditoria.registrar_evento(
                tabla="Moneda", evento="Actualizar",
                sentencia=f"Moneda actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {estado_nombre}",
                registro_id=id, usuario="Anonimo"
            )

            dic_response.update({
                "code": 200, "status": "success",
                "message": "Currency updated successfully",
                "message_user": "Moneda actualizado exitosamente",
                "data": serializer.data,
            })

            logger.info(f"Moneda actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {estado_nombre}(ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al actualizar la moneda: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)


@api_view(["PATCH"])
@transaction.atomic
def eliminar_moneda(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error deleting currency",
        "message_user": "Error al eliminar la moneda",
        "data": [],
    }

    if request.method == "PATCH":
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT estado_id FROM Moneda WHERE id = %s", [id])
                resultado = cursor.fetchone()

            if not resultado:
                dic_response["message_user"] = "Moneda no encontrado."
                return JsonResponse(dic_response, status=404)

            if resultado[0] == 3:  # 3: Eliminado
                dic_response["message_user"] = "La moneda ya está eliminado."
                return JsonResponse(dic_response, status=400)

            # Actualizar el estado a 'Eliminado'
            fecha_modificacion = datetime.now()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Moneda SET estado_id = 3, fecha_modificacion = %s WHERE id = %s",
                    [fecha_modificacion, id],
                )
                
            moneda = Moneda.objects.get(id=id)
            Auditoria.registrar_evento(
                tabla="Moneda",
                evento="Eliminar",
                sentencia=f"Se eliminó lógicamente la moneda con id: {id}.",
                registro_id=id,
                usuario="Anonimo",  
            )

            serializer = MonedaSerializer(moneda)
            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Moneda eliminado lógicamente",
                    "message": "Moneda eliminado lógicamente",
                    "data": serializer.data,
                }
            )
        
            logger.info(f"Moneda eliminado logicamente: (ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar la moneda: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)

# ------- PARA SELECCIONAR LOS ACTIVOS 
@api_view(["GET"])
@transaction.atomic
def listar_monedas_activas(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "money active system not found",
        "message_user": "Monedas activas no encontradas",
        "data": [],
    }
    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                
                #"SELECT * FROM Moneda WHERE estado_id <> 3 ORDER BY id DESC"
                """
                    SELECT m.id, m.nombre, m.abreviatura, 
                            m.fecha_creacion, m.fecha_modificacion,
                            CASE
                                WHEN m.estado_id = 3 THEN 'Eliminado'
                                WHEN m.estado_id = 2 THEN 'Inactivo'
                                ELSE 'Activo'
                            END as estado_nombre
                    FROM Moneda m
                    LEFT JOIN estado s ON m.estado_id = s.id
                    WHERE estado_id = 1
                    ORDER BY m.id DESC
                    """
                cursor.execute("""
                    SELECT * FROM Moneda WHERE estado_id = 1 ORDER BY id DESC
                    """
                )
                monedas = cursor.fetchall()
                
                # Serializa cada país usando el serializador
                moneda_serializados = []
                for m in monedas:
                    moneda = Moneda(
                        id=m[0],
                        nombre=m[1],
                        abreviatura=m[2],
                        fecha_creacion=m[3],
                        fecha_modificacion=m[4],
                        estado_id=m[5],
                    )
                    serializer = MonedaSerializer(moneda)
                    moneda_serializados.append(serializer.data)

                dic_response["data"] = moneda_serializados
                dic_response["code"] = 200
                dic_response["status"] = "success"
                dic_response["message_user"] = "Monedas obtenidos correctamente"
                dic_response["message"] = "Monedas obtenidos correctamente"
                return Response(dic_response, status=status.HTTP_200_OK)
        except Exception as e:  # Cambiado a Exception para capturar todos los errores
            logger.error(f"Error al listar las monedas: {str(e)}")
            return Response(
                {"mensaje": "Error al listar las monedas."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return Response(dic_response, status=status.HTTP_200_OK)


# ------------------------------------------------------ CRUD EMPRESA (TERMINADO SERIALIZER Y CURSOR) --------------------------------------------------------
@api_view(["GET"])
@transaction.atomic
def listar_empresas(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Company system not found",
        "message_user": "Empresas no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
        # Ejecutar la consulta SQL para obtener las empresas
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT e.id, e.nombre, e.abreviatura, e.ruc, 
                        p.nombre as pais_nombre, m.nombre as moneda_nombre, 
                        TO_CHAR(e.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(e.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE 
                            WHEN e.estado_id = 3 THEN 'Eliminado'
                            WHEN e.estado_id = 2 THEN 'Inactivo'
                            ELSE 'Activo'
                        END as estado_nombre
                    FROM empresa e
                    LEFT JOIN pais p ON e.pais_id = p.id
                    LEFT JOIN moneda m ON e.moneda_id = m.id
                    WHERE e.estado_id <> 3
                    ORDER BY e.id DESC
                """)
                empresas = cursor.fetchall()

            # Serializar las empresas obtenidas
            empresas_serializadas = [
                {
                    "id": e[0], "nombre": e[1], "abreviatura": e[2], "ruc": e[3],
                    "pais": e[4], "moneda": e[5], "fecha_creacion": e[6],
                    "fecha_modificacion": e[7], "estado": e[8]
                } for e in empresas
            ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Empresas obtenidas correctamente",
                "message": "Empresas obtenidas correctamente",
                "data": empresas_serializadas
            })
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(f"Error al listar las empresas: {str(e)}")
            dic_response.update({"message": "Error al listar las empresas", "data": str(e)})
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@transaction.atomic
def crear_empresa(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error creating company",
        "message_user": "Error al crear la empresa",
        "data": None,
    }
    
    if request.method == 'POST':
        try:
            # Deserialize request data using the serializer
            serializer = EmpresaSerializer(data=request.data)
            if serializer.is_valid():
                nombre = serializer.validated_data["nombre"]
                abreviatura = serializer.validated_data["abreviatura"]
                ruc = serializer.validated_data["ruc"]
                pais_id = serializer.validated_data["pais"].id
                moneda_id = serializer.validated_data["moneda"].id
                estado_id = 1
                fecha_creacion = datetime.now()
                fecha_modificacion = datetime.now()

                # Obtener el nombre del país antes de la inserción
                with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Pais WHERE id = %s", [pais_id])
                    pais_nombre = cursor.fetchone()[0]
                
                with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Moneda WHERE id = %s", [moneda_id])
                    moneda_nombre = cursor.fetchone()[0]
                
                with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                    estado_nombre = cursor.fetchone()[0]
                
                # Check if the company already exists
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*) FROM Empresa WHERE (nombre = %s OR abreviatura = %s OR ruc = %s) AND estado_id IN (1, 2)",
                        [nombre, abreviatura, ruc],
                    )
                    if cursor.fetchone()[0] > 0:
                        return JsonResponse({"message_user": "Ya existe una empresa con el mismo nombre, abreviatura o ruc", "message": "Ya hay un dato existente."}, status=400)

                # Insertar la empresa en la base de datos
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO Empresa (nombre, abreviatura, ruc, pais_id, moneda_id, estado_id, fecha_creacion, fecha_modificacion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                        [nombre, abreviatura, ruc, pais_id, moneda_id, estado_id, fecha_creacion, fecha_modificacion]  
                    )
                    empresa_id = cursor.fetchone()[0]

                # Registrar el evento de auditoría usando el nombre del país
                Auditoria.registrar_evento(
                    tabla="Empresa",
                    evento="Crear",
                    sentencia=f"Empresa creada: {nombre} - {abreviatura} - {ruc} - {pais_nombre} - {moneda_nombre} - {estado_nombre}",
                    registro_id=empresa_id,
                    usuario="Anonimo", 
                )
                
                dic_response.update(
                    {
                        "code": 201,
                        "status": "success",
                        "message_user": "Empresa creada exitosamente",
                        "message": "Company saved successfully",
                        "data": {"id": empresa_id, "nombre": nombre, "abreviatura": abreviatura, "estado": estado_nombre    },
                    }
                )
                logger.info(f"Empresa creada exitosamente: {nombre} - abreviatura '{abreviatura}' (ID: {empresa_id})")
                return JsonResponse(dic_response, status=201)

            else:
                dic_response["message"] = "Datos inválidos."
                dic_response["data"] = serializer.errors
                return JsonResponse(dic_response, status=400)

        except Exception as e:
            logger.error(f"Error inesperado al crear la Empresa: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
    
    return Response(dic_response, status=status.HTTP_200_OK)


@api_view(["PUT"])
@transaction.atomic
def actualizar_empresa(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error updating company",
        "message_user": "Error al actualizar la empresa",
        "data": [],
    }

    if request.method == "PUT":
        try:
            empresa_data = json.loads(request.body)

            # Validar y convertir país y moneda a IDs
            for field, model, error_msg in [('pais', Pais, 'País no encontrado'), ('moneda', Moneda, 'Moneda no encontrada')]:
                if isinstance(empresa_data.get(field), str):
                    obj = model.objects.filter(nombre=empresa_data[field]).first()
                    if obj:
                        empresa_data[field] = obj.id
                    else:
                        dic_response["message"] = f"{field.capitalize()} inválido."
                        dic_response["data"] = {field: error_msg}
                        return JsonResponse(dic_response, status=400)

            # Serializar y validar los datos
            serializer = EmpresaSerializer(data=empresa_data, partial=True)
            if not serializer.is_valid():
                dic_response.update({"message_user": "Datos inválidos.", "data": serializer.errors})
                return JsonResponse(dic_response, status=400)

            # Verificar existencia de la empresa
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Empresa WHERE id = %s", [id])
                if cursor.fetchone()[0] == 0:
                    dic_response["message_user"] = "La Empresa no existe."
                    return JsonResponse(dic_response, status=400)

            # Verificar si ya existe otra empresa con el mismo nombre, abreviatura o RUC
            with connection.cursor() as cursor:
                cursor.execute(
                    """ SELECT COUNT(*) FROM Empresa 
                        WHERE (nombre = %s OR abreviatura = %s OR ruc = %s) 
                        AND estado_id IN (1, 2)
                        AND id != %s""",
                    [serializer.validated_data["nombre"], serializer.validated_data["abreviatura"], serializer.validated_data["ruc"], id]
                )
                if cursor.fetchone()[0] > 0:
                        return JsonResponse({"message_user": "Ya existe una empresa con el mismo nombre, abreviatura o RUC.", "message": "Ya hay un dato existente."}, status=400)

            # Actualizar empresa
            
            validated_data = serializer.validated_data
            pais_id = validated_data.get("pais").id
            moneda_id = validated_data.get("moneda").id
            estado_id = validated_data.get("estado").id
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Pais WHERE id = %s", [pais_id])
                    pais_nombre = cursor.fetchone()[0]
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Moneda WHERE id = %s", [moneda_id])
                    moneda_nombre = cursor.fetchone()[0]
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                    estado_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE Empresa SET nombre = %s, abreviatura = %s, ruc = %s, pais_id = %s, 
                        moneda_id = %s, estado_id = %s, fecha_modificacion = %s WHERE id = %s""",
                    [
                        serializer.validated_data["nombre"], serializer.validated_data["abreviatura"],
                        serializer.validated_data["ruc"], serializer.validated_data["pais"].id,
                        serializer.validated_data["moneda"].id, serializer.validated_data["estado"].id,
                        datetime.now(), id
                    ],
                )

            # Registrar auditoría
            Auditoria.registrar_evento(
                tabla="Empresa", evento="Actualizar", 
                sentencia=f"Empresa actualizada: {serializer.validated_data['nombre']} - {serializer.validated_data['abreviatura']} - {serializer.validated_data['ruc']} - {pais_nombre} - {moneda_nombre} - {estado_nombre}",
                registro_id=id, usuario="Anonimo"
            )

            dic_response.update({
                "code": 200,
                "status": "success",
                "message": "Company updated successfully",
                "message_user": "Empresa actualizada exitosamente",
                "data": serializer.data
            })
            
            logger.info(f"Empresa actualizada: {validated_data['nombre']} - {validated_data['abreviatura']} - {validated_data['ruc']} - {pais_nombre} - {moneda_nombre} - {estado_nombre} (ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            dic_response.update({"message_user": "Error inesperado", "data": {"error": str(e)}})
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)

@api_view(["PATCH"])
@transaction.atomic
def eliminar_empresa(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error deleting company",
        "message_user": "Error al eliminar la empresa",
        "data": [],
    }

    if request.method == "PATCH":
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT estado_id FROM Empresa WHERE id = %s", [id])
                resultado = cursor.fetchone()

                if not resultado:
                    dic_response["message"] = "Empresa no encontrada."
                    return JsonResponse(dic_response, status=404)

                if resultado[0] == 3:  # Estado "Eliminado"
                    dic_response["message"] = "La Empresa ya está eliminada."
                    return JsonResponse(dic_response, status=400)

                # Actualizar estado a "Eliminado"
                cursor.execute("UPDATE Empresa SET estado_id = 3, fecha_modificacion = %s WHERE id = %s", [datetime.now(), id])

            empresa = Empresa.objects.get(id=id)

            Auditoria.registrar_evento(
                tabla="Empresa",
                evento="Eliminar",
                sentencia=f"Se eliminó lógicamente la empresa con id: {id}.",
                registro_id=id,
                usuario="Anonimo",  # Aquí puedes pasar el usuario real si está disponible
            )

            serializer = EmpresaSerializer(empresa)
            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Empresa eliminada lógicamente",
                "message": "Company deleted logically",
                "data": serializer.data,
            })

            logger.info(f"Empresa eliminada lógicamente: ID {id}")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar la empresa: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)

# ------- PARA SELECCIONAR LOS ACTIVOS 
@api_view(["GET"])
@transaction.atomic
def listar_empresas_activas(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Company active system not found",
        "message_user": "Empresas Activas no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
        # Ejecutar la consulta SQL para obtener las empresas
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT e.id, e.nombre, e.abreviatura, e.ruc, 
                        p.nombre as pais_nombre, m.nombre as moneda_nombre, 
                        TO_CHAR(e.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(e.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE 
                            WHEN e.estado_id = 3 THEN 'Eliminado'
                            WHEN e.estado_id = 2 THEN 'Inactivo'
                            ELSE 'Activo'
                        END as estado_nombre
                    FROM empresa e
                    LEFT JOIN pais p ON e.pais_id = p.id
                    LEFT JOIN moneda m ON e.moneda_id = m.id
                    WHERE e.estado_id = 1
                    ORDER BY e.id DESC
                """)
                empresas = cursor.fetchall()

            # Serializar las empresas obtenidas
            empresas_serializadas = [
                {
                    "id": e[0], "nombre": e[1], "abreviatura": e[2], "ruc": e[3],
                    "pais": e[4], "moneda": e[5], "fecha_creacion": e[6],
                    "fecha_modificacion": e[7], "estado": e[8]
                } for e in empresas
            ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Empresas activas obtenidas correctamente",
                "message": "Empresas activas obtenidas correctamente",
                "data": empresas_serializadas
            })
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(f"Error al listar las empresas activas: {str(e)}")
            dic_response.update({"message": "Error al listar las empresas activas", "data": str(e)})
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------ CRUD DEPARTAMENTO (TERMINADO SERIALIZER Y CURSOR) -----------------------------------------------------------


@api_view(["GET"])
@transaction.atomic
def listar_departamentos(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Departamento system not found",
        "message_user": "Departamento no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT d.id, d.nombre, d.abreviatura, 
                        p.nombre as pais_nombre, 
                        TO_CHAR(d.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(d.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE WHEN d.estado_id = 3 THEN 'Eliminado'
                                WHEN d.estado_id = 2 THEN 'Inactivo'
                                ELSE 'Activo' 
                        END as estado_nombre
                    FROM departamento d
                    LEFT JOIN pais p ON d.pais_id = p.id
                    WHERE d.estado_id <> 3
                    ORDER BY d.id DESC
                """)
            
                departamentos = cursor.fetchall()
                departamento_serializados = [
                    {**DepartamentoSerializer(Departamento(
                        id=d[0], nombre=d[1], abreviatura=d[2], pais_id=d[3],
                        fecha_creacion=d[4], fecha_modificacion=d[5]
                    )).data, 'estado': d[6]} for d in departamentos
                ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Departamentos obtenidos correctamente",
                "message": "Departamentos obtenidos correctamente",
                "data": departamento_serializados,
            })
            return JsonResponse(dic_response, status=200, safe=False)

        except DatabaseError as e:
            logger.error(f"Error al listar los departamentos: {str(e)}")
            return JsonResponse({"mensaje": "Error al listar los departamentos."}, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@transaction.atomic
def crear_departamento(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error creating department",
        "message_user": "Error al crear el departamento",
        "data": None,
    }
    
    if request.method == 'POST':
        try:
            # Deserialize request data using the serializer
            serializer = DepartamentoSerializer(data=request.data)
            if not serializer.is_valid():
                return JsonResponse({"message": "Datos inválidos.", "data": serializer.errors}, status=400)
            
            nombre = serializer.validated_data["nombre"]
            abreviatura = serializer.validated_data["abreviatura"]
            pais_id = serializer.validated_data["pais"].id
            estado_id = 1
            fecha_actual = datetime.now()
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT nombre FROM Pais WHERE id = %s", [pais_id])
                pais_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                estado_nombre = cursor.fetchone()[0]
                    
            # Verificar si el departamento ya existe
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM Departamento WHERE (nombre = %s OR abreviatura = %s) AND estado_id IN (1, 2)",
                    [nombre, abreviatura]
                )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe una departamento con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)

            # Insertar nuevo departamento
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Departamento (nombre, abreviatura, pais_id, estado_id, fecha_creacion, fecha_modificacion) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                    [nombre, abreviatura, pais_id, estado_id, fecha_actual, fecha_actual]
                )
                departamento_id = cursor.fetchone()[0]

            Auditoria.registrar_evento(
                tabla="Departamento", 
                evento="Crear",
                sentencia=f"Departamento creada: {nombre} - {abreviatura} - {pais_nombre} - {estado_nombre}", 
                registro_id=departamento_id,
                usuario="Anonimo"
            )

            dic_response.update({
                "code": 201,
                "status": "success",
                "message_user": "Departamento creado exitosamente",
                "message": "Department saved successfully",
                "data": {"id": departamento_id, "nombre": nombre, "abreviatura": abreviatura, "pais":pais_nombre, "estado": estado_nombre},
            })
            logger.info(f"Departamento creado: nombre '{nombre}' - abreviatura '{abreviatura}' - pais '{pais_nombre}' - estado '{estado_nombre}' (ID: {departamento_id})")
            return JsonResponse(dic_response, status=201)

        except Exception as e:
            logger.error(f"Error inesperado al crear el departamento: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
    
    return Response(dic_response, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@transaction.atomic
def actualizar_departamento(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error updating department",
        "message_user": "Error al actualizar el departamento",
        "data": [],
    }

    if request.method == "PUT":
        try:
            departamento_data = json.loads(request.body)

            # Validar y asignar país
            if isinstance(departamento_data.get('pais'), str):
                pais_obj = Pais.objects.filter(nombre=departamento_data['pais']).first()
                if not pais_obj:
                    return JsonResponse({"message_user": "País inválido.", "data": {"pais": "País no encontrado."}}, status=400)
                departamento_data['pais'] = pais_obj.id

            serializer = DepartamentoSerializer(data=departamento_data, partial=True)
            if not serializer.is_valid():
                return JsonResponse({"message_user": "Datos inválidos.", "data": serializer.errors}, status=400)

            # Verificar existencia del departamento
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Departamento WHERE id = %s", [id])
                if cursor.fetchone()[0] == 0:
                    return JsonResponse({"message_user": "El departamento no existe."}, status=400)
            
            # Verificar duplicado de nombre y abreviatura
            with connection.cursor() as cursor:
                cursor.execute(
                    """ SELECT COUNT(*) FROM Departamento WHERE (nombre = %s OR abreviatura = %s) AND estado_id IN (1, 2) AND id != %s""",
                    [serializer.validated_data["nombre"], serializer.validated_data["abreviatura"], id]
                )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe una departamento con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)

            
            # Actualizar departamento
            validated_data = serializer.validated_data
            pais_id = validated_data.get("pais").id
            estado_id = validated_data.get("estado").id
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Pais WHERE id = %s", [pais_id])
                    pais_nombre = cursor.fetchone()[0]
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                    estado_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Departamento SET nombre=%s, abreviatura=%s, pais_id=%s, estado_id=%s, fecha_modificacion=%s WHERE id=%s",
                    [validated_data.get("nombre"), validated_data.get("abreviatura"), validated_data.get("pais").id,
                    validated_data.get("estado").id, datetime.now(), id]
                )

            # Registrar auditoría
            Auditoria.registrar_evento(
                tabla="Departamento", evento="Actualizar",
                sentencia=f"Departamento actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {pais_nombre} - {estado_nombre}",
                registro_id=id, usuario="Anonimo"
            )

            dic_response.update({
                "code": 200, "status": "success",
                "message": "Department updated successfully",
                "message_user": "Departamento actualizado exitosamente",
                "data": serializer.data,
            })

            logger.info(f"Departamento actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {pais_nombre} - {estado_nombre} (ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            return JsonResponse({"message": "Error inesperado"}, status=500)

    return JsonResponse([], status=200)

@api_view(["PATCH"])
@transaction.atomic
def eliminar_departamento(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error deleting department",
        "message_user": "Error al eliminar el departamento",
        "data": [],
    }

    if request.method == "PATCH":
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT estado_id FROM Departamento WHERE id = %s", [id])
                resultado = cursor.fetchone()

            if not resultado:
                dic_response["message"] = "Departamento no encontrado."
                return JsonResponse(dic_response, status=404)

            if resultado[0] == 3:  # 3: Eliminado
                dic_response["message"] = "El departamento ya está eliminado."
                return JsonResponse(dic_response, status=400)

            # Actualizar el estado a 'Eliminado'
            fecha_modificacion = datetime.now()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Departamento SET estado_id = 3, fecha_modificacion = %s WHERE id = %s",
                    [fecha_modificacion, id],
                )

            # Registrar auditoría y serializar el departamento actualizado
            departamento = Departamento.objects.get(id=id)
            Auditoria.registrar_evento(
                tabla="Departamento",
                evento="Eliminar",
                sentencia=f"Se eliminó lógicamente el departamento con id: {id}.",
                registro_id=id,
                usuario="Anonimo",  # Reemplazar con el usuario actual si está disponible
            )

            serializer = DepartamentoSerializer(departamento)
            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Departamento eliminado lógicamente",
                    "message": "Department deleted logically",
                    "data": serializer.data,
                }
            )
        
            logger.info(f"Departamento eliminado logicamente: (ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar el departamento: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)

# ------- PARA SELECCIONAR LOS ACTIVOS 
@api_view(["GET"])
@transaction.atomic
def listar_departamentos_activos(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Department actives system not found",
        "message_user": "Departamento activos no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT d.id, d.nombre, d.abreviatura, 
                        p.nombre as pais_nombre, 
                        TO_CHAR(d.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(d.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE WHEN d.estado_id = 3 THEN 'Eliminado'
                                WHEN d.estado_id = 2 THEN 'Inactivo'
                                ELSE 'Activo' 
                        END as estado_nombre
                    FROM departamento d
                    LEFT JOIN pais p ON d.pais_id = p.id
                    WHERE d.estado_id = 1
                    ORDER BY d.id DESC
                """)
            
                departamentos = cursor.fetchall()
                departamento_serializados = [
                    {**DepartamentoSerializer(Departamento(
                        id=d[0], nombre=d[1], abreviatura=d[2], pais_id=d[3],
                        fecha_creacion=d[4], fecha_modificacion=d[5]
                    )).data, 'estado': d[6]} for d in departamentos
                ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Departamentos activos obtenidos correctamente",
                "message": "Departamentos activos obtenidos correctamente",
                "data": departamento_serializados,
            })
            return JsonResponse(dic_response, status=200, safe=False)

        except DatabaseError as e:
            logger.error(f"Error al listar los departamentos activos: {str(e)}")
            return JsonResponse({"mensaje": "Error al listar los departamentos activos."}, status=500)

    return JsonResponse(dic_response, safe=False, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------ CRUD PROVINCIA (TERMINADO SERIALIZER Y CURSOR) -----------------------------------------------------------

@api_view(["GET"])
@transaction.atomic
def listar_provincias(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Provincie system not found",
        "message_user": "Provincia no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT p.id, p.nombre, p.abreviatura, 
                        d.nombre as departamento_nombre, 
                        TO_CHAR(p.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(p.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE WHEN p.estado_id = 3 THEN 'Eliminado'
                                WHEN p.estado_id = 2 THEN 'Inactivo'
                                ELSE 'Activo' 
                        END as estado_nombre
                    FROM provincia p
                    LEFT JOIN departamento d ON p.departamento_id = d.id
                    WHERE p.estado_id <> 3
                    ORDER BY p.id DESC
                """)
            
                provincias = cursor.fetchall()
                provincia_serializados = [
                    {**ProvinciaSerializer(Provincia(
                        id=p[0], nombre=p[1], abreviatura=p[2], departamento_id=p[3],
                        fecha_creacion=p[4], fecha_modificacion=p[5]
                    )).data, 'estado': p[6]} for p in provincias
                ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Provincias obtenidos correctamente",
                "message": "Provincias obtenidos correctamente",
                "data": provincia_serializados,
            })
            return JsonResponse(dic_response, status=200, safe=False)

        except DatabaseError as e:
            logger.error(f"Error al listar los departamentos: {str(e)}")
            return JsonResponse({"mensaje": "Error al listar los departamentos."}, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@transaction.atomic
def crear_provincia(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error creating province",
        "message_user": "Error al crear la provincia",
        "data": [],
    }
    
    if request.method == 'POST':
        try:
            # Deserialize request data using the serializer
            serializer = ProvinciaSerializer(data=request.data)
            if not serializer.is_valid():
                return JsonResponse({"message": "Datos inválidos.", "data": serializer.errors}, status=400)
            
            nombre = serializer.validated_data["nombre"]
            abreviatura = serializer.validated_data["abreviatura"]
            departamento_id = serializer.validated_data["departamento"].id
            estado_id = 1
            fecha_actual = datetime.now()
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT nombre FROM Departamento WHERE id = %s", [departamento_id])
                departamento_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                estado_nombre = cursor.fetchone()[0]
            # Verificar si el provincia ya existe
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM Provincia WHERE (nombre = %s OR abreviatura = %s) AND estado_id IN (1, 2)",
                    [nombre, abreviatura]
                )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe una provincia con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)
                
            # Insertar nueva provincia
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Provincia (nombre, abreviatura, departamento_id, estado_id, fecha_creacion, fecha_modificacion) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                    [nombre, abreviatura, departamento_id, estado_id, fecha_actual, fecha_actual]
                )
                provincia_id = cursor.fetchone()[0]

            Auditoria.registrar_evento(
                tabla="Provincia", evento="Crear",
                sentencia=f"Provincia creada: {nombre} - {abreviatura} - {departamento_nombre} - {estado_nombre}", registro_id=provincia_id,
                usuario="Anonimo"
            )

            dic_response.update({
                "code": 201,
                "status": "success",
                "message_user": "Provincia creado exitosamente",
                "message": "Province saved successfully",
                "data": {"id": provincia_id, "nombre": nombre, "abreviatura": abreviatura, "departamento":departamento_nombre, "estado": estado_nombre},
            })
            logger.info(f"Provincia creado: nombre '{nombre}' - abreviatura '{abreviatura}' (ID: {provincia_id})")
            return JsonResponse(dic_response, status=201)

        except Exception as e:
            logger.error(f"Error inesperado al crear la provincia: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
    
    return Response([], status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@transaction.atomic
def actualizar_provincia(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error updating province",
        "message_user": "Error al actualizar la provincia",
        "data": [],
    }

    if request.method == "PUT":
        try:
            provincia_data = json.loads(request.body)

            # Validar y asignar país
            if isinstance(provincia_data.get('departamento'), str):
                departamento_obj = Departamento.objects.filter(nombre=provincia_data['departamento']).first()
                if not departamento_obj:
                    return JsonResponse({"message": "Departamento inválido.", "data": {"departamento": "Departamento no encontrado."}}, status=400)
                provincia_data['departamento'] = departamento_obj.id

            serializer = ProvinciaSerializer(data=provincia_data, partial=True)
            if not serializer.is_valid():
                return JsonResponse({"message": "Datos inválidos.", "data": serializer.errors}, status=400)

            # Verificar existencia del provincia
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Provincia WHERE id = %s", [id])
                if cursor.fetchone()[0] == 0:
                    return JsonResponse({"message": "La provincia no existe."}, status=400)
            
            with connection.cursor() as cursor:
                cursor.execute(
                    """ 
                    SELECT COUNT(*) 
                    FROM Provincia 
                    WHERE (nombre = %s OR abreviatura = %s) 
                    AND estado_id IN (1, 2) 
                    AND id != %s
                    """,
                    [serializer.validated_data["nombre"], serializer.validated_data["abreviatura"], id]
                )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe una provincia con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)
            
            # Actualizar provincia
            validated_data = serializer.validated_data
            departamento_id = validated_data.get("departamento").id
            estado_id = validated_data.get("estado").id
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Departamento WHERE id = %s", [departamento_id])
                    departamento_nombre = cursor.fetchone()[0]
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                    estado_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Provincia SET nombre=%s, abreviatura=%s, departamento_id=%s, estado_id=%s, fecha_modificacion=%s WHERE id=%s",
                    [validated_data.get("nombre"), validated_data.get("abreviatura"), validated_data.get("departamento").id,
                    validated_data.get("estado").id, datetime.now(), id]
                )

            # Registrar auditoría
            Auditoria.registrar_evento(
                tabla="Provincia", evento="Actualizar",
                sentencia=f"Provincia actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {departamento_nombre} - {estado_nombre}",
                registro_id=id, usuario="Anonimo"
            )

            dic_response.update({
                "code": 200, "status": "success",
                "message": "Province updated successfully",
                "message_user": "Provincia actualizado exitosamente",
                "data": serializer.data,
            })

            logger.info(f"Provincia actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {departamento_nombre} - {estado_nombre}(ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al actualizar la provincia: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)


@api_view(["PATCH"])
@transaction.atomic
def eliminar_provincia(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error deleting province",
        "message_user": "Error al eliminar la provincia",
        "data": [],
    }

    if request.method == "PATCH":
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT estado_id FROM Provincia WHERE id = %s", [id])
                resultado = cursor.fetchone()

            if not resultado:
                dic_response["message"] = "Provincia no encontrado."
                return JsonResponse(dic_response, status=404)

            if resultado[0] == 3:  # 3: Eliminado
                dic_response["message"] = "El Provincia ya está eliminado."
                return JsonResponse(dic_response, status=400)

            # Actualizar el estado a 'Eliminado'
            fecha_modificacion = datetime.now()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Provincia SET estado_id = 3, fecha_modificacion = %s WHERE id = %s",
                    [fecha_modificacion, id],
                )

            # Registrar auditoría y serializar el departamento actualizado
            provincia = Provincia.objects.get(id=id)
            Auditoria.registrar_evento(
                tabla="Provincia",
                evento="Eliminar",
                sentencia=f"Se eliminó lógicamente el provincia con id: {id}.",
                registro_id=id,
                usuario="Anonimo",  # Reemplazar con el usuario actual si está disponible
            )

            serializer = ProvinciaSerializer(provincia)
            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Provincia eliminado lógicamente",
                    "message": "Province deleted logically",
                    "data": serializer.data,
                }
            )
        
            logger.info(f"Provincia eliminado logicamente: (ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar la Provincia: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)

# ------- PARA SELECCIONAR LOS ACTIVOS 
@api_view(["GET"])
@transaction.atomic
def listar_provincias_activas(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Provincie active system not found",
        "message_user": "Provincia activas no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT p.id, p.nombre, p.abreviatura, 
                        d.nombre as departamento_nombre, 
                        TO_CHAR(p.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(p.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE WHEN p.estado_id = 3 THEN 'Eliminado'
                                WHEN p.estado_id = 2 THEN 'Inactivo'
                                ELSE 'Activo' 
                        END as estado_nombre
                    FROM provincia p
                    LEFT JOIN departamento d ON p.departamento_id = d.id
                    WHERE p.estado_id = 1
                    ORDER BY p.id DESC
                """)
            
                provincias = cursor.fetchall()
                provincia_serializados = [
                    {**ProvinciaSerializer(Provincia(
                        id=p[0], nombre=p[1], abreviatura=p[2], departamento_id=p[3],
                        fecha_creacion=p[4], fecha_modificacion=p[5]
                    )).data, 'estado': p[6]} for p in provincias
                ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Provincia activas obtenidos correctamente",
                "message": "Provincia activas obtenidos correctamente",
                "data": provincia_serializados,
            })
            return JsonResponse(dic_response, status=200, safe=False)

        except DatabaseError as e:
            logger.error(f"Error al listar las provincias activas: {str(e)}")
            return JsonResponse({"mensaje": "Error al listar las provincias activas."}, status=500)

    return JsonResponse(dic_response, safe=False, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------ CRUD DISTRITO (TERMINADO SERIALIZER Y CURSOR) -----------------------------------------------------------


@api_view(["GET"])
@transaction.atomic
def listar_distritos(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "District system not found",
        "message_user": "District no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT d.id, d.nombre, d.abreviatura, 
                        p.nombre as provincia_nombre, 
                        TO_CHAR(d.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(d.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE WHEN d.estado_id = 3 THEN 'Eliminado'
                                WHEN d.estado_id = 2 THEN 'Inactivo'
                                ELSE 'Activo' 
                        END as estado_nombre
                    FROM distrito d
                    LEFT JOIN provincia p ON d.provincia_id = p.id
                    WHERE d.estado_id <> 3
                    ORDER BY d.id DESC
                """)
            
                distritos = cursor.fetchall()
                distrito_serializados = [
                    {**DistritoSerializer(Distrito(
                        id=p[0], nombre=p[1], abreviatura=p[2], provincia_id=p[3],
                        fecha_creacion=p[4], fecha_modificacion=p[5]
                    )).data, 'estado': p[6]} for p in distritos
                ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Distrito obtenidos correctamente",
                "message": "Distrito obtenidos correctamente",
                "data": distrito_serializados,
            })
            return JsonResponse(dic_response, status=200, safe=False)

        except DatabaseError as e:
            logger.error(f"Error al listar los distritos: {str(e)}")
            return JsonResponse({"mensaje": "Error al listar los distritos."}, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@transaction.atomic
def crear_distrito(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error creating district",
        "message_user": "Error al crear el distrito",
        "data": [],
    }
    
    if request.method == 'POST':
        try:
            # Deserialize request data using the serializer
            serializer = DistritoSerializer(data=request.data)
            if not serializer.is_valid():
                return JsonResponse({"message": "Datos inválidos.", "data": serializer.errors}, status=400)
            
            nombre = serializer.validated_data["nombre"]
            abreviatura = serializer.validated_data["abreviatura"]
            provincia_id = serializer.validated_data["provincia"].id
            estado_id = 1
            fecha_actual = datetime.now()
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT nombre FROM Provincia WHERE id = %s", [provincia_id])
                provincia_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                estado_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM Distrito WHERE (nombre = %s OR abreviatura = %s) AND estado_id IN (1, 2)",
                    [nombre, abreviatura]
                )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe un distrito con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Distrito (nombre, abreviatura, provincia_id, estado_id, fecha_creacion, fecha_modificacion) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                    [nombre, abreviatura, provincia_id, estado_id, fecha_actual, fecha_actual]
                )
                distrito_id = cursor.fetchone()[0]

            Auditoria.registrar_evento(
                tabla="Distrito", evento="Crear",
                sentencia=f"Distrito creada: {nombre} - {abreviatura} - {provincia_nombre} - {estado_nombre}", registro_id=distrito_id,
                usuario="Anonimo"
            )

            dic_response.update({
                "code": 201,
                "status": "success",
                "message_user": "Distrito creado exitosamente",
                "message": "Province saved successfully",
                "data": {"id": distrito_id, "nombre": nombre, "abreviatura": abreviatura, "provincia":provincia_nombre, "estado": estado_nombre},
            })
            logger.info(f"Distrito creado: nombre '{nombre}' - abreviatura '{abreviatura}' - provincia '{provincia_nombre}' - estado '{estado_nombre}'(ID: {distrito_id})")
            return JsonResponse(dic_response, status=201)

        except Exception as e:
            logger.error(f"Error inesperado al crear el distrito: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
    
    return Response([], status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@transaction.atomic
def actualizar_distrito(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error updating district",
        "message_user": "Error al actualizar el distrito",
        "data": [],
    }

    if request.method == "PUT":
        try:
            distrito_data = json.loads(request.body)

            if isinstance(distrito_data.get('provincia'), str):
                provincia_obj = Provincia.objects.filter(nombre=distrito_data['provincia']).first()
                if not provincia_obj:
                    return JsonResponse({"message": "Provincia inválido.", "data": {"provincia": "Provincia no encontrado."}}, status=400)
                distrito_data['provincia'] = provincia_obj.id

            serializer = DistritoSerializer(data=distrito_data, partial=True)
            if not serializer.is_valid():
                return JsonResponse({"message": "Datos inválidos.", "data": serializer.errors}, status=400)

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Distrito WHERE id = %s", [id])
                if cursor.fetchone()[0] == 0:
                    return JsonResponse({"message": "El Distrito no existe."}, status=400)
                
            # Verificar duplicado de nombre y abreviatura
            with connection.cursor() as cursor:
                cursor.execute(
                    """ SELECT COUNT(*) FROM Distrito WHERE (nombre = %s OR abreviatura = %s) AND estado_id IN (1, 2) AND id != %s""",
                    [serializer.validated_data["nombre"], serializer.validated_data["abreviatura"],id]
                )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe un distrito con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)

            # Actualizar provincia
            validated_data = serializer.validated_data
            provincia_id = validated_data.get("provincia").id
            estado_id = validated_data.get("estado").id
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Provincia WHERE id = %s", [provincia_id])
                    provincia_nombre = cursor.fetchone()[0]
    
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                    estado_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Distrito SET nombre=%s, abreviatura=%s, provincia_id=%s, estado_id=%s, fecha_modificacion=%s WHERE id=%s",
                    [validated_data.get("nombre"), validated_data.get("abreviatura"), validated_data.get("provincia").id,
                    validated_data.get("estado").id, datetime.now(), id]
                )

            # Registrar auditoría
            Auditoria.registrar_evento(
                tabla="Distrito", evento="Actualizar",
                sentencia=f"Distrito actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {provincia_nombre} - {estado_nombre}",
                registro_id=id, usuario="Anonimo"
            )

            dic_response.update({
                "code": 200, "status": "success",
                "message": "District updated successfully",
                "message_user": "Distrito actualizado exitosamente",
                "data": serializer.data,
            })

            logger.info(f"Distrito actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {provincia_nombre} - {estado_nombre}(ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al actualizar el distrito: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)

@api_view(["PATCH"])
@transaction.atomic
def eliminar_distrito(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error deleting district",
        "message_user": "Error al eliminar la distrito",
        "data": [],
    }

    if request.method == "PATCH":
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT estado_id FROM Distrito WHERE id = %s", [id])
                resultado = cursor.fetchone()

            if not resultado:
                dic_response["message"] = "Distrito no encontrado."
                return JsonResponse(dic_response, status=404)

            if resultado[0] == 3:  # 3: Eliminado
                dic_response["message"] = "El Distrito ya está eliminado."
                return JsonResponse(dic_response, status=400)

            # Actualizar el estado a 'Eliminado'
            fecha_modificacion = datetime.now()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Distrito SET estado_id = 3, fecha_modificacion = %s WHERE id = %s",
                    [fecha_modificacion, id],
                )

            # Registrar auditoría y serializar el departamento actualizado
            distrito = Distrito.objects.get(id=id)
            Auditoria.registrar_evento(
                tabla="Distrito",
                evento="Eliminar",
                sentencia=f"Se eliminó lógicamente el provincia con id: {id}.",
                registro_id=id,
                usuario="Anonimo",  # Reemplazar con el usuario actual si está disponible
            )

            serializer = DistritoSerializer(distrito)
            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Distrito eliminado lógicamente",
                    "message": "District deleted logically",
                    "data": serializer.data,
                }
            )
        
            logger.info(f"Distrito eliminado logicamente: (ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar el distrito: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)

# --------------------------------------------------- LOGISTICO -------------------------------------------------------
# ------------------------------------------------------ CRUD CENTRO -----------------------------------------------------------
@api_view(["GET"])
@transaction.atomic
def listar_centros(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Center system not found",
        "message_user": "Centros no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT c.id, c.nombre, c.abreviatura, 
                        e.nombre as empresa_nombre, 
                        TO_CHAR(c.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(c.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE WHEN c.estado_id = 3 THEN 'Eliminado'
                                WHEN c.estado_id = 2 THEN 'Inactivo'
                                ELSE 'Activo' 
                        END as estado_nombre
                    FROM centro c
                    LEFT JOIN empresa e ON c.empresa_id = e.id
                    WHERE c.estado_id <> 3
                    ORDER BY c.id DESC
                """)
            
                centros = cursor.fetchall()
                centro_serializados = [
                    {**CentroSerializer(Centro(
                        id=p[0], nombre=p[1], abreviatura=p[2], empresa_id=p[3],
                        fecha_creacion=p[4], fecha_modificacion=p[5]
                    )).data, 'estado': p[6]} for p in centros
                ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Centros obtenidos correctamente",
                "message": "Centros obtenidos correctamente",
                "data": centro_serializados,
            })
            return JsonResponse(dic_response, status=200, safe=False)

        except DatabaseError as e:
            logger.error(f"Error al listar los centros: {str(e)}")
            return JsonResponse({"mensaje": "Error al listar los centros."}, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@transaction.atomic
def crear_centro(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error creating center",
        "message_user": "Error al crear el centro",
        "data": [],
    }
    
    if request.method == 'POST':
        try:
            # Deserialize request data using the serializer
            serializer = CentroSerializer(data=request.data)
            if not serializer.is_valid():
                return JsonResponse({"message": "Datos inválidos.", "data": serializer.errors}, status=400)
            
            nombre = serializer.validated_data["nombre"]
            abreviatura = serializer.validated_data["abreviatura"]
            empresa_id = serializer.validated_data["empresa"].id
            estado_id = 1
            fecha_actual = datetime.now()
            
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT nombre FROM Empresa WHERE id = %s", [empresa_id])
                empresa_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                estado_nombre = cursor.fetchone()[0]
                    
                    
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM Centro WHERE (nombre = %s OR abreviatura = %s) AND estado_id IN (1, 2)",
                    [nombre, abreviatura]
                )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe un centro con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Centro (nombre, abreviatura, empresa_id, estado_id, fecha_creacion, fecha_modificacion) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                    [nombre, abreviatura, empresa_id, estado_id, fecha_actual, fecha_actual]
                )
                centro_id = cursor.fetchone()[0]

            Auditoria.registrar_evento(
                tabla="Centro", evento="Crear",
                sentencia=f"Centro creada: {nombre} - {abreviatura} - {empresa_nombre} - {estado_nombre}", registro_id=centro_id,
                usuario="Anonimo"
            )

            dic_response.update({
                "code": 201,
                "status": "success",
                "message_user": "Centro creado exitosamente",
                "message": "Centro creado exitosamente",
                "data": {"id": centro_id, "nombre": nombre, "abreviatura": abreviatura, "empresa":empresa_nombre, "estado": estado_nombre},
            })
            logger.info(f"Centro creado: nombre '{nombre}' - abreviatura '{abreviatura}' - empresa '{empresa_nombre}'- estado '{estado_nombre}' (ID: {centro_id})")
            return JsonResponse(dic_response, status=201)

        except Exception as e:
            logger.error(f"Error inesperado al crear el centro: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
    
    return Response([], status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@transaction.atomic
def actualizar_centro(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error updating center",
        "message_user": "Error al actualizar el centro",
        "data": [],
    }

    if request.method == "PUT":
        try:
            centro_data = json.loads(request.body)

            # Validar empresa
            if isinstance(centro_data.get('empresa'), str):
                empresa_obj = Empresa.objects.filter(nombre=centro_data['empresa']).first()
                if not empresa_obj:
                    return JsonResponse({"message_user": "Empresa inválido.", "data": {"empresa": "Empresa no encontrado."}}, status=400)
                centro_data['empresa'] = empresa_obj.id

            # Validar datos con el serializer
            serializer = CentroSerializer(data=centro_data, partial=True)
            if not serializer.is_valid():
                return JsonResponse({"message_user": "Datos inválidos.", "data": serializer.errors}, status=400)

            # Verificar si el centro existe
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Centro WHERE id = %s", [id])         
                if cursor.fetchone()[0] == 0:
                    return JsonResponse({"message_user": "El centro no existe."}, status=400)

            # Verificar duplicado de nombre y abreviatura
            with connection.cursor() as cursor:
                cursor.execute(
                    """ SELECT COUNT(*) FROM Centro WHERE (nombre = %s OR abreviatura = %s) AND estado_id IN (1, 2) AND id != %s""",
                    [serializer.validated_data["nombre"], serializer.validated_data["abreviatura"],id]
                )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe un centro con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)


            # Actualizar centro
            validated_data = serializer.validated_data
            empresa_id = validated_data.get("empresa").id
            estado_id = validated_data.get("estado").id
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Empresa WHERE id = %s", [empresa_id])
                    empresa_nombre = cursor.fetchone()[0]

            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                    estado_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Centro SET nombre=%s, abreviatura=%s, empresa_id=%s, estado_id=%s, fecha_modificacion=%s WHERE id=%s",
                    [validated_data.get("nombre"), validated_data.get("abreviatura"), validated_data.get("empresa").id,
                    validated_data.get("estado").id, datetime.now(), id]
                )

            # Registrar auditoría
            Auditoria.registrar_evento(
                tabla="Centro", evento="Actualizar",
                sentencia=f"Centro actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {empresa_nombre} - {estado_nombre} ",
                registro_id=id, usuario="Anonimo"
            )

            dic_response.update({
                "code": 200, "status": "success",
                "message": "Center updated successfully",
                "message_user": "Centro actualizado exitosamente",
                "data": serializer.data,
            })

            logger.info(f"Centro actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {empresa_nombre} - {estado_nombre} (ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al actualizar el centro: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)

@api_view(["PATCH"])
@transaction.atomic
def eliminar_centro(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error deleting center",
        "message_user": "Error al eliminar la centro",
        "data": [],
    }

    if request.method == "PATCH":
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT estado_id FROM Centro WHERE id = %s", [id])
                resultado = cursor.fetchone()

            if not resultado:
                dic_response["message_user"] = "Centro no encontrado."
                return JsonResponse(dic_response, status=404)

            if resultado[0] == 3:  # 3: Eliminado
                dic_response["message_user"] = "El Centro ya está eliminado."
                return JsonResponse(dic_response, status=400)

            # Actualizar el estado a 'Eliminado'
            fecha_modificacion = datetime.now()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Centro SET estado_id = 3, fecha_modificacion = %s WHERE id = %s",
                    [fecha_modificacion, id],
                )

            # Registrar auditoría y serializar el departamento actualizado
            centro = Centro.objects.get(id=id)
            Auditoria.registrar_evento(
                tabla="Centro",
                evento="Eliminar",
                sentencia=f"Se eliminó lógicamente el centro con id: {id}.",
                registro_id=id,
                usuario="Anonimo",  # Reemplazar con el usuario actual si está disponible
            )

            serializer = CentroSerializer(centro)
            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Centro eliminado lógicamente",
                    "message": "Center deleted logically",
                    "data": serializer.data,
                }
            )
        
            logger.info(f"Centro eliminado logicamente: (ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar el centro: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)

# ------- PARA SELECCIONAR LOS ACTIVOS 
@api_view(["GET"])
@transaction.atomic
def listar_centros_activos(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Center active system not found",
        "message_user": "Centros activos no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT c.id, c.nombre, c.abreviatura, 
                        e.nombre as empresa_nombre, 
                        TO_CHAR(c.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(c.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE WHEN c.estado_id = 3 THEN 'Eliminado'
                                WHEN c.estado_id = 2 THEN 'Inactivo'
                                ELSE 'Activo' 
                        END as estado_nombre
                    FROM centro c
                    LEFT JOIN empresa e ON c.empresa_id = e.id
                    WHERE c.estado_id = 1
                    ORDER BY c.id DESC
                """)
            
                centros = cursor.fetchall()
                centro_serializados = [
                    {**CentroSerializer(Centro(
                        id=p[0], nombre=p[1], abreviatura=p[2], empresa_id=p[3],
                        fecha_creacion=p[4], fecha_modificacion=p[5]
                    )).data, 'estado': p[6]} for p in centros
                ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Centros activos obtenidos correctamente",
                "message": "Centros activos obtenidos correctamente",
                "data": centro_serializados,
            })
            return JsonResponse(dic_response, status=200, safe=False)

        except DatabaseError as e:
            logger.error(f"Error al listar los centros activos: {str(e)}")
            return JsonResponse({"mensaje": "Error al listar los centros activos."}, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------ CRUD ALMACEN -----------------------------------------------------------


@api_view(["GET"])
@transaction.atomic
def listar_almacenes(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "warehouse system not found",
        "message_user": "Almacenes no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT a.id, a.nombre, a.abreviatura, 
                        c.nombre as centro_nombre, 
                        TO_CHAR(a.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(a.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE WHEN a.estado_id = 3 THEN 'Eliminado'
                                WHEN a.estado_id = 2 THEN 'Inactivo'
                                ELSE 'Activo' 
                        END as estado_nombre
                    FROM almacen a
                    LEFT JOIN centro c ON a.centro_id = c.id
                    WHERE a.estado_id <> 3
                    ORDER BY a.id DESC
                """)
            
                almacenes = cursor.fetchall()
                almacen_serializados = [
                    {**AlmacenSerializer(Almacen(
                        id=p[0], nombre=p[1], abreviatura=p[2], centro_id=p[3],
                        fecha_creacion=p[4], fecha_modificacion=p[5]
                    )).data, 'estado': p[6]} for p in almacenes
                ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Almacén obtenidos correctamente",
                "message": "Almacén obtenidos correctamente",
                "data": almacen_serializados,
            })
            return JsonResponse(dic_response, status=200, safe=False)

        except DatabaseError as e:
            logger.error(f"Error al listar los almacenes: {str(e)}")
            return JsonResponse({"mensaje": "Error al listar los almacenes."}, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@transaction.atomic
def crear_almacen(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error creating warehouse",
        "message_user": "Error al crear el almacen",
        "data": [],
    }
    
    if request.method == 'POST':
        try:
            # Deserialize request data using the serializer
            serializer = AlmacenSerializer(data=request.data)
            if not serializer.is_valid():
                return JsonResponse({"message": "Datos inválidos.", "data": serializer.errors}, status=400)
            
            nombre = serializer.validated_data["nombre"]
            abreviatura = serializer.validated_data["abreviatura"]
            centro_id = serializer.validated_data["centro"].id
            estado_id = 1
            fecha_actual = datetime.now()
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT nombre FROM Centro WHERE id = %s", [centro_id])
                centro_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                estado_nombre = cursor.fetchone()[0]
                
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM Almacen WHERE (nombre = %s OR abreviatura = %s) AND estado_id IN (1, 2)",
                    [nombre, abreviatura]
                )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe un almacén con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Almacen (nombre, abreviatura, centro_id, estado_id, fecha_creacion, fecha_modificacion) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                    [nombre, abreviatura, centro_id, estado_id, fecha_actual, fecha_actual]
                )
                almacen_id = cursor.fetchone()[0]

            Auditoria.registrar_evento(
                tabla="Almacén", evento="Crear",
                sentencia=f"Almacén creada: {nombre} - {abreviatura} - {centro_id} - {estado_id}", registro_id=almacen_id,
                usuario="Anonimo"
            )

            dic_response.update({
                "code": 201,
                "status": "success",
                "message_user": "Almacén creado exitosamente",
                "message": "Warehouse saved successfully",
                "data": {"id": almacen_id, "nombre": nombre, "abreviatura": abreviatura, "centro":centro_nombre, "estado": estado_nombre},
            })
            logger.info(f"Almacén creado: nombre '{nombre}' - abreviatura '{abreviatura}' - centro '{centro_nombre}' - estado '{estado_nombre}' (ID: {almacen_id})")
            return JsonResponse(dic_response, status=201)

        except Exception as e:
            logger.error(f"Error inesperado al crear el Almacén: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
    
    return Response([], status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@transaction.atomic
def actualizar_almacen(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error updating warehouse",
        "message_user": "Error al actualizar el almacén",
        "data": [],
    }

    if request.method == "PUT":
        try:
            almacen_data = json.loads(request.body)

            if isinstance(almacen_data.get('centro'), str):
                centro_obj = Centro.objects.filter(nombre=almacen_data['centro']).first()
                if not centro_obj:
                    return JsonResponse({"message_user": "Centro inválido.", "data": {"empresa": "Centro no encontrado."}}, status=400)
                almacen_data['centro'] = centro_obj.id

            serializer = AlmacenSerializer(data=almacen_data, partial=True)
            if not serializer.is_valid():
                return JsonResponse({"message_user": "Datos inválidos.", "data": serializer.errors}, status=400)

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Almacen WHERE id = %s", [id])         
                if cursor.fetchone()[0] == 0:
                    return JsonResponse({"message_user": "El almacen no existe."}, status=400)

            # Verificar duplicado de nombre y abreviatura
            with connection.cursor() as cursor:
                cursor.execute(
                    """ SELECT COUNT(*) FROM Almacen WHERE (nombre = %s OR abreviatura = %s) AND estado_id IN (1, 2) AND id != %s""",
                    [serializer.validated_data["nombre"], serializer.validated_data["abreviatura"],id]
                )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe un almacén con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)

            validated_data = serializer.validated_data
            centro_id = validated_data.get("centro").id
            estado_id = validated_data.get("estado").id
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Centro WHERE id = %s", [centro_id])
                    centro_nombre = cursor.fetchone()[0]
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                    estado_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Almacen SET nombre=%s, abreviatura=%s, centro_id=%s, estado_id=%s, fecha_modificacion=%s WHERE id=%s",
                    [validated_data.get("nombre"), validated_data.get("abreviatura"), validated_data.get("centro").id,
                    validated_data.get("estado").id, datetime.now(), id]
                )

            # Registrar auditoría
            Auditoria.registrar_evento(
                tabla="Almacén", evento="Actualizar",
                sentencia=f"Almacén actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {centro_nombre} - {estado_nombre}",
                registro_id=id, usuario="Anonimo"
            )

            dic_response.update({
                "code": 200, "status": "success",
                "message": "Warehouse updated successfully",
                "message_user": "Almacén actualizado exitosamente",
                "data": serializer.data,
            })

            logger.info(f"Almacén actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {centro_nombre} - {estado_nombre} (ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al actualizar el almacén: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)


@api_view(["PATCH"])
@transaction.atomic
def eliminar_almacen(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error deleting warehouse",
        "message_user": "Error al eliminar la almacén",
        "data": [],
    }

    if request.method == "PATCH":
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT estado_id FROM Almacen WHERE id = %s", [id])
                resultado = cursor.fetchone()

            if not resultado:
                dic_response["message_user"] = "Almacén no encontrado."
                return JsonResponse(dic_response, status=404)

            if resultado[0] == 3:  # 3: Eliminado
                dic_response["message_user"] = "El almacén ya está eliminado."
                return JsonResponse(dic_response, status=400)

            # Actualizar el estado a 'Eliminado'
            fecha_modificacion = datetime.now()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Almacen SET estado_id = 3, fecha_modificacion = %s WHERE id = %s",
                    [fecha_modificacion, id],
                )
                
            almacen = Almacen.objects.get(id=id)
            Auditoria.registrar_evento(
                tabla="Almacén",
                evento="Eliminar",
                sentencia=f"Se eliminó lógicamente el almacén con id: {id}.",
                registro_id=id,
                usuario="Anonimo",  
            )

            serializer = AlmacenSerializer(almacen)
            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Almacén eliminado lógicamente",
                    "message": "Warehouse deleted logically",
                    "data": serializer.data,
                }
            )
        
            logger.info(f"Almacén eliminado logicamente: (ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar el almacén: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)


# ------------------------------------------------------ CRUD PROVEEDOR -----------------------------------------------------------


@api_view(["GET"])
@transaction.atomic
def listar_proveedores(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Suppliers system not found",
        "message_user": "Proveedores no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT p.id, p.nombre, p.abreviatura, 
                        TO_CHAR(p.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(p.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE WHEN p.estado_id = 3 THEN 'Eliminado'
                                WHEN p.estado_id = 2 THEN 'Inactivo'
                                ELSE 'Activo' 
                        END as estado_nombre
                    FROM proveedor p
                    WHERE p.estado_id <> 3
                    ORDER BY p.id DESC
                """)
            
                proveedores = cursor.fetchall()
                proveedores_serializados = [
                    {**ProveedorSerializer(Proveedor(
                        id=p[0], nombre=p[1], abreviatura=p[2],
                        fecha_creacion=p[3], fecha_modificacion=p[4]
                    )).data, 'estado': p[5]} for p in proveedores
                ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Proveedores obtenidos correctamente",
                "message": "Proveedores obtenidos correctamente",
                "data": proveedores_serializados,
            })
            return JsonResponse(dic_response, status=200, safe=False)

        except DatabaseError as e:
            logger.error(f"Error al listar los proveedores: {str(e)}")
            return JsonResponse({"mensaje": "Error al listar los proveedores."}, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@transaction.atomic
def crear_proveedor(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error creating supplier",
        "message_user": "Error al crear el proveedor",
        "data": [],
    }
    
    if request.method == 'POST':
        try:
            # Deserialize request data using the serializer
            serializer = ProveedorSerializer(data=request.data)
            if not serializer.is_valid():
                return JsonResponse({"message": "Datos inválidos.", "data": serializer.errors}, status=400)
            
            nombre = serializer.validated_data["nombre"]
            abreviatura = serializer.validated_data["abreviatura"]
            estado_id = 1
            fecha_actual = datetime.now()
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                estado_nombre = cursor.fetchone()[0]
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM Proveedor WHERE (nombre = %s OR abreviatura = %s) AND estado_id IN (1, 2)",
                    [nombre, abreviatura]
                    )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe un proveedor con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)
            
    
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Proveedor (nombre, abreviatura, estado_id, fecha_creacion, fecha_modificacion) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                    [nombre, abreviatura, estado_id, fecha_actual, fecha_actual]
                )
                proveedor_id = cursor.fetchone()[0]

            Auditoria.registrar_evento(
                tabla="Proveedor", evento="Crear",
                sentencia=f"Proveedor creada: {nombre} - {abreviatura} -{estado_nombre}", registro_id=proveedor_id,
                usuario="Anonimo"
            )

            dic_response.update({
                "code": 201,
                "status": "success",
                "message_user": "Proveedor creado exitosamente",
                "message": "Supplier saved successfully",
                "data": {"id": proveedor_id, "nombre": nombre, "abreviatura": abreviatura, "estado": estado_nombre},
            })
            logger.info(f"Proveedor creado: nombre '{nombre}' - abreviatura '{abreviatura}'- estado '{estado_nombre}' (ID: {proveedor_id})")
            return JsonResponse(dic_response, status=201)

        except Exception as e:
            logger.error(f"Error inesperado al crear el proveedor: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
    
    return Response([], status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@transaction.atomic
def actualizar_proveedor(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error updating supplier",
        "message_user": "Error al actualizar el proveedor",
        "data": [],
    }

    if request.method == "PUT":
        try:
            proveedor_data = json.loads(request.body)

            serializer = ProveedorSerializer(data=proveedor_data, partial=True)
            if not serializer.is_valid():
                return JsonResponse({"message_user": "Datos inválidos.", "data": serializer.errors}, status=400)

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Proveedor WHERE id = %s", [id])         
                if cursor.fetchone()[0] == 0:
                    return JsonResponse({"message_user": "El proveedor no existe."}, status=400)

            # Verificar duplicado de nombre y abreviatura
            with connection.cursor() as cursor:
                cursor.execute(
                        """
                            SELECT COUNT(*) 
                            FROM Proveedor 
                            WHERE (nombre = %s OR abreviatura = %s) 
                            AND estado_id IN (1, 2)
                            AND id != %s  -- Excluir el registro actual del chequeo
                            """,
                        [serializer.validated_data["nombre"], serializer.validated_data["abreviatura"], id]
                )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe un proveedor con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)

            validated_data = serializer.validated_data

            estado_id = validated_data.get("estado").id
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                    estado_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Proveedor SET nombre=%s, abreviatura=%s, estado_id=%s, fecha_modificacion=%s WHERE id=%s",
                    [validated_data.get("nombre"), validated_data.get("abreviatura"),
                    validated_data.get("estado").id, datetime.now(), id]
                )

            # Registrar auditoría
            Auditoria.registrar_evento(
                tabla="Proveedor", evento="Actualizar",
                sentencia=f"Proveedor actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {estado_nombre}",
                registro_id=id, usuario="Anonimo"
            )

            dic_response.update({
                "code": 200, "status": "success",
                "message": "Supplier updated successfully",
                "message_user": "Proveedor actualizado exitosamente",
                "data": serializer.data,
            })

            logger.info(f"Proveedor actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {estado_nombre}(ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al actualizar el proveedor: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)


@api_view(["PATCH"])
@transaction.atomic
def eliminar_proveedor(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error deleting supplier",
        "message_user": "Error al eliminar el proveedor",
        "data": [],
    }

    if request.method == "PATCH":
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT estado_id FROM Proveedor WHERE id = %s", [id])
                resultado = cursor.fetchone()

            if not resultado:
                dic_response["message_user"] = "Proveedor no encontrado."
                return JsonResponse(dic_response, status=404)

            if resultado[0] == 3:  # 3: Eliminado
                dic_response["message_user"] = "El Proveedor ya está eliminado."
                return JsonResponse(dic_response, status=400)

            # Actualizar el estado a 'Eliminado'
            fecha_modificacion = datetime.now()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Proveedor SET estado_id = 3, fecha_modificacion = %s WHERE id = %s",
                    [fecha_modificacion, id],
                )
                
            proveedor = Proveedor.objects.get(id=id)
            Auditoria.registrar_evento(
                tabla="Proveedor",
                evento="Eliminar",
                sentencia=f"Se eliminó lógicamente el proveedor con id: {id}.",
                registro_id=id,
                usuario="Anonimo",  
            )

            serializer = ProveedorSerializer(proveedor)
            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Proveedor eliminado lógicamente",
                    "message": "Supplier deleted logically",
                    "data": serializer.data,
                }
            )
        
            logger.info(f"Proveedor eliminado logicamente: (ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar el proveedor: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)

# ------------------------------------------------------ CRUD GRUPO -----------------------------------------------------------


@api_view(["GET"])
@transaction.atomic
def listar_grupos(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Groups system not found",
        "message_user": "Grupos no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT g.id, g.nombre, g.abreviatura, 
                        TO_CHAR(g.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(g.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE WHEN g.estado_id = 3 THEN 'Eliminado'
                                WHEN g.estado_id = 2 THEN 'Inactivo'
                                ELSE 'Activo' 
                        END as estado_nombre
                    FROM grupo g
                    WHERE g.estado_id <> 3
                    ORDER BY g.id DESC
                """)
            
                grupos = cursor.fetchall()
                grupos_serializados = [
                    {**ProveedorSerializer(Proveedor(
                        id=p[0], nombre=p[1], abreviatura=p[2],
                        fecha_creacion=p[3], fecha_modificacion=p[4]
                    )).data, 'estado': p[5]} for p in grupos
                ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Grupos obtenidos correctamente",
                "message": "Grupos obtenidos correctamente",
                "data": grupos_serializados,
            })
            return JsonResponse(dic_response, status=200, safe=False)

        except DatabaseError as e:
            logger.error(f"Error al listar los grupos: {str(e)}")
            return JsonResponse({"mensaje": "Error al listar los grupos."}, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@transaction.atomic
def crear_grupo(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error creating group",
        "message_user": "Error al crear el grupo",
        "data": [],
    }
    
    if request.method == 'POST':
        try:
            # Deserialize request data using the serializer
            serializer = GrupoSerializer(data=request.data)
            if not serializer.is_valid():
                return JsonResponse({"message": "Datos inválidos.", "data": serializer.errors}, status=400)
            
            nombre = serializer.validated_data["nombre"]
            abreviatura = serializer.validated_data["abreviatura"]
            estado_id = 1
            fecha_actual = datetime.now()
                
            with connection.cursor() as cursor:
                cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                estado_nombre = cursor.fetchone()[0]
                
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM Grupo WHERE (nombre = %s OR abreviatura = %s) AND estado_id IN (1, 2)",
                    [nombre, abreviatura]
                    )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe un grupo con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)
            
    
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Grupo (nombre, abreviatura, estado_id, fecha_creacion, fecha_modificacion) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                    [nombre, abreviatura, estado_id, fecha_actual, fecha_actual]
                )
                grupo_id = cursor.fetchone()[0]

            Auditoria.registrar_evento(
                tabla="Grupo", evento="Crear",
                sentencia=f"Grupo creada: {nombre} - {abreviatura} - {estado_nombre}", registro_id=grupo_id,
                usuario="Anonimo"
            )

            dic_response.update({
                "code": 201,
                "status": "success",
                "message_user": "Grupo creado exitosamente",
                "message": "Group saved successfully",
                "data": {"id": grupo_id, "nombre": nombre, "abreviatura": abreviatura, "estado": estado_nombre},
            })
            logger.info(f"Grupo creado: nombre '{nombre}' - abreviatura '{abreviatura}' - estado '{estado_nombre}' (ID: {grupo_id})")
            return JsonResponse(dic_response, status=201)

        except Exception as e:
            logger.error(f"Error inesperado al crear el grupo: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
    
    return Response([], status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@transaction.atomic
def actualizar_grupo(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error updating supplier",
        "message_user": "Error al actualizar el grupo",
        "data": [],
    }

    if request.method == "PUT":
        try:
            grupo_data = json.loads(request.body)

            serializer = GrupoSerializer(data=grupo_data, partial=True)
            if not serializer.is_valid():
                return JsonResponse({"message_user": "Datos inválidos.", "data": serializer.errors}, status=400)

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Grupo WHERE id = %s", [id])         
                if cursor.fetchone()[0] == 0:
                    return JsonResponse({"message_user": "El grupo no existe."}, status=400)

            # Verificar duplicado de nombre y abreviatura
            with connection.cursor() as cursor:
                cursor.execute(
                        """
                            SELECT COUNT(*) 
                            FROM Grupo 
                            WHERE (nombre = %s OR abreviatura = %s) 
                            AND estado_id IN (1, 2)
                            AND id != %s 
                            """,
                        [serializer.validated_data["nombre"], serializer.validated_data["abreviatura"], id]
                )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe un grupo con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)

            validated_data = serializer.validated_data
            estado_id = validated_data.get("estado").id
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                    estado_nombre = cursor.fetchone()[0]
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Grupo SET nombre=%s, abreviatura=%s, estado_id=%s, fecha_modificacion=%s WHERE id=%s",
                    [validated_data.get("nombre"), validated_data.get("abreviatura"),
                    validated_data.get("estado").id, datetime.now(), id]
                )

            # Registrar auditoría
            Auditoria.registrar_evento(
                tabla="Grupo", evento="Actualizar",
                sentencia=f"Grupo actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {estado_nombre}",
                registro_id=id, usuario="Anonimo"
            )

            dic_response.update({
                "code": 200, "status": "success",
                "message": "Group updated successfully",
                "message_user": "Grupo actualizado exitosamente",
                "data": serializer.data,
            })

            logger.info(f"Grupo actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} (ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al actualizar el grupo: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)


@api_view(["PATCH"])
@transaction.atomic
def eliminar_grupo(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error deleting group",
        "message_user": "Error al eliminar el grupo",
        "data": [],
    }

    if request.method == "PATCH":
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT estado_id FROM Grupo WHERE id = %s", [id])
                resultado = cursor.fetchone()

            if not resultado:
                dic_response["message_user"] = "Grupo no encontrado."
                return JsonResponse(dic_response, status=404)

            if resultado[0] == 3:  # 3: Eliminado
                dic_response["message_user"] = "El grupo ya está eliminado."
                return JsonResponse(dic_response, status=400)

            # Actualizar el estado a 'Eliminado'
            fecha_modificacion = datetime.now()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Grupo SET estado_id = 3, fecha_modificacion = %s WHERE id = %s",
                    [fecha_modificacion, id],
                )
                
            grupo = Grupo.objects.get(id=id)
            Auditoria.registrar_evento(
                tabla="Grupo",
                evento="Eliminar",
                sentencia=f"Se eliminó lógicamente el grupo con id: {id}.",
                registro_id=id,
                usuario="Anonimo",  
            )

            serializer = GrupoSerializer(grupo)
            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Grupo eliminado lógicamente",
                    "message": "Group deleted logically",
                    "data": serializer.data,
                }
            )
        
            logger.info(f"Grupo eliminado logicamente: (ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar el grupo: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)

# ------- PARA SELECCIONAR LOS ACTIVOS 

@api_view(["GET"])
@transaction.atomic
def listar_grupos_activos(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Grupos activos no encontradas",
        "message_user": "Grupos activos no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT g.id, g.nombre, g.abreviatura, 
                        TO_CHAR(g.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(g.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE WHEN g.estado_id = 3 THEN 'Eliminado'
                                WHEN g.estado_id = 2 THEN 'Inactivo'
                                ELSE 'Activo' 
                        END as estado_nombre
                    FROM grupo g
                    WHERE g.estado_id = 1
                    ORDER BY g.id DESC
                """)
            
                grupos = cursor.fetchall()
                grupos_serializados = [
                    {**GrupoSerializer(Grupo(
                        id=p[0], nombre=p[1], abreviatura=p[2],
                        fecha_creacion=p[3], fecha_modificacion=p[4]
                    )).data, 'estado': p[5]} for p in grupos
                ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Grupos activos obtenidos correctamente",
                "message": "Grupos activos obtenidos correctamente",
                "data": grupos_serializados,
            })
            return JsonResponse(dic_response, status=200, safe=False)

        except DatabaseError as e:
            logger.error(f"Error al listar los grupos activos: {str(e)}")
            return JsonResponse({"mensaje": "Error al listar los grupos activos."}, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------ CRUD SUBGRUPO -----------------------------------------------------------


@api_view(["GET"])
@transaction.atomic
def listar_subgrupos(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Subgroups system not found",
        "message_user": "Subgrupos no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT sg.id, sg.nombre, sg.abreviatura, 
                        g.nombre as grupo_nombre, 
                        TO_CHAR(sg.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(sg.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE WHEN sg.estado_id = 3 THEN 'Eliminado'
                                WHEN sg.estado_id = 2 THEN 'Inactivo'
                                ELSE 'Activo' 
                        END as estado_nombre
                    FROM subgrupo sg
                    LEFT JOIN grupo g ON sg.grupo_id = g.id
                    WHERE sg.estado_id <> 3
                    ORDER BY sg.id DESC
                """)
            
                subgrupos = cursor.fetchall()
                subgrupos_serializados = [
                    {**SubgrupoSerializer(Subgrupo(
                        id=p[0], nombre=p[1], abreviatura=p[2], grupo_id=p[3],
                        fecha_creacion=p[4], fecha_modificacion=p[5]
                    )).data, 'estado': p[6]} for p in subgrupos
                ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Subgrupos obtenidos correctamente",
                "message": "Subgrupos obtenidos correctamente",
                "data": subgrupos_serializados,
            })
            return JsonResponse(dic_response, status=200, safe=False)

        except DatabaseError as e:
            logger.error(f"Error al listar los subgrupos: {str(e)}")
            return JsonResponse({"mensaje": "Error al listar los subgrupos."}, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@transaction.atomic
def crear_subgrupo(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error creating subgroups",
        "message_user": "Error al crear el subgrupo",
        "data": [],
    }
    
    if request.method == 'POST':
        try:
            # Deserialize request data using the serializer
            serializer = SubgrupoSerializer(data=request.data)
            if not serializer.is_valid():
                return JsonResponse({"message": "Datos inválidos.", "data": serializer.errors}, status=400)
            
            nombre = serializer.validated_data["nombre"]
            abreviatura = serializer.validated_data["abreviatura"]
            grupo_id = serializer.validated_data["grupo"].id
            estado_id = 1
            fecha_actual = datetime.now()
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT nombre FROM Grupo WHERE id = %s", [grupo_id])
                grupo_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                estado_nombre = cursor.fetchone()[0]
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM Subgrupo WHERE (nombre = %s OR abreviatura = %s) AND estado_id IN (1, 2)",
                    [nombre, abreviatura]
                )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe un subgrupo con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Subgrupo (nombre, abreviatura, grupo_id, estado_id, fecha_creacion, fecha_modificacion) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                    [nombre, abreviatura, grupo_id, estado_id, fecha_actual, fecha_actual]
                )
                subgrupo_id = cursor.fetchone()[0]

            Auditoria.registrar_evento(
                tabla="Subgrupo", evento="Crear",
                sentencia=f"Subgrupo creada: {nombre} - {abreviatura} - {grupo_nombre} - {estado_nombre}", registro_id=subgrupo_id,
                usuario="Anonimo"
            )

            dic_response.update({
                "code": 201,
                "status": "success",
                "message_user": "Subgrupo creado exitosamente",
                "message": "Subgroup saved successfully",
                "data": {"id": subgrupo_id, "nombre": nombre, "abreviatura": abreviatura, "grupo":grupo_nombre, "estado": estado_nombre},
            })  
            logger.info(f"Almacén creado: nombre '{nombre}' - abreviatura '{abreviatura}' - grupo '{grupo_nombre}' - estado '{estado_nombre}' (ID: {subgrupo_id})")
            return JsonResponse(dic_response, status=201)

        except Exception as e:
            logger.error(f"Error inesperado al crear el subgrupo: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
    
    return Response([], status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@transaction.atomic
def actualizar_subgrupo(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error updating subgroup",
        "message_user": "Error al actualizar el subgrupo",
        "data": [],
    }

    if request.method == "PUT":
        try:
            subgrupo_data = json.loads(request.body)

            if isinstance(subgrupo_data.get('grupo'), str):
                grupo_obj = Grupo.objects.filter(nombre=subgrupo_data['grupo']).first()
                if not grupo_obj:
                    return JsonResponse({"message_user": "Grupo inválido.", "data": {"Grupo": "Grupo no encontrado."}}, status=400)
                subgrupo_data['grupo'] = grupo_obj.id

            serializer = SubgrupoSerializer(data=subgrupo_data, partial=True)
            if not serializer.is_valid():
                return JsonResponse({"message_user": "Datos inválidos.", "data": serializer.errors}, status=400)

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Subgrupo WHERE id = %s", [id])         
                if cursor.fetchone()[0] == 0:
                    return JsonResponse({"message_user": "El subgrupo no existe."}, status=400)

            # Verificar duplicado de nombre y abreviatura
            with connection.cursor() as cursor:
                cursor.execute(
                    """ SELECT COUNT(*) FROM Subgrupo WHERE (nombre = %s OR abreviatura = %s) AND estado_id IN (1, 2) AND id != %s""",
                    [serializer.validated_data["nombre"], serializer.validated_data["abreviatura"],id]
                )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe un subgrupo con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)

            validated_data = serializer.validated_data

            grupo_id = validated_data.get("grupo").id
            estado_id = validated_data.get("estado").id
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Grupo WHERE id = %s", [grupo_id])
                    grupo_nombre = cursor.fetchone()[0]
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                    estado_nombre = cursor.fetchone()[0]
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Subgrupo SET nombre=%s, abreviatura=%s, grupo_id=%s, estado_id=%s, fecha_modificacion=%s WHERE id=%s",
                    [validated_data.get("nombre"), validated_data.get("abreviatura"), validated_data.get("grupo").id,
                    validated_data.get("estado").id, datetime.now(), id]
                )

            # Registrar auditoría
            Auditoria.registrar_evento(
                tabla="Subgrupo", evento="Actualizar",
                sentencia=f"Subgrupo actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {grupo_nombre} - {estado_nombre}",
                registro_id=id, usuario="Anonimo"
            )

            dic_response.update({
                "code": 200, "status": "success",
                "message": "Subgroup updated successfully",
                "message_user": "Subgrupo actualizado exitosamente",
                "data": serializer.data,
            })

            logger.info(f"Subgrupo actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} (ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al actualizar el subgrupo: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)


@api_view(["PATCH"])
@transaction.atomic
def eliminar_subgrupo(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error deleting subgroup",
        "message_user": "Error al eliminar el subgrupo",
        "data": [],
    }

    if request.method == "PATCH":
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT estado_id FROM Subgrupo WHERE id = %s", [id])
                resultado = cursor.fetchone()

            if not resultado:
                dic_response["message_user"] = "Subgrupo no encontrado."
                return JsonResponse(dic_response, status=404)

            if resultado[0] == 3:  # 3: Eliminado
                dic_response["message_user"] = "El subgrupo ya está eliminado."
                return JsonResponse(dic_response, status=400)

            # Actualizar el estado a 'Eliminado'
            fecha_modificacion = datetime.now()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Subgrupo SET estado_id = 3, fecha_modificacion = %s WHERE id = %s",
                    [fecha_modificacion, id],
                )
                
            subgrupo = Subgrupo.objects.get(id=id)
            Auditoria.registrar_evento(
                tabla="Subgrupo",
                evento="Eliminar",
                sentencia=f"Se eliminó lógicamente el subgrupo con id: {id}.",
                registro_id=id,
                usuario="Anonimo",  
            )

            serializer = SubgrupoSerializer(subgrupo)
            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Subgrupo eliminado lógicamente",
                    "message": "Subgroup deleted logically",
                    "data": serializer.data,
                }
            )
        
            logger.info(f"Subgrupo eliminado logicamente: (ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar el subgrupo: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)

# ------- PARA SELECCIONAR LOS ACTIVOS 
@api_view(["GET"])
@transaction.atomic
def listar_subgrupos_activos(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Subgroups active system not found",
        "message_user": "Subgrupos activos no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT sg.id, sg.nombre, sg.abreviatura, 
                        g.nombre as grupo_nombre, 
                        TO_CHAR(sg.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(sg.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE WHEN sg.estado_id = 3 THEN 'Eliminado'
                                WHEN sg.estado_id = 2 THEN 'Inactivo'
                                ELSE 'Activo' 
                        END as estado_nombre
                    FROM subgrupo sg
                    LEFT JOIN grupo g ON sg.grupo_id = g.id
                    WHERE sg.estado_id = 1
                    ORDER BY sg.id DESC
                """)
            
                subgrupos = cursor.fetchall()
                subgrupos_serializados = [
                    {**SubgrupoSerializer(Subgrupo(
                        id=p[0], nombre=p[1], abreviatura=p[2], grupo_id=p[3],
                        fecha_creacion=p[4], fecha_modificacion=p[5]
                    )).data, 'estado': p[6]} for p in subgrupos
                ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Subgrupos obtenidos correctamente",
                "message": "Subgrupos obtenidos correctamente",
                "data": subgrupos_serializados,
            })
            return JsonResponse(dic_response, status=200, safe=False)

        except DatabaseError as e:
            logger.error(f"Error al listar los subgrupos: {str(e)}")
            return JsonResponse({"mensaje": "Error al listar los subgrupos."}, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------ CRUD PRODUCTO -----------------------------------------------------------

@api_view(["GET"])
@transaction.atomic
def listar_productos(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Products system not found",
        "message_user": "Productos no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT p.id, p.nombre, p.abreviatura, 
                        sg.nombre as grupo_nombre, 
                        TO_CHAR(p.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(p.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE WHEN p.estado_id = 3 THEN 'Eliminado'
                                WHEN p.estado_id = 2 THEN 'Inactivo'
                                ELSE 'Activo' 
                        END as estado_nombre
                    FROM producto p
                    LEFT JOIN subgrupo sg ON p.subgrupo_id = sg.id
                    WHERE p.estado_id <> 3
                    ORDER BY p.id DESC
                """)
            
                productos = cursor.fetchall()
                productos_serializados = [
                    {**ProductoSerializer(Producto(
                        id=p[0], nombre=p[1], abreviatura=p[2], subgrupo_id=p[3],
                        fecha_creacion=p[4], fecha_modificacion=p[5]
                    )).data, 'estado': p[6]} for p in productos
                ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Productos obtenidos correctamente",
                "message": "Productos obtenidos correctamente",
                "data": productos_serializados,
            })
            return JsonResponse(dic_response, status=200, safe=False)

        except DatabaseError as e:
            logger.error(f"Error al listar los productos: {str(e)}")
            return JsonResponse({"mensaje": "Error al listar los productos."}, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@transaction.atomic
def crear_producto(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error creating product",
        "message_user": "Error al crear el producto",
        "data": [],
    }
    
    if request.method == 'POST':
        try:
            # Deserialize request data using the serializer
            serializer = ProductoSerializer(data=request.data)
            if not serializer.is_valid():
                return JsonResponse({"message": "Datos inválidos.", "data": serializer.errors}, status=400)
            
            nombre = serializer.validated_data["nombre"]
            abreviatura = serializer.validated_data["abreviatura"]
            subgrupo_id = serializer.validated_data["subgrupo"].id
            estado_id = 1
            fecha_actual = datetime.now()
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT nombre FROM Subgrupo WHERE id = %s", [subgrupo_id])
                subgrupo_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                estado_nombre = cursor.fetchone()[0]
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM Producto WHERE (nombre = %s OR abreviatura = %s) AND estado_id IN (1, 2)",
                    [nombre, abreviatura]
                )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe un producto con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Producto (nombre, abreviatura, subgrupo_id, estado_id, fecha_creacion, fecha_modificacion) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                    [nombre, abreviatura, subgrupo_id, estado_id, fecha_actual, fecha_actual]
                )
                producto_id = cursor.fetchone()[0]

            Auditoria.registrar_evento(
                tabla="Producto", evento="Crear",
                sentencia=f"Producto creada: {nombre} - {abreviatura} - {subgrupo_nombre} - {estado_nombre}", registro_id=producto_id,
                usuario="Anonimo"
            )

            dic_response.update({
                "code": 201,
                "status": "success",
                "message_user": "Producto creado exitosamente",
                "message": "Producto saved successfully",
                "data": {"id": producto_id, "nombre": nombre, "abreviatura": abreviatura, "subgrupo":subgrupo_nombre, "estado": estado_nombre},
            })
            logger.info(f"Producto creado: nombre '{nombre}' - abreviatura '{abreviatura}' - subgrupo '{subgrupo_nombre}' -  estado '{estado_nombre}' (ID: {producto_id})")
            return JsonResponse(dic_response, status=201)

        except Exception as e:
            logger.error(f"Error inesperado al crear el subgrupo: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
    
    return Response([], status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@transaction.atomic
def actualizar_producto(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error updating product",
        "message_user": "Error al actualizar el producto",
        "data": [],
    }

    if request.method == "PUT":
        try:
            producto_data = json.loads(request.body)

            if isinstance(producto_data.get('subgrupo'), str):
                subgrupo_obj = Subgrupo.objects.filter(nombre=producto_data['subgrupo']).first()
                if not subgrupo_obj:
                    return JsonResponse({"message_user": "Subgrupo inválido.", "data": {"Subgrupo": "Subgrupo no encontrado."}}, status=400)
                producto_data['subgrupo'] = subgrupo_obj.id

            serializer = ProductoSerializer(data=producto_data, partial=True)
            if not serializer.is_valid():
                return JsonResponse({"message_user": "Datos inválidos.", "data": serializer.errors}, status=400)

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Producto WHERE id = %s", [id])         
                if cursor.fetchone()[0] == 0:
                    return JsonResponse({"message_user": "El producto no existe."}, status=400)

            # Verificar duplicado de nombre y abreviatura
            with connection.cursor() as cursor:
                cursor.execute(
                    """ SELECT COUNT(*) FROM Producto WHERE (nombre = %s OR abreviatura = %s) AND estado_id IN (1, 2) AND id != %s""",
                    [serializer.validated_data["nombre"], serializer.validated_data["abreviatura"],id]
                )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe un producto con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)

            validated_data = serializer.validated_data
            subgrupo_id = validated_data.get("subgrupo").id
            estado_id = validated_data.get("estado").id
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Subgrupo WHERE id = %s", [subgrupo_id])
                    subgrupo_nombre = cursor.fetchone()[0]
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                    estado_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Producto SET nombre=%s, abreviatura=%s, subgrupo_id=%s, estado_id=%s, fecha_modificacion=%s WHERE id=%s",
                    [validated_data.get("nombre"), validated_data.get("abreviatura"), validated_data.get("subgrupo").id,
                    validated_data.get("estado").id, datetime.now(), id]
                )

            # Registrar auditoría
            Auditoria.registrar_evento(
                tabla="Producto", evento="Actualizar",
                sentencia=f"Producto actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {subgrupo_nombre} - {estado_nombre}",
                registro_id=id, usuario="Anonimo"
            )

            dic_response.update({
                "code": 200, "status": "success",
                "message": "Product updated successfully",
                "message_user": "Producto actualizado exitosamente",
                "data": serializer.data,
            })

            logger.info(f"Producto actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} (ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al actualizar el producto: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)


@api_view(["PATCH"])
@transaction.atomic
def eliminar_producto(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error deleting product",
        "message_user": "Error al eliminar el producto",
        "data": [],
    }

    if request.method == "PATCH":
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT estado_id FROM Producto WHERE id = %s", [id])
                resultado = cursor.fetchone()

            if not resultado:
                dic_response["message_user"] = "Producto no encontrado."
                return JsonResponse(dic_response, status=404)

            if resultado[0] == 3:  # 3: Eliminado
                dic_response["message_user"] = "El producto ya está eliminado."
                return JsonResponse(dic_response, status=400)

            # Actualizar el estado a 'Eliminado'
            fecha_modificacion = datetime.now()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Producto SET estado_id = 3, fecha_modificacion = %s WHERE id = %s",
                    [fecha_modificacion, id],
                )
                
            producto = Producto.objects.get(id=id)
            Auditoria.registrar_evento(
                tabla="Producto",
                evento="Eliminar",
                sentencia=f"Se eliminó lógicamente el producto con id: {id}.",
                registro_id=id,
                usuario="Anonimo",  
            )

            serializer = ProductoSerializer(producto)
            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Producto eliminado lógicamente",
                    "message": "Producto deleted logically",
                    "data": serializer.data,
                }
            )
        
            logger.info(f"Producto eliminado logicamente: (ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar el producto: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)


# ------------------------------------------------------ CRUD TIPOINGSAL -----------------------------------------------------------


@api_view(["GET"])
@transaction.atomic
def listar_tipoingsal(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Products system not found",
        "message_user": "Productos no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT t.id, t.nombre, t.abreviatura, 
                        TO_CHAR(t.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(t.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE WHEN t.estado_id = 3 THEN 'Eliminado'
                                WHEN t.estado_id = 2 THEN 'Inactivo'
                                ELSE 'Activo' 
                        END as estado_nombre
                    FROM tipoingsal t
                    WHERE t.estado_id = 1
                    ORDER BY t.id DESC
                """)
            
                tipoingsal = cursor.fetchall()
                tipoingsal_serializados = [
                    {**TipoingsalSerializer(Tipoingsal(
                        id=p[0], nombre=p[1], abreviatura=p[2],
                        fecha_creacion=p[3], fecha_modificacion=p[4]
                    )).data, 'estado': p[5]} for p in tipoingsal
                ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Tipoingsal obtenidos correctamente",
                "message": "Tipoingsal obtenidos correctamente",
                "data": tipoingsal_serializados,
            })
            return JsonResponse(dic_response, status=200, safe=False)

        except DatabaseError as e:
            logger.error(f"Error al listar los tipoingsal: {str(e)}")
            return JsonResponse({"mensaje": "Error al listar los tipoingsal."}, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_400_BAD_REQUEST)


"""@api_view(["POST"])
@transaction.atomic
def crear_tipoingsal(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error saving Tipoingsal",
        "message_user": "Error al guardar al Tipoingsal",
        "data": [],
    }

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            estado_id = data.get("estado")
            estado = Estado.objects.get(id=estado_id)

            # Verificar si ya existe un país con el mismo nombre y abreviatura en estado activo o inactivo
            tipoingsal_existente = Tipoingsal.objects.filter(
                estado__in=[1, 2],  # 1: Activo, 2: Inactivo
                nombre=data.get("nombre"),
                abreviatura=data.get("abreviatura"),
            ).first()

            if tipoingsal_existente:
                dic_response["message"] = "El Tipoingsal ya existe."
                dic_response["message_user"] = "El Tipoingsal ya existe."
                return JsonResponse(
                    dic_response, safe=False, status=status.HTTP_400_BAD_REQUEST
                )

            # Crear nuevo país
            tipoingsal = Tipoingsal(
                nombre=data.get("nombre"),
                abreviatura=data.get("abreviatura"),
                estado=estado,
            )
            tipoingsal.save()

            # Registrar evento en auditoría
            Auditoria.registrar_evento(
                tabla="Tipoingsal",
                evento="Crear",
                sentencia=f"Proveedor creado: {tipoingsal.nombre} - {tipoingsal.abreviatura} con estado {tipoingsal.estado.nombre}",
                registro_id=tipoingsal.id,
                usuario="Anonimo",
            )

            logger.info(f"Grupo creado: {tipoingsal.nombre}")

            dic_response["data"] = {
                "id": tipoingsal.id,
                "nombre": tipoingsal.nombre,
                "abreviatura": tipoingsal.abreviatura,
                "estado": estado.nombre,
            }
            dic_response["code"] = 201
            dic_response["status"] = "success"
            dic_response["message_user"] = "Tipoingsal creado exitosamente"
            dic_response["message"] = "Tipoingsal saved successfully"
            return JsonResponse(
                dic_response, safe=False, status=status.HTTP_201_CREATED
            )

        except DatabaseError as e:
            logger.error(f"Error al crear al Tipoingsal: {str(e)}")
            dic_response["message"] = "Error saving Tipoingsal"
            dic_response["message_user"] = "Error al guardar al Tipoingsal"
            return JsonResponse(
                dic_response, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            logger.error(f"Error inesperado al crear al grupo: {str(e)}")
            dic_response["message"] = "Unexpected error"
            dic_response["message_user"] = "Error inesperado al guardar al grupo"
            return JsonResponse(
                dic_response, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)


###TERMINAR
@api_view(["PUT"])
@transaction.atomic
def actualizar_tipoingsal(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error updating tipoingsal",
        "message_user": "Error al actualizar el tipoingsal",
        "data": [],
    }
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            estado_id = data.get("estado")
            estado = Estado.objects.get(id=estado_id)
            tipoingsal = Tipoingsal.objects.get(id=id)

            tipoingsal_existente = (
                Tipoingsal.objects.filter(
                    nombre=data.get("nombre"), abreviatura=data.get("abreviatura")
                )
                .exclude(id=id)
                .exclude(estado=3)  # 3: Eliminado
                .first()
            )

            if tipoingsal_existente:
                dic_response["message"] = "Ya existe un tipoingsal con los mismos datos"
                dic_response["message_user"] = (
                    "Ya existe un tipoingsal con los mismos datos"
                )
                return JsonResponse(
                    dic_response, safe=False, status=status.HTTP_400_BAD_REQUEST
                )

            # Datos antiguos (antes de la actualización)
            datos_anteriores = {
                "nombre": tipoingsal.nombre,
                "abreviatura": tipoingsal.abreviatura,
                "estado": tipoingsal.estado.nombre,
            }

            tipoingsal.nombre = data.get("nombre")
            tipoingsal.abreviatura = data.get("abreviatura")
            tipoingsal.estado = estado
            tipoingsal.save()

            # Datos nuevos (después de la actualización)
            datos_nuevos = {
                "nombre": tipoingsal.nombre,
                "abreviatura": tipoingsal.abreviatura,
                "estado": estado.nombre,
            }

            # Crear la sentencia de auditoría
            sentencia = (
                f"Se actualizó el tipoingsal."
                f" Los datos anteriores eran: nombre '{datos_anteriores['nombre']}', "
                f"abreviatura '{datos_anteriores['abreviatura']}', estado '{datos_anteriores['estado']}'."
                f" Los nuevos datos son: nombre '{datos_nuevos['nombre']}', "
                f"abreviatura '{datos_nuevos['abreviatura']}', estado '{datos_nuevos['estado']}'."
            )

            # Registrar evento de auditoría
            usuario = "Anonimo"
            Auditoria.registrar_evento(
                tabla="Tipoingsal",
                evento="Actualizar",
                sentencia=sentencia,
                registro_id=tipoingsal.id,
                usuario=usuario,
            )

            logger.info(f"Tipoingsal actualizado: {tipoingsal.nombre}")

            dic_response["code"] = 200
            dic_response["status"] = "success"
            dic_response["message_user"] = "Tipoingsal actualizado exitosamente"
            dic_response["message"] = "Tipoingsal updated successfully"
            dic_response["data"] = {
                "id": tipoingsal.id,
                "nombre": tipoingsal.nombre,
                "abreviatura": tipoingsal.abreviatura,
                "estado": estado.nombre,
            }

            return JsonResponse(dic_response, safe=False, status=status.HTTP_200_OK)
        except DatabaseError as e:
            logger.error(f"Error al actualizar el Tipoingsal: {str(e)}")
            dic_response["message"] = "Error updating tipoingsal"
            dic_response["message_user"] = "Error al actualizar el tipoingsal"
            return JsonResponse(
                dic_response, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Error inesperado al actualizar el tipoingsal: {str(e)}")
            dic_response["message"] = "Unexpected error"
            dic_response["message_user"] = (
                "Error inesperado al actualizar el tipoingsal"
            )
            return JsonResponse(
                dic_response, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@transaction.atomic
def eliminar_tipoingsal(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error deleting tipoingsal",
        "message_user": "Error al eliminar el tipoingsal",
        "data": [],
    }
    if request.method == "PATCH":
        try:
            tipoingsal = Tipoingsal.objects.get(id=id)
            estado_eliminado_id = 3  # Estado para 'Eliminado'

            # Verificar si el país ya está en estado 'Eliminado'
            if tipoingsal.estado_id == estado_eliminado_id:
                dic_response["message"] = "The tipoingsal is already deleted"
                dic_response["message_user"] = "El tipoingsal ya está eliminado"
                return JsonResponse(
                    dic_response, safe=False, status=status.HTTP_400_BAD_REQUEST
                )

            # Datos antes de la eliminación lógica
            datos_anteriores = {
                "nombre": tipoingsal.nombre,
                "abreviatura": tipoingsal.abreviatura,
                "estado": tipoingsal.estado.nombre,
            }

            # Realizar la eliminación lógica
            tipoingsal.estado_id = estado_eliminado_id
            tipoingsal.save()

            # Crear la sentencia de auditoría como una oración
            sentencia = (
                f"Se eliminó lógicamente el tipoingsal. "
                f"Datos eliminados: nombre '{datos_anteriores['nombre']}', "
                f"abreviatura '{datos_anteriores['abreviatura']}', estado '{datos_anteriores['estado']}'."
            )

            # Registrar el evento de auditoría
            usuario = (
                request.user.username if request.user.is_authenticated else "Anonimo"
            )
            Auditoria.registrar_evento(
                tabla="Tipoingsal",
                evento="Eliminar",
                sentencia=sentencia,
                registro_id=tipoingsal.id,
                usuario=usuario,
            )

            logger.info(f"Tipoingsal eliminado lógicamente: {tipoingsal.nombre}")

            dic_response["code"] = 200
            dic_response["status"] = "success"
            dic_response["message_user"] = "Tipoingsal eliminado lógicamente"
            dic_response["message"] = "Tipoingsal deleted logically"
            dic_response["data"] = {
                "id": tipoingsal.id,
                "nombre": tipoingsal.nombre,
                "abreviatura": tipoingsal.abreviatura,
                "estado": "Eliminado",
            }

            return JsonResponse(dic_response, status=status.HTTP_200_OK)

        except Tipoingsal.DoesNotExist:
            dic_response["message"] = "Tipoingsal not found"
            dic_response["message_user"] = "Tipoingsal no encontrado"
            return JsonResponse(
                dic_response, safe=False, status=status.HTTP_404_NOT_FOUND
            )

        except DatabaseError as e:
            logger.error(f"Error al eliminar el tipoingsal: {str(e)}")
            dic_response["message"] = "Error deleting tipoingsal"
            dic_response["message_user"] = "Error al eliminar el tipoingsal"
            return JsonResponse(
                dic_response, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            logger.error(f"Error inesperado al eliminar el tipoingsal: {str(e)}")
            dic_response["message"] = "Unexpected error"
            dic_response["message_user"] = "Error inesperado al eliminar el tipoingsal"
            return JsonResponse(
                dic_response, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return JsonResponse([], safe=False, status=status.HTTP_200_OK)
"""

# ------------------------------------------------------ CRUD TIPO MOVIMIENTO  -----------------------------------------------------------


@api_view(["GET"])
@transaction.atomic
def listar_tipomovimientos(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Movement type system not movement type",
        "message_user": "Tipo movimiento no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
        # Ejecutar la consulta SQL para obtener las empresas
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT m.id, m.nombre, m.abreviatura, 
                        e.nombre as empresa_nombre, t.nombre as tipo_ing_sal_nombre, 
                        TO_CHAR(m.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(m.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE 
                            WHEN m.estado_id = 3 THEN 'Eliminado'
                            WHEN m.estado_id = 2 THEN 'Inactivo'
                            ELSE 'Activo'
                        END as estado_nombre
                    FROM tipomovimiento m
                    LEFT JOIN empresa e ON m.empresa_id = e.id
                    LEFT JOIN tipoingsal t ON m.tipo_ing_sal_id = t.id
                    WHERE m.estado_id <> 3
                    ORDER BY m.id DESC
                """)
                movimientos = cursor.fetchall()

            # Serializar las empresas obtenidas
            movimiento_serializadas = [
                {
                    "id": m[0], "nombre": m[1], "abreviatura": m[2],
                    "empresa": m[3], "tipo_ing_sal": m[4], "fecha_creacion": m[5],
                    "fecha_modificacion": m[6], "estado": m[7]
                } for m in movimientos
            ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Tipo movimiento obtenidas correctamente",
                "message": "Tipo movimiento  obtenidas correctamente",
                "data": movimiento_serializadas
            })
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(f"Error al listar los tipo movimiento : {str(e)}")
            dic_response.update({"message": "Error al listar los tipo movimiento ", "data": str(e)})
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@transaction.atomic
def crear_tipomovimiento(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error creating movement type",
        "message_user": "Error al crear el tipo movimiento",
        "data": None,
    }
    
    if request.method == 'POST':
        try:
            # Deserialize request data using the serializer
            serializer = TipomovimientoSerializer(data=request.data)
            if serializer.is_valid():
                nombre = serializer.validated_data["nombre"]
                abreviatura = serializer.validated_data["abreviatura"]
                empresa_id = serializer.validated_data["empresa"].id
                tipo_ing_sal_id = serializer.validated_data["tipo_ing_sal"].id
                estado_id = 1
                fecha_creacion = datetime.now()
                fecha_modificacion = datetime.now()
                # Check if the country already exists
                
                with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Tipoingsal WHERE id = %s", [tipo_ing_sal_id])
                    tipo_ing_sal_nombre = cursor.fetchone()[0]
                        
                with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Empresa WHERE id = %s", [empresa_id])
                    empresa_nombre = cursor.fetchone()[0]
                        
                with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                    estado_nombre = cursor.fetchone()[0]
                
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*) FROM Tipomovimiento WHERE (nombre = %s OR abreviatura = %s) AND estado_id IN (1, 2)",
                        [nombre, abreviatura],
                    )
                    if cursor.fetchone()[0] > 0:
                        return JsonResponse({"message_user": "Ya existe un tipo movimiento con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)

                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO Tipomovimiento (nombre, abreviatura, empresa_id, tipo_ing_sal_id, estado_id, fecha_creacion, fecha_modificacion) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
                        [nombre, abreviatura, empresa_id, tipo_ing_sal_nombre, estado_id, fecha_creacion, fecha_modificacion]  # Assuming estado_id '1' means 'Activo'
                    )
                    tipomovimiento_id = cursor.fetchone()[0]

                Auditoria.registrar_evento(
                    tabla="Tipo movimiento",
                    evento="Crear",
                    sentencia=f"Tipo movimiento creada: {nombre} - {abreviatura} - {empresa_nombre} - {tipo_ing_sal_nombre} - {estado_nombre}",
                    registro_id=tipomovimiento_id,
                    usuario="Anonimo", 
                )
                
                dic_response.update(
                    {
                        "code": 201,
                        "status": "success",
                        "message_user": "Tipo movimiento creado exitosamente",
                        "message": "Movement type saved successfully",
                        "data": {"id": tipomovimiento_id, "nombre": nombre, "abreviatura": abreviatura, "empresa": empresa_nombre, "tipoingsal": tipo_ing_sal_nombre, "estado": estado_nombre},
                    }
                )
                logger.info(f"Tipo movimiento creado exitosamente: Movimiento '{nombre}' - abreviatura '{abreviatura}' - empresa '{empresa_nombre}' - tipoingsal '{tipo_ing_sal_nombre}' - estado '{estado_nombre}' (ID: {tipomovimiento_id})")
                return JsonResponse(dic_response, status=201)

            else:
                dic_response["message"] = "Datos inválidos."
                dic_response["data"] = serializer.errors
                return JsonResponse(dic_response, status=400)

        except Exception as e:
            logger.error(f"Error inesperado al crear el tipo movimiento: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
    
    return Response(dic_response, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@transaction.atomic
def actualizar_tipomovimiento(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error updating movement type",
        "message_user": "Error al actualizar el tipo de movimiento",
        "data": [],
    }

    if request.method == "PUT":
        try:
            tipomovimiento_data = json.loads(request.body)

            # Validar y convertir país y moneda a IDs
            for field, model, error_msg in [('empresa', Empresa, 'Empresa no encontrado'), ('tipo_ing_sal', Tipoingsal, 'Tipoingsal no encontrada')]:
                if isinstance(tipomovimiento_data.get(field), str):
                    obj = model.objects.filter(nombre=tipomovimiento_data[field]).first()
                    if obj:
                        tipomovimiento_data[field] = obj.id
                    else:
                        dic_response["message"] = f"{field.capitalize()} inválido."
                        dic_response["data"] = {field: error_msg}
                        return JsonResponse(dic_response, status=400)

            # Serializar y validar los datos
            serializer = TipomovimientoSerializer(data=tipomovimiento_data, partial=True)
            if not serializer.is_valid():
                dic_response.update({"message_user": "Datos inválidos.", "data": serializer.errors})
                return JsonResponse(dic_response, status=400)

            # Verificar existencia de la empresa
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Tipomovimiento WHERE id = %s", [id])
                if cursor.fetchone()[0] == 0:
                    dic_response["message_user"] = "La tipo movimiento no existe."
                    return JsonResponse(dic_response, status=400)

            # Verificar si ya existe otra empresa con el mismo nombre, abreviatura o RUC
            with connection.cursor() as cursor:
                cursor.execute(
                    """ SELECT COUNT(*) FROM Tipomovimiento 
                        WHERE (nombre = %s OR abreviatura = %s) 
                        AND estado_id IN (1, 2)
                        AND id != %s""",
                    [serializer.validated_data["nombre"], serializer.validated_data["abreviatura"], id]
                )
                if cursor.fetchone()[0] > 0:
                        return JsonResponse({"message_user": "Ya existe un tipo movimiento con el mismo nombre o abreviatura.", "message": "Ya hay un dato existente."}, status=400)

            # Actualizar empresa
            
            validated_data = serializer.validated_data
            empresa_id = validated_data.get("empresa").id
            tipo_ing_sal_id = validated_data.get("tipo_ing_sal").id
            estado_id = validated_data.get("estado").id
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Empresa WHERE id = %s", [empresa_id])
                    empresa_nombre = cursor.fetchone()[0]
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Tipoingsal WHERE id = %s", [tipo_ing_sal_id])
                    tipo_ing_sal_nombre = cursor.fetchone()[0]
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                    estado_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE Tipomovimiento SET nombre = %s, abreviatura = %s, empresa_id = %s, 
                        tipo_ing_sal_id = %s, estado_id = %s, fecha_modificacion = %s WHERE id = %s""",
                    [
                        serializer.validated_data["nombre"], serializer.validated_data["abreviatura"],
                        serializer.validated_data["empresa"].id, serializer.validated_data["tipo_ing_sal"].id,
                        serializer.validated_data["estado"].id, datetime.now(), id
                    ],
                )

            # Registrar auditoría
            Auditoria.registrar_evento(
                tabla="Tipo movimiento", evento="Actualizar", 
                sentencia=f"Tipo movimiento actualizada: {serializer.validated_data['nombre']} - {serializer.validated_data['abreviatura']} - {empresa_nombre} - [{tipo_ing_sal_nombre}] - {estado_nombre}",
                registro_id=id, usuario="Anonimo"
            )

            dic_response.update({
                "code": 200,
                "status": "success",
                "message": "Movement type updated successfully",
                "message_user": "Tipo movimiento actualizada exitosamente",
                "data": serializer.data
            })
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            dic_response.update({"message_user": "Error inesperado", "data": {"error": str(e)}})
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)

@api_view(["PATCH"])
@transaction.atomic
def eliminar_tipomovimiento(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error deleting movement type",
        "message_user": "Error al eliminar el tipo movimiento",
        "data": [],
    }

    if request.method == "PATCH":
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT estado_id FROM Tipomovimiento WHERE id = %s", [id])
                resultado = cursor.fetchone()

                if not resultado:
                    dic_response["message"] = "Tipo movimiento no encontrada."
                    return JsonResponse(dic_response, status=404)

                if resultado[0] == 3:  # Estado "Eliminado"
                    dic_response["message"] = " El tipo movimiento ya está eliminada."
                    return JsonResponse(dic_response, status=400)

                # Actualizar estado a "Eliminado"
                cursor.execute("UPDATE Tipomovimiento SET estado_id = 3, fecha_modificacion = %s WHERE id = %s", [datetime.now(), id])

            movimiento = Tipomovimiento.objects.get(id=id)

            Auditoria.registrar_evento(
                tabla="Tipo movimiento",
                evento="Eliminar",
                sentencia=f"Se eliminó lógicamente el tipo movimiento con id: {id}.",
                registro_id=id,
                usuario="Anonimo",  # Aquí puedes pasar el usuario real si está disponible
            )

            serializer = TipomovimientoSerializer(movimiento)
            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Tipo movimiento eliminada lógicamente",
                "message": "Movement type deleted logically",
                "data": serializer.data,
            })

            logger.info(f"Tipo movimiento eliminada lógicamente: ID {id}")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar el tipo movimiento: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)

# ------------------------------------------------------ CRUD TIPO DOCUMENTO -----------------------------------------------------------


@api_view(["GET"])
@transaction.atomic
def listar_tipodocumentos(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Document type system not document type",
        "message_user": "Tipo documento no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
        # Ejecutar la consulta SQL para obtener las empresas
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT d.id, d.nombre, d.abreviatura, 
                        e.nombre as empresa_nombre, t.nombre as tipo_ing_sal_nombre, 
                        TO_CHAR(d.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(d.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE 
                            WHEN d.estado_id = 3 THEN 'Eliminado'
                            WHEN d.estado_id = 2 THEN 'Inactivo'
                            ELSE 'Activo'
                        END as estado_nombre
                    FROM tipodocumento d
                    LEFT JOIN empresa e ON d.empresa_id = e.id
                    LEFT JOIN tipoingsal t ON d.tipo_ing_sal_id = t.id
                    WHERE d.estado_id <> 3
                    ORDER BY d.id DESC
                """)
                documentos = cursor.fetchall()

            # Serializar las empresas obtenidas
            documento_serializadas = [
                {
                    "id": d[0], "nombre": d[1], "abreviatura": d[2],
                    "empresa": d[3], "tipo_ing_sal": d[4], "fecha_creacion": d[5],
                    "fecha_modificacion": d[6], "estado": d[7]
                } for d in documentos
            ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Tipo documento obtenidas correctamente",
                "message": "Tipo documento  obtenidas correctamente",
                "data": documento_serializadas
            })
            return JsonResponse(dic_response, status=200)

        except DatabaseError as e:
            logger.error(f"Error al listar los tipo documento : {str(e)}")
            dic_response.update({"message": "Error al listar los tipo documento ", "data": str(e)})
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@transaction.atomic
def crear_tipodocumento(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error creating document type",
        "message_user": "Error al crear el tipo documento",
        "data": None,
    }
    
    if request.method == 'POST':
        try:
            # Deserialize request data using the serializer
            serializer = TipodocumentoSerializer(data=request.data)
            if serializer.is_valid():
                nombre = serializer.validated_data["nombre"]
                abreviatura = serializer.validated_data["abreviatura"]
                empresa_id = serializer.validated_data["empresa"].id
                tipo_ing_sal_id = serializer.validated_data["tipo_ing_sal"].id
                estado_id = 1
                fecha_creacion = datetime.now()
                fecha_modificacion = datetime.now()
                # Check if the country already exists
                
                
                with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Tipoingsal WHERE id = %s", [tipo_ing_sal_id])
                    tipo_ing_sal_nombre = cursor.fetchone()[0]
                        
                with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Empresa WHERE id = %s", [empresa_id])
                    empresa_nombre = cursor.fetchone()[0]
                        
                with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                    estado_nombre = cursor.fetchone()[0]
                    
                    
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*) FROM Tipodocumento WHERE (nombre = %s OR abreviatura = %s) AND estado_id IN (1, 2)",
                        [nombre, abreviatura],
                    )
                    if cursor.fetchone()[0] > 0:
                        return JsonResponse({"message_user": "Ya existe un tipo documento con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)

                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO Tipodocumento (nombre, abreviatura, empresa_id, tipo_ing_sal_id, estado_id, fecha_creacion, fecha_modificacion) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
                        [nombre, abreviatura, empresa_id, tipo_ing_sal_id, estado_id, fecha_creacion, fecha_modificacion]  # Assuming estado_id '1' means 'Activo'
                    )
                    tipodocumento_id = cursor.fetchone()[0]

                Auditoria.registrar_evento(
                    tabla="Tipo documento",
                    evento="Crear",
                    sentencia=f"Tipo documento creada: {nombre} - {abreviatura} - {empresa_nombre} -  {tipo_ing_sal_nombre} - {estado_nombre}",
                    registro_id=tipodocumento_id,
                    usuario="Anonimo", 
                )
                
                dic_response.update(
                    {
                        "code": 201,
                        "status": "success",
                        "message_user": "Tipo documento creado exitosamente",
                        "message": "Document type saved successfully",
                        "data": {"id": tipodocumento_id, "nombre": nombre, "abreviatura": abreviatura, "empresa": empresa_nombre, "tipoingsal": tipo_ing_sal_nombre, "estado": estado_nombre},
                    }
                )
                logger.info(f"Tipo documento creado exitosamente: documento '{nombre}' - abreviatura '{abreviatura}' - empresa '{empresa_nombre}' - tipoingsal '{tipo_ing_sal_nombre}' - estado '{estado_nombre}'(ID: {tipodocumento_id})")
                return JsonResponse(dic_response, status=201)

            else:
                dic_response["message"] = "Datos inválidos."
                dic_response["data"] = serializer.errors
                return JsonResponse(dic_response, status=400)

        except Exception as e:
            logger.error(f"Error inesperado al crear el tipo documento: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
    
    return Response(dic_response, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@transaction.atomic
def actualizar_tipodocumento(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error updating document type",
        "message_user": "Error al actualizar el tipo de documento",
        "data": [],
    }

    if request.method == "PUT":
        try:
            tipodocumento_data = json.loads(request.body)

            # Validar y convertir país y moneda a IDs
            for field, model, error_msg in [('empresa', Empresa, 'Empresa no encontrado'), ('tipo_ing_sal', Tipoingsal, 'Tipoingsal no encontrada')]:
                if isinstance(tipodocumento_data.get(field), str):
                    obj = model.objects.filter(nombre=tipodocumento_data[field]).first()
                    if obj:
                        tipodocumento_data[field] = obj.id
                    else:
                        dic_response["message"] = f"{field.capitalize()} inválido."
                        dic_response["data"] = {field: error_msg}
                        return JsonResponse(dic_response, status=400)

            # Serializar y validar los datos
            serializer = TipodocumentoSerializer(data=tipodocumento_data, partial=True)
            if not serializer.is_valid():
                dic_response.update({"message_user": "Datos inválidos.", "data": serializer.errors})
                return JsonResponse(dic_response, status=400)

            # Verificar existencia de la empresa
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Tipodocumento WHERE id = %s", [id])
                if cursor.fetchone()[0] == 0:
                    dic_response["message_user"] = "La tipo documento no existe."
                    return JsonResponse(dic_response, status=400)

            # Verificar si ya existe otra empresa con el mismo nombre, abreviatura o RUC
            with connection.cursor() as cursor:
                cursor.execute(
                    """ SELECT COUNT(*) FROM Tipodocumento 
                        WHERE (nombre = %s OR abreviatura = %s) 
                        AND estado_id IN (1, 2)
                        AND id != %s""",
                    [serializer.validated_data["nombre"], serializer.validated_data["abreviatura"], id]
                )
                if cursor.fetchone()[0] > 0:
                        return JsonResponse({"message_user": "Ya existe un tipo documento con el mismo nombre o abreviatura.", "message": "Ya hay un dato existente."}, status=400)

            # Actualizar empresa
            
            validated_data = serializer.validated_data
            empresa_id = validated_data.get("empresa").id
            tipo_ing_sal_id = validated_data.get("tipo_ing_sal").id
            estado_id = validated_data.get("estado").id
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Empresa WHERE id = %s", [empresa_id])
                    empresa_nombre = cursor.fetchone()[0]
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Tipoingsal WHERE id = %s", [tipo_ing_sal_id])
                    tipo_ing_sal_nombre = cursor.fetchone()[0]
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                    estado_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE Tipodocumento SET nombre = %s, abreviatura = %s, empresa_id = %s, 
                        tipo_ing_sal_id = %s, estado_id = %s, fecha_modificacion = %s WHERE id = %s""",
                    [
                        serializer.validated_data["nombre"], serializer.validated_data["abreviatura"],
                        serializer.validated_data["empresa"].id, serializer.validated_data["tipo_ing_sal"].id,
                        serializer.validated_data["estado"].id, datetime.now(), id
                    ],
                )

            # Registrar auditoría
            Auditoria.registrar_evento(
                tabla="Tipo documento", evento="Actualizar", 
                sentencia=f"Tipo documento actualizada: {serializer.validated_data['nombre']} - {serializer.validated_data['abreviatura']} - {empresa_nombre} - [{tipo_ing_sal_nombre}] - {estado_nombre}",
                registro_id=id, usuario="Anonimo"
            )

            dic_response.update({
                "code": 200,
                "status": "success",
                "message": "Document type updated successfully",
                "message_user": "Tipo documento actualizada exitosamente",
                "data": serializer.data
            })
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            dic_response.update({"message_user": "Error inesperado", "data": {"error": str(e)}})
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)


@api_view(["PATCH"])
@transaction.atomic
def eliminar_tipodocumento(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error deleting document type",
        "message_user": "Error al eliminar el tipo documento",
        "data": [],
    }

    if request.method == "PATCH":
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT estado_id FROM Tipodocumento WHERE id = %s", [id])
                resultado = cursor.fetchone()

                if not resultado:
                    dic_response["message"] = "Tipo documento no encontrada."
                    return JsonResponse(dic_response, status=404)

                if resultado[0] == 3:  # Estado "Eliminado"
                    dic_response["message"] = " El tipo documento ya está eliminada."
                    return JsonResponse(dic_response, status=400)

                # Actualizar estado a "Eliminado"
                cursor.execute("UPDATE Tipodocumento SET estado_id = 3, fecha_modificacion = %s WHERE id = %s", [datetime.now(), id])

            documento = Tipodocumento.objects.get(id=id)

            Auditoria.registrar_evento(
                tabla="Tipo documento",
                evento="Eliminar",
                sentencia=f"Se eliminó lógicamente el tipo documento con id: {id}.",
                registro_id=id,
                usuario="Anonimo",  # Aquí puedes pasar el usuario real si está disponible
            )

            serializer = TipodocumentoSerializer(documento)
            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Tipo documento eliminada lógicamente",
                "message": "Document type deleted logically",
                "data": serializer.data,
            })

            logger.info(f"Tipo documento eliminada lógicamente: ID {id}")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar el tipo documento: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)

# --------------------------------------------------- AGRICOLA -------------------------------------------------------
# ------------------------------------------------------ CRUD CAMPAÑIA -----------------------------------------------------------


@api_view(["GET"])
@transaction.atomic
def listar_campanias(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Campaigns system not found",
        "message_user": "Campañas no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT c.id, c.nombre, c.abreviatura, 
                        TO_CHAR(c.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(c.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE WHEN c.estado_id = 3 THEN 'Eliminado'
                                WHEN c.estado_id = 2 THEN 'Inactivo'
                                ELSE 'Activo' 
                        END as estado_nombre
                    FROM campania c
                    WHERE c.estado_id <> 3
                    ORDER BY c.id DESC
                """)
            
                campanias = cursor.fetchall()
                campanias_serializados = [
                    {**CampaniaSerializer(Campania(
                        id=c[0], nombre=c[1], abreviatura=c[2],
                        fecha_creacion=c[3], fecha_modificacion=c[4]
                    )).data, 'estado': c[5]} for c in campanias
                ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Campañas obtenidos correctamente",
                "message": "Campañas obtenids correctamente",
                "data": campanias_serializados,
            })
            return JsonResponse(dic_response, status=200, safe=False)

        except DatabaseError as e:
            logger.error(f"Error al listar las campañas: {str(e)}")
            return JsonResponse({"mensaje": "Error al listar las campañas."}, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@transaction.atomic
def crear_campania(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error creating campaigns",
        "message_user": "Error al crear la campaña",
        "data": [],
    }
    
    if request.method == 'POST':
        try:
            # Deserialize request data using the serializer
            serializer = CampaniaSerializer(data=request.data)
            if not serializer.is_valid():
                return JsonResponse({"message": "Datos inválidos.", "data": serializer.errors}, status=400)
            
            nombre = serializer.validated_data["nombre"]
            abreviatura = serializer.validated_data["abreviatura"]
            estado_id = 1
            fecha_actual = datetime.now()
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                    estado_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM Campania WHERE (nombre = %s OR abreviatura = %s) AND estado_id IN (1, 2)",
                    [nombre, abreviatura]
                    )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe una campaña con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)
            
    
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Campania (nombre, abreviatura, estado_id, fecha_creacion, fecha_modificacion) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                    [nombre, abreviatura, estado_id, fecha_actual, fecha_actual]
                )
                campania_id = cursor.fetchone()[0]

            Auditoria.registrar_evento(
                tabla="Campaña", evento="Crear",
                sentencia=f"Campaña creada: {nombre} - {abreviatura}", registro_id=campania_id,
                usuario="Anonimo"
            )

            dic_response.update({
                "code": 201,
                "status": "success",
                "message_user": "Campaigns creado exitosamente",
                "message": "Supplier saved successfully",
                "data": {"id": campania_id, "nombre": nombre, "abreviatura": abreviatura, "estado": estado_nombre},
            })
            logger.info(f"Campaña creado: nombre '{nombre}' - abreviatura '{abreviatura}' - estado '{estado_nombre}' (ID: {campania_id})")
            return JsonResponse(dic_response, status=201)

        except Exception as e:
            logger.error(f"Error inesperado al crear la campaña: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
    
    return Response([], status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@transaction.atomic
def actualizar_campania(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error updating campaigns",
        "message_user": "Error al actualizar la campaña",
        "data": [],
    }

    if request.method == "PUT":
        try:
            campania_data = json.loads(request.body)

            serializer = CampaniaSerializer(data=campania_data, partial=True)
            if not serializer.is_valid():
                return JsonResponse({"message_user": "Datos inválidos.", "data": serializer.errors}, status=400)

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Campania WHERE id = %s", [id])         
                if cursor.fetchone()[0] == 0:
                    return JsonResponse({"message_user": "La campaña no existe."}, status=400)

            # Verificar duplicado de nombre y abreviatura
            with connection.cursor() as cursor:
                cursor.execute(
                        """
                            SELECT COUNT(*) 
                            FROM Campania 
                            WHERE (nombre = %s OR abreviatura = %s) 
                            AND estado_id IN (1, 2)
                            AND id != %s  -- Excluir el registro actual del chequeo
                            """,
                        [serializer.validated_data["nombre"], serializer.validated_data["abreviatura"], id]
                )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe una campaña con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)

            validated_data = serializer.validated_data
            
            estado_id = validated_data.get("estado").id
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                    estado_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Campania SET nombre=%s, abreviatura=%s, estado_id=%s, fecha_modificacion=%s WHERE id=%s",
                    [validated_data.get("nombre"), validated_data.get("abreviatura"),
                    validated_data.get("estado").id, datetime.now(), id]
                )

            # Registrar auditoría
            Auditoria.registrar_evento(
                tabla="Campaña", evento="Actualizar",
                sentencia=f"Campaña actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {estado_nombre}",
                registro_id=id, usuario="Anonimo"
            )

            dic_response.update({
                "code": 200, "status": "success",
                "message": "Campaigns updated successfully",
                "message_user": "Campaña actualizado exitosamente",
                "data": serializer.data,
            })

            logger.info(f"Campaña actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {estado_nombre} (ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al actualizar la campaña: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)


@api_view(["PATCH"])
@transaction.atomic
def eliminar_campania(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error deleting campaigns",
        "message_user": "Error al eliminar la campaña",
        "data": [],
    }

    if request.method == "PATCH":
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT estado_id FROM Campania WHERE id = %s", [id])
                resultado = cursor.fetchone()

            if not resultado:
                dic_response["message_user"] = "Campaña no encontrado."
                return JsonResponse(dic_response, status=404)

            if resultado[0] == 3:  # 3: Eliminado
                dic_response["message_user"] = "La campanña ya está eliminado."
                return JsonResponse(dic_response, status=400)

            # Actualizar el estado a 'Eliminado'
            fecha_modificacion = datetime.now()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Campania SET estado_id = 3, fecha_modificacion = %s WHERE id = %s",
                    [fecha_modificacion, id],
                )
                
            campania = Campania.objects.get(id=id)
            Auditoria.registrar_evento(
                tabla="Campaña",
                evento="Eliminar",
                sentencia=f"Se eliminó lógicamente la campaña con id: {id}.",
                registro_id=id,
                usuario="Anonimo",  
            )

            serializer = CampaniaSerializer(campania)
            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Campaña eliminado lógicamente",
                    "message": "Campaigns deleted logically",
                    "data": serializer.data,
                }
            )
        
            logger.info(f"Campaña eliminado logicamente: (ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar la campaña: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)


# ------------------------------------------------------ CRUD CULTIVO -----------------------------------------------------------

@api_view(["GET"])
@transaction.atomic
def listar_cultivos(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Crops system not found",
        "message_user": "Crops no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT c.id, c.nombre, c.abreviatura, 
                        TO_CHAR(c.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(c.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE WHEN c.estado_id = 3 THEN 'Eliminado'
                                WHEN c.estado_id = 2 THEN 'Inactivo'
                                ELSE 'Activo' 
                        END as estado_nombre
                    FROM cultivo c
                    WHERE c.estado_id <> 3
                    ORDER BY c.id DESC
                """)
            
                cultivos = cursor.fetchall()
                cultivo_serializados = [
                    {**CultivoSerializer(Cultivo(
                        id=c[0], nombre=c[1], abreviatura=c[2],
                        fecha_creacion=c[3], fecha_modificacion=c[4]
                    )).data, 'estado': c[5]} for c in cultivos
                ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Cultivos obtenidos correctamente",
                "message": "Cultivos obtenidos correctamente",
                "data": cultivo_serializados,
            })
            return JsonResponse(dic_response, status=200, safe=False)

        except DatabaseError as e:
            logger.error(f"Error al listar los cultivos: {str(e)}")
            return JsonResponse({"mensaje": "Error al listar los cultivos."}, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@transaction.atomic
def crear_cultivo(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error creating cultivation",
        "message_user": "Error al crear el cultivo",
        "data": [],
    }
    
    if request.method == 'POST':
        try:
            # Deserialize request data using the serializer
            serializer = CultivoSerializer(data=request.data)
            if not serializer.is_valid():
                return JsonResponse({"message": "Datos inválidos.", "data": serializer.errors}, status=400)
            
            nombre = serializer.validated_data["nombre"]
            abreviatura = serializer.validated_data["abreviatura"]
            estado_id = 1
            fecha_actual = datetime.now()
            
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                    estado_nombre = cursor.fetchone()[0]

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM Cultivo WHERE (nombre = %s OR abreviatura = %s) AND estado_id IN (1, 2)",
                    [nombre, abreviatura]
                    )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe un cultvo con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)
            
    
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Cultivo (nombre, abreviatura, estado_id, fecha_creacion, fecha_modificacion) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                    [nombre, abreviatura, estado_id, fecha_actual, fecha_actual]
                )
                campania_id = cursor.fetchone()[0]

            Auditoria.registrar_evento(
                tabla="Cultivo", evento="Crear",
                sentencia=f"Cultivo creada: {nombre} - {abreviatura} - {estado_nombre}", registro_id=campania_id,
                usuario="Anonimo"
            )

            dic_response.update({
                "code": 201,
                "status": "success",
                "message_user": "Cultivo creado exitosamente",
                "message": "Cultivation saved successfully",
                "data": {"id": campania_id, "nombre": nombre, "abreviatura": abreviatura, "estado": estado_nombre},
            })
            logger.info(f"Cultivo creado: nombre '{nombre}' - abreviatura '{abreviatura}' - estado '{estado_nombre}' (ID: {campania_id})")
            return JsonResponse(dic_response, status=201)

        except Exception as e:
            logger.error(f"Error inesperado al crear el cultivo: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
    
    return Response([], status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@transaction.atomic
def actualizar_cultivo(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error updating cultivation",
        "message_user": "Error al actualizar el cultivo",
        "data": [],
    }

    if request.method == "PUT":
        try:
            cultivo_data = json.loads(request.body)

            serializer = CampaniaSerializer(data=cultivo_data, partial=True)
            if not serializer.is_valid():
                return JsonResponse({"message_user": "Datos inválidos.", "data": serializer.errors}, status=400)

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Cultivo WHERE id = %s", [id])         
                if cursor.fetchone()[0] == 0:
                    return JsonResponse({"message_user": "El cultivo no existe."}, status=400)

            # Verificar duplicado de nombre y abreviatura
            with connection.cursor() as cursor:
                cursor.execute(
                        """
                            SELECT COUNT(*) 
                            FROM Cultivo 
                            WHERE (nombre = %s OR abreviatura = %s) 
                            AND estado_id IN (1, 2)
                            AND id != %s  -- Excluir el registro actual del chequeo
                            """,
                        [serializer.validated_data["nombre"], serializer.validated_data["abreviatura"], id]
                )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe un cultivo con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)

            validated_data = serializer.validated_data
            
            estado_id = validated_data.get("estado").id
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                    estado_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Cultivo SET nombre=%s, abreviatura=%s, estado_id=%s, fecha_modificacion=%s WHERE id=%s",
                    [validated_data.get("nombre"), validated_data.get("abreviatura"),
                    validated_data.get("estado").id, datetime.now(), id]
                )

            # Registrar auditoría
            Auditoria.registrar_evento(
                tabla="Cultivo", evento="Actualizar",
                sentencia=f"Cultivo actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {estado_nombre}",
                registro_id=id, usuario="Anonimo"
            )

            dic_response.update({
                "code": 200, "status": "success",
                "message": "Cultivation updated successfully",
                "message_user": "Cultivo actualizado exitosamente",
                "data": serializer.data,
            })

            logger.info(f"Cultivo actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {estado_nombre}(ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al actualizar el cultivo: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)


@api_view(["PATCH"])
@transaction.atomic
def eliminar_cultivo(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error deleting cultivation",
        "message_user": "Error al eliminar el cultivo",
        "data": [],
    }

    if request.method == "PATCH":
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT estado_id FROM Cultivo WHERE id = %s", [id])
                resultado = cursor.fetchone()

            if not resultado:
                dic_response["message_user"] = "Cultivo no encontrado."
                return JsonResponse(dic_response, status=404)

            if resultado[0] == 3:  # 3: Eliminado
                dic_response["message_user"] = "El cultivo ya está eliminado."
                return JsonResponse(dic_response, status=400)

            # Actualizar el estado a 'Eliminado'
            fecha_modificacion = datetime.now()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Cultivo SET estado_id = 3, fecha_modificacion = %s WHERE id = %s",
                    [fecha_modificacion, id],
                )
                
            cultivo = Cultivo.objects.get(id=id)
            Auditoria.registrar_evento(
                tabla="Cultivo",
                evento="Eliminar",
                sentencia=f"Se eliminó lógicamente el cultivo con id: {id}.",
                registro_id=id,
                usuario="Anonimo",  
            )

            serializer = CultivoSerializer(cultivo)
            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Cultivo eliminado lógicamente",
                    "message": "Cultivation deleted logically",
                    "data": serializer.data,
                }
            )
        
            logger.info(f"Cultivo eliminado logicamente: (ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar el cultivo: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)


# ------- PARA SELECCIONAR LOS ACTIVOS 
@api_view(["GET"])
@transaction.atomic
def listar_cultivos_activos(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Cultivos activos no encontradas",
        "message_user": "Cultivos activos no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT c.id, c.nombre, c.abreviatura, 
                        TO_CHAR(c.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(c.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE WHEN c.estado_id = 3 THEN 'Eliminado'
                                WHEN c.estado_id = 2 THEN 'Inactivo'
                                ELSE 'Activo' 
                        END as estado_nombre
                    FROM cultivo c
                    WHERE c.estado_id = 1
                    ORDER BY c.id DESC
                """)
            
                cultivos = cursor.fetchall()
                cultivo_serializados = [
                    {**CultivoSerializer(Cultivo(
                        id=c[0], nombre=c[1], abreviatura=c[2],
                        fecha_creacion=c[3], fecha_modificacion=c[4]
                    )).data, 'estado': c[5]} for c in cultivos
                ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Cultivos activos obtenidos correctamente",
                "message": "Cultivos activos obtenidos correctamente",
                "data": cultivo_serializados,
            })
            return JsonResponse(dic_response, status=200, safe=False)

        except DatabaseError as e:
            logger.error(f"Error al listar los cultivos activos: {str(e)}")
            return JsonResponse({"mensaje": "Error al listar los cultivos activos."}, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------ CRUD VARIEDAD -----------------------------------------------------------


@api_view(["GET"])
@transaction.atomic
def listar_variedades(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Varieties system not found",
        "message_user": "Variedades no encontradas",
        "data": [],
    }

    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT v.id, v.nombre, v.abreviatura, 
                        c.nombre as cultivo_nombre, 
                        TO_CHAR(v.fecha_creacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_creacion,
                        TO_CHAR(v.fecha_modificacion, 'YYYY-MM-DD HH24:MI:SS') as fecha_modificacion,
                        CASE WHEN v.estado_id = 3 THEN 'Eliminado'
                                WHEN v.estado_id = 2 THEN 'Inactivo'
                                ELSE 'Activo' 
                        END as estado_nombre
                    FROM variedad v
                    LEFT JOIN cultivo c ON v.cultivo_id = c.id
                    WHERE v.estado_id <> 3
                    ORDER BY v.id DESC
                """)
            
                variedad = cursor.fetchall()
                variedades_serializados = [
                    {**VariedadSerializer(Variedad(
                        id=v[0], nombre=v[1], abreviatura=v[2], cultivo_id=v[3],
                        fecha_creacion=v[4], fecha_modificacion=v[5]
                    )).data, 'estado': v[6]} for v in variedad
                ]

            dic_response.update({
                "code": 200,
                "status": "success",
                "message_user": "Variedades obtenidos correctamente",
                "message": "Variedades obtenidos correctamente",
                "data": variedades_serializados,
            })
            return JsonResponse(dic_response, status=200, safe=False)

        except DatabaseError as e:
            logger.error(f"Error al listar las variedades: {str(e)}")
            return JsonResponse({"mensaje": "Error al listar las variedades."}, status=500)

    return JsonResponse([], safe=False, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@transaction.atomic
def crear_variedad(request):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error creating varieties",
        "message_user": "Error al crear la variedad",
        "data": None,
    }
    
    if request.method == 'POST':
        try:
            # Deserialize request data using the serializer
            serializer = VariedadSerializer(data=request.data)
            if not serializer.is_valid():
                return JsonResponse({"message": "Datos inválidos.", "data": serializer.errors}, status=400)
            
            nombre = serializer.validated_data["nombre"]
            abreviatura = serializer.validated_data["abreviatura"]
            cultivo_id = serializer.validated_data["cultivo"].id
            estado_id = 1
            fecha_actual = datetime.now()
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Cultivo WHERE id = %s", [cultivo_id])
                    cultivo_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                    estado_nombre = cursor.fetchone()[0]
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM Variedad WHERE (nombre = %s OR abreviatura = %s) AND estado_id IN (1, 2)",
                    [nombre, abreviatura]
                )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe una variedad con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Variedad (nombre, abreviatura, cultivo_id, estado_id, fecha_creacion, fecha_modificacion) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                    [nombre, abreviatura, cultivo_id, estado_id, fecha_actual, fecha_actual]
                )
                variedad_id = cursor.fetchone()[0]

            Auditoria.registrar_evento(
                tabla="Variedad", evento="Crear",
                sentencia=f"Variedad creada: {nombre} - {abreviatura} - {cultivo_nombre} - {estado_nombre}", registro_id=variedad_id,
                usuario="Anonimo"
            )

            dic_response.update({
                "code": 201,
                "status": "success",
                "message_user": "Variedad creado exitosamente",
                "message": "Variedad saved successfully",
                "data": {"id": variedad_id, "nombre": nombre, "abreviatura": abreviatura, "cultivo": cultivo_nombre, "estado": estado_nombre},
            })
            logger.info(f"Variedad creada: nombre '{nombre}' - abreviatura '{abreviatura}' - cultivo '{cultivo_nombre}' - estado '{estado_nombre}' (ID: {variedad_id})")
            return JsonResponse(dic_response, status=201)

        except Exception as e:
            logger.error(f"Error inesperado al crear la variedad: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)
    
    return Response(dic_response, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@transaction.atomic
def actualizar_variedad(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error updating varieties",
        "message_user": "Error al actualizar la variedad",
        "data": [],
    }

    if request.method == "PUT":
        try:
            variedad_data = json.loads(request.body)

            # Validar y asignar país
            if isinstance(variedad_data.get('cultivo'), str):
                cultivo_obj = Cultivo.objects.filter(nombre=variedad_data['cultivo']).first()
                if not cultivo_obj:
                    return JsonResponse({"message_user": "Cultivo inválido.", "data": {"cultivo": "Cultivo no encontrado."}}, status=400)
                variedad_data['cultivo'] = cultivo_obj.id

            serializer = VariedadSerializer(data=variedad_data, partial=True)
            if not serializer.is_valid():
                return JsonResponse({"message_user": "Datos inválidos.", "data": serializer.errors}, status=400)
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Variedad WHERE id = %s", [id])
                if cursor.fetchone()[0] == 0:
                    return JsonResponse({"message_user": "La variedad no existe."}, status=400)
            
            with connection.cursor() as cursor:
                cursor.execute(
                    """ SELECT COUNT(*) FROM Variedad WHERE (nombre = %s OR abreviatura = %s) AND estado_id IN (1, 2) AND id != %s""",
                    [serializer.validated_data["nombre"], serializer.validated_data["abreviatura"], id]
                )
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({"message_user": "Ya existe una variedad con el mismo nombre o abreviatura", "message": "Ya hay un dato existente."}, status=400)

            validated_data = serializer.validated_data
            
            cultivo_id = validated_data.get("cultivo").id
            estado_id = validated_data.get("estado").id
            
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Cultivo WHERE id = %s", [cultivo_id])
                    cultivo_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                    cursor.execute("SELECT nombre FROM Estado WHERE id = %s", [estado_id])
                    estado_nombre = cursor.fetchone()[0]
                    
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Variedad SET nombre=%s, abreviatura=%s, cultivo_id=%s, estado_id=%s, fecha_modificacion=%s WHERE id=%s",
                    [validated_data.get("nombre"), validated_data.get("abreviatura"), validated_data.get("cultivo").id,
                    validated_data.get("estado").id, datetime.now(), id]
                )

            Auditoria.registrar_evento(
                tabla="Variedad", evento="Actualizar",
                sentencia=f"Variedad actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {cultivo_nombre} - {estado_nombre}",
                registro_id=id, usuario="Anonimo"
            )

            dic_response.update({
                "code": 200, "status": "success",
                "message": "Variedad actualizado exitosamente",
                "message_user": "Variedad actualizado exitosamente",
                "data": serializer.data,
            })

            logger.info(f"Variedad actualizado: {validated_data['nombre']} - {validated_data['abreviatura']} - {cultivo_nombre} - {estado_nombre} (ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            return JsonResponse({"message": "Error inesperado"}, status=500)

    return JsonResponse([], status=200)

@api_view(["PATCH"])
@transaction.atomic
def eliminar_variedad(request, id):
    dic_response = {
        "code": 400,
        "status": "error",
        "message": "Error al eliminar la variedad",
        "message_user": "Error al eliminar la variedad",
        "data": [],
    }

    if request.method == "PATCH":
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT estado_id FROM Variedad WHERE id = %s", [id])
                resultado = cursor.fetchone()

            if not resultado:
                dic_response["message"] = "Variedad no encontrado."
                return JsonResponse(dic_response, status=404)

            if resultado[0] == 3:  # 3: Eliminado
                dic_response["message"] = "La variedad ya está eliminado."
                return JsonResponse(dic_response, status=400)

            # Actualizar el estado a 'Eliminado'
            fecha_modificacion = datetime.now()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Variedad SET estado_id = 3, fecha_modificacion = %s WHERE id = %s",
                    [fecha_modificacion, id],
                )

            variedad = Variedad.objects.get(id=id)
            Auditoria.registrar_evento(
                tabla="Variedad",
                evento="Eliminar",
                sentencia=f"Se eliminó lógicamente la variedad con id: {id}.",
                registro_id=id,
                usuario="Anonimo",  # Reemplazar con el usuario actual si está disponible
            )

            serializer = VariedadSerializer(variedad)
            dic_response.update(
                {
                    "code": 200,
                    "status": "success",
                    "message_user": "Variedad eliminado lógicamente",
                    "message": "Variedad eliminado lógicamente",
                    "data": serializer.data,
                }
            )
        
            logger.info(f"Variedad eliminado logicamente: (ID: {id})")
            return JsonResponse(dic_response, status=200)

        except Exception as e:
            logger.error(f"Error inesperado al eliminar la variedad: {str(e)}")
            dic_response["message"] = "Error inesperado"
            return JsonResponse(dic_response, status=500)

    return JsonResponse([], status=200)
