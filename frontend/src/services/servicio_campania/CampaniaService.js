import axios from 'axios'

const API_URL = 'http://localhost:8000/api/campanias/'

class CampaniaService {

    async getCampanias() {
        const response = await axios.get(API_URL)
        
        return response.data.data
    }
    async createCampania(data) {
        const response = await axios.post(`${API_URL}crear/`, data)

        return response.data
    }

    async updateCampania(id, data) {
        const response = await axios.put(`${API_URL}actualizar/${id}/`, data)

        return response.data
    }

    async deleteCampania(id) {
        const response = await axios.patch(`${API_URL}eliminar/${id}/`, { estado: 3 })

        return response.data
    }
}
export default new CampaniaService()
