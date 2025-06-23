from flask import Blueprint, jsonify
from app.db.conexion import get_db

bp_producto = Blueprint("productos", __name__)


@bp_producto.route("/listar-todos", methods=["GET"])
def listar_productos():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM rol")
    resultados = cursor.fetchall()
    cursor.close()
    return jsonify(resultados), 200
