import axios from 'axios';

export const useApiUploadService = () => {
    
    const axiosConfig = () => ({
        headers: {
            'Authorization': `JWT ${localStorage.getItem('access')}`,
        },
    });

    const getCsrfToken = () => {
        return document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];
    };

    const axiosConfigDownload = (additionalConfig = {}) => ({
        headers: {
            'Authorization': `JWT ${localStorage.getItem('access')}`,
            'X-CSRFToken': getCsrfToken(),
            ...additionalConfig.headers
        },
        ...additionalConfig
    });

    const uploadFile = async (fileBlob, fileName) => {
        const formData = new FormData();
        formData.append('pdf_file', fileBlob, fileName);

        try {
            const response = await axios.post(`${process.env.REACT_APP_API_URL}/api/upload-pdf/`, formData, axiosConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    };

    const getFiles = async () => {
        try {
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/list-words/`, axiosConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    };

    const getSubscriptionsTypes = async () => {
        try {
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/list-subscriptions/`, axiosConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    };

    const downloadWithAxios = async (fileId, title) => {
        try {
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/download-word/${fileId}/`, axiosConfigDownload({ responseType: 'arraybuffer' }));

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `${title}.docx`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            return response.data;
        } catch (error) {
            throw error;
        }
    };

    const deleteWithAxios = async (fileId) => {
        try {
            const response = await axios.delete(`${process.env.REACT_APP_API_URL}/api/delete-word/${fileId}/`, axiosConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    };

    return {
        uploadFile,
        getFiles,
        downloadWithAxios,
        getSubscriptionsTypes,
        deleteWithAxios,
        axiosConfig,
    };
};
