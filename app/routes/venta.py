from flask import Blueprint, jsonify, request
from app.db.conexion import get_db
import mysql.connector

bp_venta = Blueprint("ventas", __name__)

def validar_venta(data):
    campos = ["fecha", "id_usuario", "id_tipo_venta", "total"]
    if not data:
        return False, "No se recibió información"
    for campo in campos:
        if campo not in data or data[campo] in (None, ""):
            return False, f"Falta el campo requerido: {campo}"
    return True, None

def validar_detalle_venta(data):
    campos = ["id_producto", "cantidad", "precio_unitario"]
    if not data:
        return False, "No se recibió información"
    for campo in campos:
        if campo not in data or data[campo] in (None, ""):
            return False, f"Falta el campo requerido: {campo}"
    return True, None

@bp_venta.route("/", methods=["GET"])
def listar_ventas():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM venta")
        resultados = cursor.fetchall()
        cursor.close()
        return jsonify(resultados), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_venta.route("/<int:id>", methods=["GET"])
def listar_venta(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM venta WHERE id_venta = %s", (id,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return jsonify(resultado), 200
        return jsonify({"error": "Venta no encontrada"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_venta.route("/", methods=["POST"])
def guardar_venta():
    try:
        data = request.get_json(silent=True)
        valido, error = validar_venta(data)
        if not valido:
            return jsonify({"error": error}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO venta (fecha, id_usuario, id_tipo_venta, total) VALUES (%s, %s, %s, %s)",
            (data["fecha"], data["id_usuario"], data["id_tipo_venta"], data["total"])
        )
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Venta creada correctamente"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_venta.route("/<int:id>", methods=["PUT"])
def actualizar_venta(id):
    try:
        data = request.get_json(silent=True)
        valido, error = validar_venta(data)
        if not valido:
            return jsonify({"error": error}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "UPDATE venta SET fecha = %s, id_usuario = %s, id_tipo_venta = %s, total = %s WHERE id_venta = %s",
            (data["fecha"], data["id_usuario"], data["id_tipo_venta"], data["total"], id)
        )
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Venta no encontrada"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Venta actualizada correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_venta.route("/<int:id>", methods=["DELETE"])
def eliminar_venta(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM venta WHERE id_venta = %s", (id,))
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Venta no encontrada"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Venta eliminada correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- DETALLE DE VENTA ANIDADO ---

@bp_venta.route("/<int:venta_id>/detalle", methods=["GET"])
def listar_detalle_venta(venta_id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM detalle_venta WHERE id_venta = %s", (venta_id,))
        resultados = cursor.fetchall()
        cursor.close()
        return jsonify(resultados), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_venta.route("/<int:venta_id>/detalle", methods=["POST"])
def guardar_detalle_venta(venta_id):
    try:
        data = request.get_json(silent=True)
        valido, error = validar_detalle_venta(data)
        if not valido:
            return jsonify({"error": error}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO detalle_venta (id_venta, id_producto, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
            (venta_id, data["id_producto"], data["cantidad"], data["precio_unitario"])
        )
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Detalle de venta creado correctamente"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_venta.route("/<int:venta_id>/detalle/<int:id_detalle>", methods=["PUT"])
def actualizar_detalle_venta(venta_id, id_detalle):
    try:
        data = request.get_json(silent=True)
        valido, error = validar_detalle_venta(data)
        if not valido:
            return jsonify({"error": error}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "UPDATE detalle_venta SET id_producto = %s, cantidad = %s, precio_unitario = %s WHERE id_venta = %s AND id_detalle_venta = %s",
            (data["id_producto"], data["cantidad"], data["precio_unitario"], venta_id, id_detalle)
        )
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Detalle de venta no encontrado"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Detalle de venta actualizado correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_venta.route("/<int:venta_id>/detalle/<int:id_detalle>", methods=["DELETE"])
def eliminar_detalle_venta(venta_id, id_detalle):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM detalle_venta WHERE id_venta = %s AND id_detalle_venta = %s", (venta_id, id_detalle))
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Detalle de venta no encontrado"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Detalle de venta eliminado correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500