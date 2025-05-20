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


  return (
   
      <div>
         <div>
            <h1>Register</h1>
            <h2>Already have an account?</h2> <button type="button" onClick = {navLogin}>Log In</button>
         </div>
            <form onSubmit = {handleSubmit}>
               <p  id ="pswdCheckText" style ={{color:'red'}}></p>
               <input type="text" value={nameInput} onChange={(e) => setNameInput(e.target.value)} placeholder='Username'></input><br></br><br></br>
               <input type="password" value={pswdInput} onChange={(e) => setPswdInput(e.target.value)} placeholder='Password'></input><br></br><br></br>
               <input type="password" value={doubleCheckPswd} onChange={(e) => setDoubleCheckPswd(e.target.value)} placeholder='Re-Enter Password'></input><br></br><br></br>
               <button type ="submit"> REGISTER </button>
            </form>
      </div>
   
  );
  
};

export default RegUser;