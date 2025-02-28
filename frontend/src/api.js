import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000';

export const submitRequest = async (text) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/submit-request`, { text });
        return response.data;
    } catch (error) {
        console.error('Error submitting request:', error);
        throw error;
    }
};

export const speechToText = async (audioFile) => {
    const formData = new FormData();
    formData.append('audio', audioFile);
    try {
        const response = await axios.post(`${API_BASE_URL}/speech-to-text`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
        return response.data;
    } catch (error) {
        console.error('Error processing speech-to-text:', error);
        throw error;
    }
};
