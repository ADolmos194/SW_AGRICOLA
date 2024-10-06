import axios from 'axios'

const API_URL = 'http://localhost:8000/api/variedades/'

class VariedadService {

    async getVariedades() {
        const response = await axios.get(API_URL)
        
        return response.data.data
    }
    async createVariedad(data) {
        const response = await axios.post(`${API_URL}crear/`, data)

        return response.data
    }

    async updateVariedad(id, data) {
        const response = await axios.put(`${API_URL}actualizar/${id}/`, data)

        return response.data
    }

    async deleteVariedad(id) {
        const response = await axios.patch(`${API_URL}eliminar/${id}/`, { estado: 3 })

        return response.data
    }
}
export default new VariedadService()
