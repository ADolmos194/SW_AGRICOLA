import axios from 'axios'

const axiosIns = axios.create({
// You can add your headers here
// ================================
    baseURL: "http://localhost:7400/travel",
    // baseURL: "http://104.236.0.154:8000/packing",


// timeout: 1000,
// headers: {'X-Custom-Header': 'foobar'}
})


export const axiosInsAuth = axios.create({
// You can add your headers here
// ================================
    baseURL: "http://localhost:7400",
    // baseURL: "http://104.236.0.154:8000",



// timeout: 1000,
// headers: {'X-Custom-Header': 'foobar'}
})

export default axiosIns
