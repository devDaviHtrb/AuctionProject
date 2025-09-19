import { singInPerson } from "../interactivity/SingInPerson"
class LoginButton{
    constructor(id){
        this.button = document.getElementById(id)
        
        this.button.addEventListener("click", (event)=>{
            singInPerson()
        })
    }
}

const button = new LoginButton("loginButton")