import axios from 'axios';

const api = {
    getItems: async () => {
        try {
            const response = await axios.get(`/item/`);
            return response.data;
        } catch (error) {
            console.error('Error fetching items:', error);
            throw error;
        }
    },

    createItem: async (name) => {
        try {
            await axios.post(`/item/`, {name});
        } catch (error) {
            console.error('Error creating item:', error);
            throw error;
        }
    },

    updateItem: async (itemId, isActive) => {
        try {
            await axios.put(`/item/${itemId}/`, {is_active: isActive});
        } catch (error) {
            console.error('Error updating item:', error);
            throw error;
        }
    },

    deleteItem: async (itemId) => {
        try {
            await axios.delete(`/item/${itemId}/`);
        } catch (error) {
            console.error('Error deleting item:', error);
            throw error;
        }
    },
};

export default api;
