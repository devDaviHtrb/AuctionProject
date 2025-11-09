from myapp.models.PhysicalPerson import physical_persons
from typing import Optional

def get_by_id(wanted_id:int) -> Optional[physical_persons]:
    return physical_persons.query.filter_by(user_id = wanted_id).first()