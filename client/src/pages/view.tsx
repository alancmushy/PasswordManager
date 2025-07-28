import { useEffect, useState, type FC } from 'react';
import { useParams, useNavigate } from "react-router-dom";
import api from '../api';


interface Password {
  user_name: string;
  plain_password: string;
  website: string
}

const View : FC = () =>{
   const [pswds, setPswds] = useState<Password[]>([])
   const navigate = useNavigate()
   const {username} = useParams()

   const grabPswds = async () => {
      try{
         const response = await api.get(`${username}/view`);
         console.log("Fetched data:", response.data);
         setPswds(response.data)
      } 
      catch(error){
         console.error("Error grabbing passwords", error)
         navigate("/error")
      }
   }
   
   const navAdd = () => {  
   navigate(`/${username}/append`)
   };

   const navUpdate = (pswd:Password)=>{
      localStorage.setItem("oldPswd",JSON.stringify(pswd))
      navigate(`/${localStorage.getItem("username")}/update`)
   }

   const remove = async(selectedPswd:Password)=>{
      try{
         await api.delete(`/${username}/delete`,{
            data:selectedPswd,
            });
      } catch(error){
         console.error("Error deleteing password", error)
      }
      window.location.reload();
   }

   const logout = async() =>{
         await api.post(`/logout`)
         navigate((`/login`))
   }
   useEffect(() => {
    grabPswds();
    
   }, []);

     return (
      
      <div className ="view">
         <title>View - ARCH</title>
         <div className="sidebar">
            <a onClick = {navAdd}>Add</a>
            <a onClick = {logout}>LogOut</a>
         </div>
         <div>
            <h1>{localStorage.getItem('username')}'s Passwords</h1>
         </div>
         <div className="password-div">
            <ul className="passwords">
               {pswds.map((pswd, index) => (
                  <li key={index}>
                     <div className ="password-data">      
                        <p>Username: {pswd.user_name}</p> <p>Website: {pswd.website}</p>  <p>Password: {pswd.plain_password}</p> 
                        <div>
                           <img className = "removeImg" src = "/garbage.png" onClick={() => remove(pswd)}></img>
                           <img className = "updateImg" src = "/pencil.png" onClick={() => navUpdate(pswd)}></img>
                        </div>  
                     </div>
                  </li>
               ))}
            </ul>
         </div>
      </div>
   );
       
   
}

export default View;