import axios from 'axios'

const API_URL = 'http://localhost:8000/api/distritos/'

class DistritoService {

    async getDistritos() {
        const response = await axios.get(API_URL)
        
        return response.data.data
    }
    async createDistrito(data) {
        const response = await axios.post(`${API_URL}crear/`, data)

        return response.data
    }

    async updateDistrito(id, data) {
        const response = await axios.put(`${API_URL}actualizar/${id}/`, data)

        return response.data
    }

    async deleteDistrito(id) {
        const response = await axios.patch(`${API_URL}eliminar/${id}/`, { estado: 3 })

        return response.data
    }
}
export default new DistritoService()
