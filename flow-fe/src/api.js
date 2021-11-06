const axios = require("axios")

const client = axios.create({
    baseURL: 'http://localhost:8000',
})

const api = {
    getProcess: () => {
        return client.get('/process')
    },
    getActiveStep: () => {
        return client.get('/process-step')
    },
    submitForm: (form) => {
        return client.post('/process-step', form)
    },
    getProcessGraph: () => {
        return client.get('/process-graph', { responseType: 'blob' })
    }
}


export default api
