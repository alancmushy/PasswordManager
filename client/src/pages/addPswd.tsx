import React, { useState, type FC } from 'react';
import { useNavigate } from "react-router-dom";
import api from '../api';

const Append : FC = () =>{
   const [pswdUsername, setpswdUsername] = useState<string>('');
   const [pswdPlaintext, setPswdPlaintext] = useState<string>('')
   const [pswdWebsite, setPswdWebsite] = useState<string>('')
   const navigate = useNavigate()
   const username = localStorage.getItem('username')

const addPswd = async(pswdUsername:string, pswdPlaintext:string, pswdWebsite:string) => {
      try{
         await api.post(`/${username}/append`,{user_name:pswdUsername,plain_password:pswdPlaintext,website:pswdWebsite});
         console.log(`${username} added ${website} password to database`)
      } catch(error){
         console.error("Error adding password", error)
   }
   }

   const navView = () => {
      navigate(`/${username}/view`)
   };

   const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
      event.preventDefault()
      addPswd(pswdUsername,pswdPlaintext,pswdWebsite)
      navigate(`/${username}/view`)
}

const hideAndShow = () =>{
   
   var passwordBox = document.getElementById("passwordForm") as HTMLInputElement;
   
    if (!passwordBox) {
      console.error("Element with ID 'passwordForm' not found.");
      return;
   }
   
   if(passwordBox.type === "password"){
      passwordBox.type = "text"
   }else if (passwordBox.type === "text"){
      passwordBox.type = "password"
   }
}
  return (
   
      <div>
         <div>
            <h1>Add Password to Database</h1>
            <h2>View Passwords</h2> <button type="button" onClick = {navView}>Log In</button> <br></br><br></br>
         </div>
            <form onSubmit = {handleSubmit}>
               <input type="text" value={pswdUsername} onChange={(e) => setpswdUsername(e.target.value)} placeholder='Account Username'></input><br></br><br></br>
               <input type="text" value={pswdWebsite} onChange={(e) => setPswdWebsite(e.target.value)} placeholder='Account Website'></input><br></br><br></br>
               <input id = "passwordForm" type="password" value={pswdPlaintext} onChange={(e) => setPswdPlaintext(e.target.value)} placeholder='Account Password'></input> <br></br>
               <img className = "see" src = "/eye.png" onClick={() => hideAndShow()}></img>
               <br></br><br></br>
               <button type ="submit"> ADD PASSWORD </button>
            </form>
      </div>
   
  );
  
};

export default Append;