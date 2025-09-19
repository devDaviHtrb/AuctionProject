import { login } from "../interactivity/Login.js"
class LoginButton{
    constructor(id){
        this.button = document.getElementById(id)
        
        this.button.addEventListener("click", (event)=>{
            login()
        })
    }
}

const button = new LoginButton("loginButton")