
import axios from 'axios'

const API_URL = 'http://localhost:8000/api/auditoriapordia/'

class AuditoriaService {
    async getAuditoriasPorDia() {
        const response = await axios.get(API_URL)

        return response.data
    }
}
export default new AuditoriaService()
