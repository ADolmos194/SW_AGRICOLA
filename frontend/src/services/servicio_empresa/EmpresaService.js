import axios from 'axios'

const API_URL = 'http://localhost:8000/api/empresas/'

class EmpresaService {

    async getEmpresas() {
        const response = await axios.get(API_URL)
        
        return response.data.data 
    }

    async createEmpresa(data) {
        const response = await axios.post(API_URL + 'crear/', data)

        return response.data // La respuesta ya tiene el formato correcto
    }
    
    async updateEmpresa(id, data) {
        const response = await axios.put(API_URL + `actualizar/${id}/`, data)

        return response.data
    }

    async deleteEmpresa(id) {
        const response = await axios.patch(API_URL + `eliminar/${id}/`, { estado: 3 })

        return response.data
    }
}
export default new EmpresaService()
