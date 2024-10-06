import axios from 'axios'

const API_URL = 'http://localhost:8000/api/paises/'

class PaisService {

    async getPaises() {
        const response = await axios.get(API_URL)
        
        return response.data.data
    }
    async createPais(data) {
        const response = await axios.post(`${API_URL}crear/`, data)

        return response.data
    }

    async updatePais(id, data) {
        const response = await axios.put(`${API_URL}actualizar/${id}/`, data)

        return response.data
    }

    async deletePais(id) {
        const response = await axios.patch(`${API_URL}eliminar/${id}/`, { estado: 3 })

        return response.data
    }
}
export default new PaisService()
