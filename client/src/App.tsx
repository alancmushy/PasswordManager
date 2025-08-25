import React from 'react';
import './App.css'
import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";
import RegUser from './pages/register'
import LogIn from './pages/logIn'
import Append from './pages/addPswd'
import View from './pages/view'
import Update from './pages/update'
import ErrorPage from './pages/errorpage';


const Home: React.FC = () =>{
   const navigate = useNavigate()

   return (
      <div>
         <img src="\Lock_icon.png" width="60" height="60"></img>
         <h1 id = "typed-out-h1">Welcome To Archlock</h1><br></br>
         <h2 id = "typed-out-h2">Your go-to, no-nonsense, secure password manager</h2><br></br><br></br>
         <button onClick = {()=> navigate("/register")}> Register </button><br></br><br></br>
         <button onClick = {()=> navigate("/login")}> LogIn </button>
      </div>
   ); 
};



const App: React.FC = () => {
  return (
      
   <BrowserRouter>
      <Routes>
         <Route path="/" element={<Home />} /> 
         <Route path = "/register" element = {<RegUser />}  />
         <Route path = "/login" element = {<LogIn />}  />
         <Route path = "/:username/view"  element = {<View />}  />
         <Route path = "/:username/append" element = {<Append/>}></Route>
         <Route path = "/:username/update" element = {<Update/>}></Route>
         <Route path = "/error" element ={<ErrorPage/>}></Route>
      </Routes>
   </BrowserRouter>

   
  );
};



export default App
