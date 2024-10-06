import axios from 'axios'

const API_URL = 'http://localhost:8000/api/paisesactivos/'

class PaisActivoService {
    async getPaisesActivos() {
        const response = await axios.get(API_URL)

        return response.data.data
    }
}
export default new PaisActivoService()
