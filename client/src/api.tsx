import axios from 'axios'

const api = axios.create({
    baseURL: 'https://archlock.onrender.com',
    //baseURL:'http://localhost:8000',
    withCredentials: true  
    
    
})



export default api;