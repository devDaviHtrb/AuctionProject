
from myapp.models.PhysicalPerson import physical_persons
from myapp.setup.InitSqlAlchemy import db
from myapp.models.Users import users
from myapp.models.LegalPerson import legal_persons
from werkzeug.security import generate_password_hash
from datetime import datetime
from typing import Dict, Any

def create_user(data: Dict[str, Any]) -> Dict[str, Any]:

    user_type = data.get("userType", "physical_person")
    

    user = users(
        username = data.get("username"),
        password = generate_password_hash(data.get("password")),
        email = data.get("email"),
        cpf = data.get("cpf"),
        name = data.get("name"),
        photo = data.get("photo_url", None),
        cellphone1 = data.get("cellphone1", None),
        cellphone2 = data.get("cellphone2", None),
        landline = data.get("landline", None),
        wallet = 100, #rs
        active_auction_number = float(0),
        password_token_expiration_datetime = None,
        api_token = None,
        password_token = None,
        admin_user = False,
    )
    db.session.add(user)
    db.session.flush() #generate the user id
    
    """create_adress(
        street_name = data.get("street_name"),
        street_number = data.get("street_number"),
        apt = data.get("apt", None),
        zip_code = data.get("zip_code"),
        district = data.get("district"),
        city = data.get("city"),
        state = data.get("state")),
        principal_adress = True,
        user_id = user.user_id"""

    if user_type == "physical_person":
        physical_person = physical_persons(
            user_id = user.user_id, 
            rg = data.get("rg"), 
            birth_date = data.get("birth_date"), 
            gender = data.get("gender")
        )
        db.session.add(physical_person)
    else:  # legal person
        legal_person = legal_persons(
            user_id = user.user_id,
            scrap_purchase_authorization = data.get("scrap_purchase_authorization", False),
            trade_name = data.get("trade_name"), 
            legal_business_name = data.get("legal_business_name"),
            cnpj = data.get("cnpj"),
            state_tax_registration = data.get("state_tax_registration")
        )
        db.session.add(legal_person)
    
    db.session.commit()
    return user