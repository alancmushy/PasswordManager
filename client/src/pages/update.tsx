import React, { useEffect, useState, type FC } from 'react';
import { useParams, useNavigate } from "react-router-dom";
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
   const [oldPassword,setOldPassword] = useState<Password>({
                           user_name: "",
                           plain_password: "",
                           website: ""
   });
   const navigate = useNavigate()
   const {username} = useParams()
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
            navigate("/error")
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
         navigate(`/${localStorage.getItem("username")}/view`)
      };

      const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
         event.preventDefault()
         const updated: Password = {user_name:newPswdUsername,plain_password:newPswdPlaintext,website:newPswdWebsite}
         console.log(updated)
         console.log(oldPassword)
         if(username !=null){
            console.log("New Password")
            updatePswd(oldPassword,updated,username)
            navigate(`/${localStorage.getItem("username")}/view`)
         }else{
            console.error("Error")
         }
   }

   return(
      <div>
         <div>
            <h1>Update Password</h1>
            <h2 id="typed-out-h2">View Passwords</h2> <button type="button" onClick = {navView}>VIEW</button> <br></br><br></br>
         </div>
            <form onSubmit = {handleSubmit}>
               <input type="text" value={newPswdUsername} onChange={(e) => setNewPswdUsername(e.target.value)} placeholder={oldPassword.user_name}></input><br></br><br></br>
               <input type="text" value={newPswdWebsite} onChange={(e) => setNewPswdWebsite(e.target.value)} placeholder={oldPassword.website}></input><br></br><br></br>
               <input id = "passwordForm"type="password" value={newPswdPlaintext} onChange={(e) => setNewPswdPlaintext(e.target.value)} placeholder={oldPassword.plain_password}></input><br></br>
               <img className = "see" src = "/eye.png" onClick={() => hideAndShow()}></img>
            
               <br></br><br></br>
               <button type ="submit"> UPDATE PASSWORD </button>
            </form>
      </div>
   );
}


export default Update;
