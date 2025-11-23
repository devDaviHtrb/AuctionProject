from myapp.utils.Validations.ZipCodeValidation import zip_code_validation

#The keys are in portuguese because the module 
NEIGHBORHOOD =  "district"
UF =            "uf"
CITY =          "city"

def adress_validation(
    zip_code:str,
    district:str,
    state:str,
    city:str
) -> bool:
    adress = zip_code_validation(zip_code)
    print(adress)
    if adress:
        if district != adress[NEIGHBORHOOD] or state!=adress[UF] or city!=adress[CITY]:
            return [district==adress[NEIGHBORHOOD],state==adress[UF], city==adress[CITY]]
        else:
            return True
    else:
        return ["não há endereço"]