import axios from 'axios'

const API_URL = 'http://localhost:8000/api/subgruposactivos/'

class SubgruposActivosService {
    async getSubgruposActivos() {
        const response = await axios.get(API_URL)

        return response.data.data
    }
}
export default new SubgruposActivosService()
