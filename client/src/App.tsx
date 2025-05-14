import React from 'react';
import './App.css'
import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";
import RegUser from './pages/register'
import LogIn from './pages/logIn'

const Home: React.FC = () =>{
   const navigate = useNavigate()

   return (
      <div>
         <h1>Welcome To ArchLOCK</h1>
         <button onClick = {()=> navigate("/register")}> Register </button>
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
         <Route path = "/:username/view"></Route>
         <Route path = "/:username/append"></Route>
      </Routes>
   </BrowserRouter>

   
  );
};



export default App
