from myapp.utils.Validations.ZipCodeValidation import zip_code_validation

#The keys are in portuguese because the module 
NEIGHBORHOOD =  "bairro"
UF =            "uf"
CITY =          "cidade"

def adress_validation(
    zip_code:str,
    district:str,
    state:str,
    city:str
) -> bool:
    adress = zip_code_validation(zip_code)
    if adress:
        if district != adress[NEIGHBORHOOD] or state!=adress[UF] or city!=adress[CITY]:
            return False
        else:
            return True
    else:
        return False