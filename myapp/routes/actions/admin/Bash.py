from flask import Blueprint, jsonify, request, Response
from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import text
from typing import Tuple


bash_bp = Blueprint("bash", __name__)

@bash_bp.route('/admin/bash/psql', methods=['POST'])
def execute_sql() -> Tuple[Response, int]:
    data = request.get_json()
    sql = data.get('sql', '').strip()
    if not sql:
        return jsonify({'error': 'No SQL sent'}),

    forbidden = ['DROP DATABASE', 'ATTACH', 'DETACH']
    if any(f.lower() in sql.lower() for f in forbidden):
        return jsonify({'error': 'Command prohibited'}), 403

    try:
        result = db.session.execute(text(sql))

     
        if sql.lower().startswith('select'):
            rows = [dict(r) for r in result.mappings().all()]
            return jsonify({'type': 'select', 'rows': rows, "cols":list(result.keys())}), 200

        else:
            db.session.commit()
            return jsonify({'type': 'modify', 'rowcount': result.rowcount}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400