import React, { useEffect, useState, type FC } from 'react';
import { useNavigate } from "react-router-dom";
import api from '../api';


interface Password {
  user_name: string;
  plain_password: string;
  website: string
}


const Update : FC = () =>{
   const [newPswdUsername, setNewPswdUsername] = useState<string>('');
   const [newPswdPlaintext, setNewPswdPlaintext] = useState<string>('')
   const [newPswdWebsite, setNewPswdWebsite] = useState<string>('')
   const [newPswd, setNewPswd] = useState<Password>({
                           user_name: "",
                           plain_password: "",
                           website: ""
   });
   const [oldPassword,setOldPassword] = useState<Password>({
                           user_name: "",
                           plain_password: "",
                           website: ""
   });
   const navigate = useNavigate()
   const username = localStorage.getItem('username')
   const oldPswd = localStorage.getItem('oldPswd')
   

   const parseOldPswd = (old:string) => {
      if(oldPswd){
         const data = JSON.parse(old)
         setOldPassword(data);
      }
   }  

   useEffect(() => {
      if(oldPswd !=null){
         parseOldPswd(oldPswd);
      }
   }, []);
   const updatePswd = async (oldPassword:Password,newPswd:Password,username:string) => {
      
         try{
            await api.post(`/${username}/update`, {oldPswd:oldPassword,newPswd:newPswd,username:username})
         } catch(error){
            console.error("Error adding password", error)
         }
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


      const navView = () => {
         navigate(`/${username}/view`)
      };

      const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
         event.preventDefault()
         const updated: Password = {user_name:newPswdUsername,plain_password:newPswdPlaintext,website:newPswdWebsite}
         console.log(updated)
         console.log(oldPassword)
         if(username !=null){
            console.log("New Password")
            updatePswd(oldPassword,updated,username)
            navigate(`/${username}/view`)
         }else{
            console.error("Error")
         }
   }

   return(
      <div>
         <div>
            <h1>Add Password to Database</h1>
            <h2>View Passwords</h2> <button type="button" onClick = {navView}>Log In</button> <br></br><br></br>
         </div>
            <form onSubmit = {handleSubmit}>
               <p> Previous Username: {oldPassword.user_name}</p>
               <p> Previous Website: {oldPassword.website}</p>
               <p> Previous Password: {oldPassword.plain_password}</p>
               <input type="text" value={newPswdUsername} onChange={(e) => setNewPswdUsername(e.target.value)} placeholder='Enter New Account Username'></input><br></br><br></br>
               <input type="text" value={newPswdWebsite} onChange={(e) => setNewPswdWebsite(e.target.value)} placeholder='Enter New Account Website'></input><br></br><br></br>
               <input id = "passwordForm"type="password" value={newPswdPlaintext} onChange={(e) => setNewPswdPlaintext(e.target.value)} placeholder='Enter New Account Password'></input><br></br>
               <img className = "see" src = "/eye.png" onClick={() => hideAndShow()}></img>
            
               <br></br><br></br>
               <button type ="submit"> UPDATE PASSWORD </button>
            </form>
      </div>
   );
}


export default Update;