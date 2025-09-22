from myapp.utils.Validations.ZipCodeValidation import zip_code_validation
def adress_validation(zip_code, district, state, city):
    adress = zip_code_validation(zip_code)
    if adress:
        if district != adress["bairro"] or state!=adress["uf"] or city!=adress["cidade"]:#The keys are in portuguese because the module 
            return False
        else:
            return True
    else:
        return False