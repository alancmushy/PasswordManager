import React, { useState, type FC } from 'react';
import { useNavigate } from "react-router-dom";
//import LogIn from './logIn'
import api from '../api';



const RegUser : FC = () =>{
   const [nameInput, setNameInput] = useState<string>('')
   const [pswdInput, setPswdInput] = useState<string>('')
   const [doubleCheckPswd, setDoubleCheckPswd] = useState<string>('')
   const navigate = useNavigate()

const registerUser = async(nameInput:string, pswdInput:string) => {
   try{
      await api.post('/register',   {username:nameInput,password:pswdInput});
      localStorage.setItem('username', nameInput)
      navigate(`/${nameInput}/append`)
   } catch(error){
      console.error("Error adding user", error)
   }
};

const navLogin = () => {
   navigate('/login')
};

const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
  event.preventDefault()
  if(pswdInput === doubleCheckPswd && pswdInput.length !== null && doubleCheckPswd.length != null){
      registerUser(nameInput, pswdInput);
  }else{
      document.getElementById("pswdCheckText")!.innerHTML = "Passwords do NOT match! Try again";
  }

};

   const hideAndShow = () =>{
   
   var passwordBox1 = document.getElementById("pswdForm1") as HTMLInputElement;
   var passwordBox2 = document.getElementById("pswdForm2") as HTMLInputElement;
    if (!passwordBox1 && !passwordBox2) {
      console.error("Element with ID 'passwordForm' not found.");
      return;
   }
   
   if(passwordBox1.type === "password"){
      passwordBox1.type = "text"
      passwordBox2.type = "text"
   }else if (passwordBox1.type === "text"){
      passwordBox1.type = "password"
      passwordBox2.type = "password"
   }
}


  return (
   
      <div>
         <head>
            <title>Register - ARCH</title>
         </head>
         <div>
            <h1>Register</h1>
            <h2 id="typed-out-h2">Already have an account?</h2><br></br> <button type="button" onClick = {navLogin}>Log In</button>
         </div>
            <form onSubmit = {handleSubmit}>
               <p  id ="pswdCheckText" style ={{color:'red'}}></p>
               <input type="text" value={nameInput} onChange={(e) => setNameInput(e.target.value)} placeholder='Username'></input><br></br><br></br>
               <input id = "pswdForm1" type="password" value={pswdInput} onChange={(e) => setPswdInput(e.target.value)} placeholder='Password'></input><br></br><br></br>
               <input id = "pswdForm2" type="password" value={doubleCheckPswd} onChange={(e) => setDoubleCheckPswd(e.target.value)} placeholder='Re-Enter Password'></input><br></br>
               <img className = "see" src = "/eye.png" onClick={() => hideAndShow()}></img>
               <br></br><br></br>
               <button type ="submit"> Register </button>
            </form>
      </div>
   
  );
  
};

export default RegUser;