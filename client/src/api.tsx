import axios from 'axios'

const api = axios.create({
    baseURL: 'https://archlock.onrender.com', 
    withCredentials: true  
    
    
})



export default api;