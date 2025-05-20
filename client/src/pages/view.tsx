import React, { useEffect, useState, type FC } from 'react';
import { useNavigate } from "react-router-dom";
import api from '../api';


interface Password {
  user_name: string;
  plain_password: string;
  website: string
}

const View : FC = () =>{
   const [pswds, setPswds] = useState<Password[]>([])
   const navigate = useNavigate()
   const username = localStorage.getItem('username')

   const grabPswds = async () => {
      try{
         const response = await api.get(`${username}/view`);
         setPswds(response.data)
        
      } 
      catch(error){
         console.error("Error adding user", error)
      }
   }


   useEffect(() => {
    grabPswds();
   }, []);

     return (
      <div>
         <h1> {username}'s Passwords</h1>
         <h2>Add more passwords?</h2>
         <ul>
            {pswds.map((pswd, index) => (
               <li key={index}>
                  <div id ="password-data">      
                     <p>Username: {pswd.user_name}</p> <p>Website: {pswd.website}</p>  <p >Password: {pswd.plain_password}</p>  
                  </div>
               </li>
            ))}
        </ul>
      </div>
   );
       
   
}

export default View;