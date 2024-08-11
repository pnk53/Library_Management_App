import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useUserStore = defineStore('userStore', () => {

    const user = ref(null);
    const errorMessage = ref(null);
    const allUsers = ref([]);
    const selectedUser = ref({});

    async function userRegistration(userData){

        const userPayLoad = {
            userType : "User",
            visitedToday : "False",
            flagged : "False",
            firstName : userData.firstName,
            lastName : userData.lastName,
            username : userData.username,
            email : userData.email,
            password : userData.password.password
        };

        try{
            const response = await axios.post(`http://localhost:5000/api/user`, userPayLoad, {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            user.value = response.data;
        }
        catch(error){
            errorMessage.value = error.response ? error.response.data.message.message : error.message;
            throw Error(error);
        }
        
    }

    async function userLogin(userData){
        const userPayLoad = {
            username: userData.username,
            password: userData.password
        };

        try{
            const response = await axios.post(`http://localhost:5000/login`, userPayLoad, {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            user.value = response.data;
            localStorage.setItem('name', user.value.name),
            localStorage.setItem('user_id', user.value.user_id),
            localStorage.setItem('userType', user.value.userType),
            localStorage.setItem('jwt', user.value.jwt),
            localStorage.setItem('exp', user.value.exp)
        }
        catch(error){
            errorMessage.value = error.response ? error.response.data.message : error.message;
            throw Error(error);
        }
    }

    async function retrieveAllUsers(){
        try{
            const response =  await axios.get(`http://localhost:5000/api/user`, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('jwt')
                }
            })
            allUsers.value = Object.values(response.data).filter(u => u.userType == "User");
        }
        catch(error){
            errorMessage.value = error.response ? error.response.data.message.message : error.message;
            throw Error(error);
        }
    }

    async function currentUser(id) {
        try {
            const response = await axios.get(`http://localhost:5000/api/user/${id}`, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('jwt')
                }
            })
            selectedUser.value = response.data;
        }
        catch (error) {
            errorMessage.value = error.response ? error.response.data.message.message : error.message;
            throw Error(error);
        }
    }

    async function userUpdate(id, userData){

        const userUpdatePayLoad = {
            firstName : userData.firstName,
            lastName : userData.lastName,
            username : userData.username,
            email : userData.email
        };

        try{
            await axios.put(`http://localhost:5000/api/user/${id}`, userUpdatePayLoad, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('jwt')
                }
            })
        }
        catch(error){
            errorMessage.value = error.response ? error.response.data.message.message : error.message;
            throw Error(error);
        }
    }

    return{
        userRegistration,
        userLogin,
        retrieveAllUsers,
        currentUser,
        userUpdate,
        user,
        errorMessage,
        selectedUser,
        allUsers
    }
})