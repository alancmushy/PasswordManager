import axios from 'axios'

const api = axios.create({
    baseURL:'https://archlock.onrender.com'
})

console.log("NEXT_PUBLIC_BASE_URL:", process.env.NEXT_PUBLIC_BASE_URL);

export default api;