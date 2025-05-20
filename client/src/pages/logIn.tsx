import React, { useState, type FC } from 'react';
import { useNavigate } from "react-router-dom";
import api from '../api';



const LogIn : FC = () =>{
   const [nameInput, setNameInput] = useState<string>('')
   const [pswdInput, setPswdInput] = useState<string>('')
   const navigate = useNavigate()

   const loginUser = async(nameInput:string, pswdInput:string) => {
   try{
      await api.post('/login',{username:nameInput,password:pswdInput});
      localStorage.setItem('username', nameInput)
      navigate(`/${nameInput}/view`)
   } catch(error){
      document.getElementById("pswdCheckText")!.innerHTML = "Password or Username invalid! Try again.";
      console.error("Error logging in user", error)
   }
};
const navReg = () => {  
   navigate('/register')
};

const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
  event.preventDefault()
  loginUser(nameInput, pswdInput)
}


  return (
      <div>
         <div>
            <h1>Login</h1>
            <h2>Don't have an account?</h2> <button onClick = {navReg}>Register</button>
         </div>
            <form onSubmit = {handleSubmit}>
               <p id ="pswdCheckText" color='red'></p>
               <input type="text" value={nameInput} onChange={(e) => setNameInput(e.target.value)} placeholder='Username'></input><br></br><br></br>
               <input type="password" value={pswdInput} onChange={(e) => setPswdInput(e.target.value)} placeholder='Password'></input><br></br><br></br>
               <button type ="submit"> LOGIN </button>
            </form>
      </div>
  );
  
};

export default LogIn;