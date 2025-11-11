from myapp.models.LegalPerson import legal_persons
from typing import Optional

def get_by_id(wanted_id: int) -> Optional[legal_persons]:
    return legal_persons.query.filter_by(user_id = wanted_id).first()