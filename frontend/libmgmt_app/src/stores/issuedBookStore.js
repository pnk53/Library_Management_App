import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useIssuedBookStore = defineStore('issuedBookStore', () => {

    const errorMessage = ref(null);
    const issuedBook = ref(null);
    const allIssuedBooks = ref([]);
    const requestedBook = ref(null);

    async function registerIssuedBook(id, bName, issuedBookData) {
        const date = new Date();
        const todayDate = date.toISOString().split('T')[0];
        const date2 = new Date();
        date2.setDate(date2.getDate() + 7);
        const finalEndDate = date2.toISOString().split('T')[0];
        const issuedBookPayLoad = {
            status: "Ongoing",
            issuedDate: todayDate,
            returnedDate: finalEndDate,
            bookId: parseInt(id,10),
            bookName: bName,
            userId: issuedBookData.userId,
            issuerName: issuedBookData.username
        }
        try {
            const response = await axios.post(`http://localhost:5000/api/issuedBook`, issuedBookPayLoad, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('jwt')
                }
            })
            issuedBook.value = response.data;
        }
        catch (error) {
            errorMessage.value = error.response ? error.response.data.message.message : error.message;
            throw Error(error);
        }
    }

    async function retrieveAllIssuedBooks(){
        try {
            const response = await axios.get(`http://localhost:5000/api/issuedBook`, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('jwt')
                }
            })
            allIssuedBooks.value = Object.values(response.data);
        }
        catch (error) {
            errorMessage.value = error.response ? error.response.data.message.message : error.message;
            throw Error(error);
        }
    }

    async function requestBookDetails(id, bName, requestedBookData){
        const requestBookPayLoad = {
            status: "Requested",
            // issuedDate: todayDate,
            // returnedDate: finalEndDate,
            bookId: parseInt(id,10),
            bookName: bName,
            userId: requestedBookData.userId,
            issuerName: requestedBookData.username
        }
        try {
            const response = await axios.post(`http://localhost:5000/api/issuedBook`, requestBookPayLoad, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('jwt')
                }
            })
            requestedBook.value = response.data;
        }
        catch (error) {
            errorMessage.value = error.response ? error.response.data.message.message : error.message;
            throw Error(error);
        }
    }

    async function acceptBookRequest(id){
        const date = new Date();
        const todayDate = date.toISOString().split('T')[0];
        const date2 = new Date();
        date2.setDate(date2.getDate() + 7);
        const finalEndDate = date2.toISOString().split('T')[0];
        const acceptBookPayLoad = {
            status: "Ongoing",
            issuedDate: todayDate,
            returnedDate: finalEndDate,
        }
        try {
            await axios.put(`http://localhost:5000/api/issuedBook/${id}`, acceptBookPayLoad, {
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

    async function revokeBookRequest(id){
        const date = new Date();
        const todayDate = date.toISOString().split('T')[0];
        const revokeBookPayLoad = {
            status: "Revoked",
            returnedDate: todayDate,
        }
        try {
            await axios.put(`http://localhost:5000/api/issuedBook/${id}`, revokeBookPayLoad, {
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

    return {
        errorMessage,
        issuedBook,
        allIssuedBooks,
        requestedBook,
        registerIssuedBook,
        retrieveAllIssuedBooks,
        requestBookDetails,
        acceptBookRequest,
        revokeBookRequest
    }
})