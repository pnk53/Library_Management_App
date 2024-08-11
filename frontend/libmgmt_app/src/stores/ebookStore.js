import axios from "axios";
import { defineStore } from "pinia";
import { ref } from 'vue';

export const useEBookStore = defineStore('eBook', () => {
    const errorMessage = ref(null);
    const eBook = ref(null);
    const allEBooks = ref([]);
    const selectedEbook = ref({});

    async function addEBook(eBookData) {

        let formData = new FormData()
        formData.append('title', eBookData.title)
        formData.append('author', eBookData.author)
        formData.append('language', eBookData.language)
        formData.append('releaseDate', eBookData.releaseDate)
        formData.append('section', eBookData.section)
        formData.append('eBook', eBookData.ebook)

        try {
            const response = await axios.post("http://127.0.0.1:5000/api/book", formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Authorization': 'Bearer ' + localStorage.getItem('jwt')
                }
            });
            eBook.value = response.data
        }
        catch (error) {
            errorMessage.value = error.response ? error.response.data.message.message : error.message;
            throw Error(error);
        }
    }

    async function retrieveAllEBooks() {
        try {
            const response = await axios.get(`http://localhost:5000/api/book`, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('jwt')
                }
            })
            allEBooks.value = Object.values(response.data);
        }
        catch (error) {
            errorMessage.value = error.response ? error.response.data.message.message : error.message;
            throw Error(error);
        }
    }

    async function currentEBook(id) {
        try {
            const response = await axios.get(`http://localhost:5000/api/book/${id}`, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('jwt')
                }
            })
            selectedEbook.value = response.data;
        }
        catch (error) {
            errorMessage.value = error.response ? error.response.data.message.message : error.message;
            throw Error(error);
        }
    }

    async function updateEBook(id, eBookUpdateData, tRater) {
        try {
            const eBookUpdatePayLoad = {
                title: eBookUpdateData.title,
                author: eBookUpdateData.author,
                language: eBookUpdateData.language,
                releaseDate: eBookUpdateData.releaseDate,
                section: eBookUpdateData.section,
                rating: eBookUpdateData.rating,
                totalRater: tRater
            };

            const response = await axios.put(`http://localhost:5000/api/book/${id}`, eBookUpdatePayLoad, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('jwt')
                }
            })
            console.log(response.data);
        }
        catch (error) {
            errorMessage.value = error.response ? error.response.data.message.message : error.message;
            throw Error(error);
        }
    }

    async function deleteEBook(id) {
        try {
            await axios.delete(`http://localhost:5000/api/book/${id}`, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('jwt')
                }
            })
        }
        catch (error) {
            errorMessage.value = error.response ? error.response.data.message.message : error.message;
            throw Error(error);
        }
    }

    async function updateAssignedBookInfo(id, issuerData) {
        try {
            const date = new Date();
            const todayDate = date.toISOString().split('T')[0];
            const date2 = new Date();
            date2.setDate(date2.getDate() + 7);
            const finalEndDate = date2.toISOString().split('T')[0];
            const updateAssignedBookPayLoad = {
                status: "Issued",
                issuedDate: todayDate,
                returnedDate: finalEndDate,
                currentIssuer: issuerData.userId,
            }

            const response = await axios.put(`http://localhost:5000/api/book/${id}`, updateAssignedBookPayLoad, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('jwt')
                }
            })
            console.log(response.data);
        }
        catch (error) {
            errorMessage.value = error.response ? error.response.data.message.message : error.message;
            throw Error(error);
        }
    }

    async function updateRevokedBookInfo(id) {
        try {
            const updateRevokedBookPayLoad = {
                status: "Available",
                issuedDate: "",
                returnedDate: "",
                currentIssuer: 0,
            }
            const response = await axios.put(`http://localhost:5000/api/book/${id}`, updateRevokedBookPayLoad, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('jwt')
                }
            })
            console.log(response.data);
        }
        catch (error) {
            errorMessage.value = error.response ? error.response.data.message.message : error.message;
            throw Error(error);
        }
    }

    return {
        errorMessage,
        eBook,
        allEBooks,
        selectedEbook,
        addEBook,
        retrieveAllEBooks,
        currentEBook,
        updateEBook,
        deleteEBook,
        updateAssignedBookInfo,
        updateRevokedBookInfo
    }
})