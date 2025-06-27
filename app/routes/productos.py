from flask import Blueprint, jsonify, request
from app.db.conexion import get_db
import mysql.connector

bp_producto = Blueprint("productos", __name__)

error_permiso = 'Método no permitido'


@bp_producto.route("/", methods=["GET"])
def listar_productos():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM producto")
        resultados = cursor.fetchall()
        cursor.close()
        return jsonify(resultados), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_producto.route("/<int:id>", methods=["GET"])
def listar_producto(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM producto WHERE id_producto = %s", (id,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return jsonify(resultado), 200
        else:
            return jsonify({"error": "Producto no encontrado"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_producto.route("/", methods=["POST"])
def guardar_producto():
    try:
        data = request.get_json()
        required_fields = ["id_categoria", "nombre_producto", "precio_base"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO producto (id_categoria, nombre_producto, precio_base) VALUES (%s,%s,%s)",
            (data["id_categoria"], data["nombre_producto"], data["precio_base"])
        )
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Producto creado correctamente"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_producto.route("/<int:id>", methods=["PUT"])
def actualizar_producto(id):
    try:
        data = request.get_json()
        required_fields = ["id_categoria", "nombre_producto", "precio_base"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "UPDATE producto SET id_categoria = %s, nombre_producto = %s, precio_base = %s WHERE id_producto = %s",
            (data["id_categoria"], data["nombre_producto"], data["precio_base"], id)
        )
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Producto no encontrado"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Producto actualizado correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_producto.route("/<int:id>", methods=["DELETE"])
def eliminar_producto(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM producto WHERE id_producto = %s", (id,))
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Producto no encontrado"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Producto eliminado correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500