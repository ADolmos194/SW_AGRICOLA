
import axios from 'axios'

const API_URL = 'http://localhost:8000/api/auditoria/'

class AuditoriaService {
    async getAuditorias() {
        const response = await axios.get(API_URL)

        return response.data.data
    }
}
export default new AuditoriaService()
