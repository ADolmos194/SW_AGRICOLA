import axios from 'axios'

const API_URL = 'http://localhost:8000/api/centros/'

class CentroService {

    async getCentros() {
        const response = await axios.get(API_URL)
        
        return response.data.data
    }
    async createCentro(data) {
        const response = await axios.post(`${API_URL}crear/`, data)

        return response.data
    }

    async updateCentro(id, data) {
        const response = await axios.put(`${API_URL}actualizar/${id}/`, data)

        return response.data
    }

    async deleteCentro(id) {
        const response = await axios.patch(`${API_URL}eliminar/${id}/`, { estado: 3 })

        return response.data
    }
}
export default new CentroService()
