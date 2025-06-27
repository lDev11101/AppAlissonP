from flask import Blueprint, jsonify, request
from app.db.conexion import get_db
import mysql.connector

bp_usuario = Blueprint("usuarios", __name__)

def validar_usuario(data):
    campos = ["nombre", "id_rol", "correo", "contraseña"]
    if not data:
        return False, "No se recibió información"
    for campo in campos:
        if campo not in data or data[campo] in (None, ""):
            return False, f"Falta el campo requerido: {campo}"
    return True, None

@bp_usuario.route("/", methods=["GET"])
def listar_usuarios():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuario")
        resultados = cursor.fetchall()
        cursor.close()
        return jsonify(resultados), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_usuario.route("/<int:id>", methods=["GET"])
def listar_usuario(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return jsonify(resultado), 200
        return jsonify({"error": "Usuario no encontrado"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_usuario.route("/", methods=["POST"])
def guardar_usuario():
    try:
        data = request.get_json(silent=True)
        valido, error = validar_usuario(data)
        if not valido:
            return jsonify({"error": error}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO usuario (nombre, id_rol, correo, contraseña) VALUES (%s, %s, %s, %s)",
            (data["nombre"], data["id_rol"], data["correo"], data["contraseña"])
        )
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Usuario creado correctamente"}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"error": "El correo ya está registrado"}), 409
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_usuario.route("/<int:id>", methods=["PUT"])
def actualizar_usuario(id):
    try:
        data = request.get_json(silent=True)
        valido, error = validar_usuario(data)
        if not valido:
            return jsonify({"error": error}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "UPDATE usuario SET nombre = %s, id_rol = %s, correo = %s, contraseña = %s WHERE id_usuario = %s",
            (data["nombre"], data["id_rol"], data["correo"], data["contraseña"], id)
        )
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Usuario no encontrado"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Usuario actualizado correctamente"}), 200
    except mysql.connector.IntegrityError:
        return jsonify({"error": "El correo ya está registrado"}), 409
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_usuario.route("/<int:id>", methods=["DELETE"])
def eliminar_usuario(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id,))
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Usuario no encontrado"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Usuario eliminado correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500