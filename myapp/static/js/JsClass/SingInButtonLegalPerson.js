import { singInLegalPerson } from "../interactivity/SingInLegalPerson"
class LoginButton{
    constructor(id){
        this.button = document.getElementById(id)
        
        this.button.addEventListener("click", (event)=>{
            singInLegalPerson()
        })
    }
}

const button = new LoginButton("loginButton")