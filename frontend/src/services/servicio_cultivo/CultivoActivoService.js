import axios from 'axios'

const API_URL = 'http://localhost:8000/api/cultivosactivos/'

class CultivoActivoService {

    async getCultivosActivos() {
        const response = await axios.get(API_URL)
        
        return response.data.data
    }
}
export default new CultivoActivoService()
