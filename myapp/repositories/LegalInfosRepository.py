from myapp.models.LegalInfos import legal_infos
from myapp.models.CaseTypes import case_types
from myapp.setup.InitSqlAlchemy import db
from typing import Dict, Any

def save_item(data:Dict[str, Any]) -> legal_infos:
    