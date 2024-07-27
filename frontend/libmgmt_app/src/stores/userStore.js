import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useUserStore = defineStore('user', () => {

    const user = ref(null);
    const errorMessage = ref(null);

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

    return{
        userRegistration,
        userLogin,
        user,
        errorMessage
    }
})