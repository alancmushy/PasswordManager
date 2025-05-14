import React, { useState, type FC } from 'react';
import { useNavigate } from "react-router-dom";
import api from '../api';



const LogIn : FC = () =>{
   const [username, setUsername] = useState<string>('')
   const [nameInput, setNameInput] = useState<string>('')
   const [pswdInput, setPswdInput] = useState<string>('')
   const navigate = useNavigate()

   const loginUser = async(nameInput:string, pswdInput:string) => {
   try{
      const response = await api.post('/login',{username:nameInput,password:pswdInput});
      setUsername(response.data.username)
      navigate(`/${nameInput}/view`)
   } catch(error){
      document.getElementById("pswdCheckText")!.innerHTML = "Password or Username invalid! Try again.";
      console.error("Error logging in user", error)
   }
};

const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
  event.preventDefault()
  loginUser(nameInput, pswdInput)
}
  return (
   <form onSubmit = {handleSubmit}>
      <div>
            <h1>Login</h1>
            <p id ="pswdCheckText" color='red'></p>
            <input type="text" value={nameInput} onChange={(e) => setNameInput(e.target.value)} placeholder='Username'></input><br></br><br></br>
            <input type="password" value={pswdInput} onChange={(e) => setPswdInput(e.target.value)} placeholder='Password'></input><br></br><br></br>
            <button type ="submit"> LOGIN </button>
      </div>
   </form>
  );
  
};

export default LogIn;