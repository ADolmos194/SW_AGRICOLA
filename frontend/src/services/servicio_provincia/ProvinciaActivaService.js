import axios from 'axios'

const API_URL = 'http://localhost:8000/api/provinciasactivas/'

class ProvinciaActivaService {
    async getProvinciaActiva() {
        const response = await axios.get(API_URL)

        return response.data.data
    }
}
export default new ProvinciaActivaService()
