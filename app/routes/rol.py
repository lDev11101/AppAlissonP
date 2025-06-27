from flask import Blueprint, jsonify, request
from app.db.conexion import get_db
import mysql.connector

bp_roles = Blueprint("roles", __name__)

def validar_rol(data):
    if not data or "nombre_rol" not in data or not data["nombre_rol"]:
        return False, "Falta el campo requerido: nombre_rol"
    return True, None

@bp_roles.route("/", methods=["GET"])
def listar_roles():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM rol")
        resultados = cursor.fetchall()
        cursor.close()
        return jsonify(resultados), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_roles.route("/<int:id>", methods=["GET"])
def listar_rol(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM rol WHERE id_rol = %s", (id,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return jsonify(resultado), 200
        return jsonify({"error": "Rol no encontrado"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_roles.route("/", methods=["POST"])
def guardar_rol():
    try:
        data = request.get_json(silent=True)
        valido, error = validar_rol(data)
        if not valido:
            return jsonify({"error": error}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO rol (nombre_rol) VALUES (%s)",
            (data["nombre_rol"],)
        )
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Rol creado correctamente"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_roles.route("/<int:id>", methods=["PUT"])
def actualizar_rol(id):
    try:
        data = request.get_json(silent=True)
        valido, error = validar_rol(data)
        if not valido:
            return jsonify({"error": error}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "UPDATE rol SET nombre_rol = %s WHERE id_rol = %s",
            (data["nombre_rol"], id)
        )
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Rol no encontrado"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Rol actualizado correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_roles.route("/<int:id>", methods=["DELETE"])
def eliminar_rol(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM rol WHERE id_rol = %s", (id,))
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Rol no encontrado"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Rol eliminado correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return