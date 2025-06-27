from flask import Blueprint, jsonify, request
from app.db.conexion import get_db
import mysql.connector

bp_inventario = Blueprint("inventario", __name__)

error_permiso = 'Método no permitido'

@bp_inventario.route("/", methods=["GET"])
def listar_inventario():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM inventario")
        resultados = cursor.fetchall()
        cursor.close()
        return jsonify(resultados), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_inventario.route("/<int:id>", methods=["GET"])
def listar_inventario_id(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM inventario WHERE id_inventario = %s", (id,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return jsonify(resultado), 200
        else:
            return jsonify({"error": "Inventario no encontrado"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_inventario.route("/", methods=["POST"])
def guardar_inventario():
    try:
        data = request.get_json()
        required_fields = ["id_producto", "fecha_vencimiento", "codigo_lote", "cantidad_disponible", "alerta_vencimiento"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO inventario (id_producto, fecha_vencimiento, codigo_lote, cantidad_disponible, alerta_vencimiento) VALUES (%s, %s, %s, %s, %s)",
            (
                data.get("id_producto"),
                data.get("fecha_vencimiento"),
                data.get("codigo_lote"),
                data.get("cantidad_disponible"),
                data.get("alerta_vencimiento")
            )
        )
        conn.commit()
        cursor.close()
        return jsonify({"message": "Inventario guardado exitosamente"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_inventario.route("/<int:id>", methods=["PUT"])
def actualizar_inventario(id):
    try:
        data = request.get_json()
        required_fields = ["id_producto", "fecha_vencimiento", "codigo_lote", "cantidad_disponible", "alerta_vencimiento"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE inventario SET id_producto = %s, fecha_vencimiento = %s, codigo_lote = %s, cantidad_disponible = %s, alerta_vencimiento = %s WHERE id_inventario = %s",
            (
                data["id_producto"],
                data["fecha_vencimiento"],
                data["codigo_lote"],
                data["cantidad_disponible"],
                data["alerta_vencimiento"],
                id
            )
        )
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Inventario no encontrado"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"message": "Inventario actualizado exitosamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_inventario.route("/<int:id>", methods=["DELETE"])
def eliminar_inventario(id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventario WHERE id_inventario = %s", (id,))
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Inventario no encontrado"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"message": "Inventario eliminado exitosamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500