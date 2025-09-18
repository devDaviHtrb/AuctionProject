from flask import Blueprint, redirect, url_for, request

from myapp.models.LegalEntity import LegalEntity
from myapp.models.NaturalPerson import NaturalPerson
from myapp.models.User import User

from myapp.utils.utils import get_columns_names, is_cpf, is_cnpj, is_email, User_validation

singIn = Blueprint("singIn", __name__)

@singIn.route("/singIn", methods=["POST"])
def SingIn():
    user_type = request.form["userType"]#company or natural person

    #required data
    datakey = get_columns_names(User)
    datakey += get_columns_names(NaturalPerson) if user_type == "person" else  get_columns_names(LegalEntity)
    data = {}

    for requiredData in datakey:
        value = request.form[requiredData]
        if value == "":
            return redirect(url_for("singInPage.singInPage", msg = "Complete all the inputs"))
        data[requiredData] = value


    if not is_email(data["email"]):
        return redirect(url_for("singInPage.singInPage", msg = "Invalid email"))
    if user_type == "person":
        if is_cpf(data["cpf"]):
            if not User_validation(data["username"], data["email"], data["cpf"]):
                return redirect(url_for("singInPage.singInPage", msg = "There is already a user with that name, email or CPF"))
        else:
            return redirect(url_for("singInPage.singInPage", msg = "Invalid CPF"))
    else:
        if is_cnpj(data["cnpj"]):
            if not User_validation(data["username"], data["email"], data["cpf"], data["cnpj"]):
                return redirect(url_for("singInPage.singInPage", msg = "There is already a user with that name, email or CNPJ"))
        else:
            return redirect(url_for("singInPage.singInPage", msg = "Invalid CNPJ"))
        

    #validations
    return redirect(url_for("loginPage.LoginPage"))