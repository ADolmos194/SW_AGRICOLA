import axios from 'axios'

const API_URL = 'http://localhost:8000/api/empresasactivas/'

class EmpresaActivaService {
    async getEmpresasActivas() {
        const response = await axios.get(API_URL)

        return response.data.data
    }
}
export default new EmpresaActivaService()
