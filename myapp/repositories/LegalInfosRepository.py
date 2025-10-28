from myapp.models.LegalInfos import legal_infos
from myapp.models.CaseTypes import case_types
from myapp.setup.InitSqlAlchemy import db
from typing import Dict, Any
from sqlalchemy import select

def save_item(data:Dict[str, Any]) -> legal_infos:
    data["case_type"] = db.session.execute(
            select(case_types.case_type_id)
            .where(case_types.case_type_name == data["case_type"])
        ).scalar()
    new_legal_info = legal_infos(**data)
    db.session.add(new_legal_info)
    db.session.flush()
    db.session.commit()