from flask import Blueprint, jsonify, request
from app.db.conexion import get_db
import mysql.connector

bp_movimiento = Blueprint("movimientos_almacen", __name__)

def validar_movimiento(data):
    campos = ["fecha", "id_tipo_movimiento", "id_producto", "cantidad"]
    if not data:
        return False, "No se recibió información"
    for campo in campos:
        if campo not in data or data[campo] in (None, ""):
            return False, f"Falta el campo requerido: {campo}"
    return True, None

@bp_movimiento.route("/", methods=["GET"])
def listar_movimientos():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM movimiento_almacen")
        resultados = cursor.fetchall()
        cursor.close()
        return jsonify(resultados), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_movimiento.route("/<int:id>", methods=["GET"])
def listar_movimiento(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM movimiento_almacen WHERE id_movimiento = %s", (id,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return jsonify(resultado), 200
        else:
            return jsonify({"error": "Movimiento no encontrado"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_movimiento.route("/", methods=["POST"])
def guardar_movimiento():
    try:
        data = request.get_json()
        valido, error = validar_movimiento(data)
        if not valido:
            return jsonify({"error": error}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO movimiento_almacen (fecha, id_tipo_movimiento, id_producto, cantidad, detalle) VALUES (%s, %s, %s, %s, %s)",
            (
                data["fecha"],
                data["id_tipo_movimiento"],
                data["id_producto"],
                data["cantidad"],
                data.get("detalle")
            )
        )
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Movimiento creado correctamente"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_movimiento.route("/<int:id>", methods=["PUT"])
def actualizar_movimiento(id):
    try:
        data = request.get_json()
        valido, error = validar_movimiento(data)
        if not valido:
            return jsonify({"error": error}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "UPDATE movimiento_almacen SET fecha = %s, id_tipo_movimiento = %s, id_producto = %s, cantidad = %s, detalle = %s WHERE id_movimiento = %s",
            (
                data["fecha"],
                data["id_tipo_movimiento"],
                data["id_producto"],
                data["cantidad"],
                data.get("detalle"),
                id
            )
        )
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Movimiento no encontrado"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Movimiento actualizado correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_movimiento.route("/<int:id>", methods=["DELETE"])
def eliminar_movimiento(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM movimiento_almacen WHERE id_movimiento = %s", (id,))
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Movimiento no encontrado"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Movimiento eliminado correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500