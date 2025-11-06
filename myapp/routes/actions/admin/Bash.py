from flask import Blueprint, jsonify, request, render_template
from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import text
import os


bash_bp = Blueprint("bash", __name__)

@bash_bp.route('/admin/bash/psql', methods=['POST'])
def execute_sql():
    data = request.get_json()
    sql = data.get('sql', '').strip()
    if not sql:
        return jsonify({'error': 'Nenhum SQL enviado'}), 400

    forbidden = ['DROP DATABASE', 'ATTACH', 'DETACH']
    if any(f.lower() in sql.lower() for f in forbidden):
        return jsonify({'error': 'Comando proibido'}), 403

    try:
        result = db.session.execute(text(sql))

        # 🔹 SELECT → converter RowMapping para dict
        if sql.lower().startswith('select'):
            rows = [dict(r) for r in result.mappings().all()]
            return jsonify({'type': 'select', 'rows': rows, "cols":list(result.keys())}), 200

        # 🔹 Outros comandos → commit + contagem de linhas
        else:
            db.session.commit()
            return jsonify({'type': 'modify', 'rowcount': result.rowcount}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400