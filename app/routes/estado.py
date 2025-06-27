from flask import Blueprint, jsonify, request
from app.db.conexion import get_db
import mysql.connector

bp_estado = Blueprint("estados", __name__)

def validar_estado(data):
    if not data or "nombre_estado" not in data or not data["nombre_estado"]:
        return False, "Falta el campo requerido: nombre_estado"
    return True, None

@bp_estado.route("/", methods=["GET"])
def listar_estados():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM estado")
        resultados = cursor.fetchall()
        cursor.close()
        return jsonify(resultados), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_estado.route("/<int:id>", methods=["GET"])
def listar_estado(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM estado WHERE id_estado = %s", (id,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return jsonify(resultado), 200
        return jsonify({"error": "Estado no encontrado"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_estado.route("/", methods=["POST"])
def guardar_estado():
    try:
        data = request.get_json(silent=True)
        valido, error = validar_estado(data)
        if not valido:
            return jsonify({"error": error}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO estado (nombre_estado) VALUES (%s)",
            (data["nombre_estado"],)
        )
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Estado creado correctamente"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_estado.route("/<int:id>", methods=["PUT"])
def actualizar_estado(id):
    try:
        data = request.get_json(silent=True)
        valido, error = validar_estado(data)
        if not valido:
            return jsonify({"error": error}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "UPDATE estado SET nombre_estado = %s WHERE id_estado = %s",
            (data["nombre_estado"], id)
        )
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Estado no encontrado"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Estado actualizado correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_estado.route("/<int:id>", methods=["DELETE"])
def eliminar_estado(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM estado WHERE id_estado = %s", (id,))
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Estado no encontrado"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Estado eliminado correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}),