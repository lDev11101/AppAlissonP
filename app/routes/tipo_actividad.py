from flask import Blueprint, jsonify, request
from app.db.conexion import get_db
import mysql.connector

bp_tipo_actividad = Blueprint("tipo_actividad", __name__)

def validar_tipo_actividad(data):
    if not data or "nombre" not in data or not data["nombre"]:
        return False, "Falta el campo requerido: nombre"
    return True, None

@bp_tipo_actividad.route("/", methods=["GET"])
def listar_tipos_actividad():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tipo_actividad")
        resultados = cursor.fetchall()
        cursor.close()
        return jsonify(resultados), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_tipo_actividad.route("/<int:id>", methods=["GET"])
def listar_tipo_actividad(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tipo_actividad WHERE id_tipoactividad = %s", (id,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return jsonify(resultado), 200
        return jsonify({"error": "Tipo de actividad no encontrado"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_tipo_actividad.route("/", methods=["POST"])
def guardar_tipo_actividad():
    try:
        data = request.get_json(silent=True)
        valido, error = validar_tipo_actividad(data)
        if not valido:
            return jsonify({"error": error}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO tipo_actividad (nombre) VALUES (%s)",
            (data["nombre"],)
        )
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Tipo de actividad creado correctamente"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_tipo_actividad.route("/<int:id>", methods=["PUT"])
def actualizar_tipo_actividad(id):
    try:
        data = request.get_json(silent=True)
        valido, error = validar_tipo_actividad(data)
        if not valido:
            return jsonify({"error": error}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "UPDATE tipo_actividad SET nombre = %s WHERE id_tipoactividad = %s",
            (data["nombre"], id)
        )
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Tipo de actividad no encontrado"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Tipo de actividad actualizado correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_tipo_actividad.route("/<int:id>", methods=["DELETE"])
def eliminar_tipo_actividad(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM tipo_actividad WHERE id_tipoactividad = %s", (id,))
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Tipo de actividad no encontrado"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Tipo de actividad eliminado correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500