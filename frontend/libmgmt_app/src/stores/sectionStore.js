import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";


export const useSectionStore = defineStore('section', () => {
    const errorMessage = ref(null);
    const section = ref(null);
    const allSections = ref([]);
    const allSectionNames = ref([]);
    const selectedSection = ref({});

    async function sectionRegistration(sectionData){
        const sectionPayLoad = {
            name : sectionData.name,
            dateCreated : sectionData.dateCreated,
            description : sectionData.description,
            rating: 0
        };

        try{
            const response =  await axios.post(`http://localhost:5000/api/section`, sectionPayLoad, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('jwt')
                }
            })
            section.value = response.data;
        }
        catch(error){
            errorMessage.value = error.response ? error.response.data.message.message : error.message;
            throw Error(error);
        }
    }

    async function retrieveAllSections(){
        try{
            const response =  await axios.get(`http://localhost:5000/api/section`, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('jwt')
                }
            })
            allSections.value = Object.values(response.data);
        }
        catch(error){
            errorMessage.value = error.response ? error.response.data.message.message : error.message;
            throw Error(error);
        }
    }

    async function currentSection(id){
        try{
            const response =  await axios.get(`http://localhost:5000/api/section/${id}`, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('jwt')
                }
            })
            selectedSection.value = response.data;
        }
        catch(error){
            errorMessage.value = error.response ? error.response.data.message.message : error.message;
            throw Error(error);
        }
    }

    async function updateSection(id, sectionUpdateData){
        try{
            const sectionUpdatePayLoad = {
                name : sectionUpdateData.name,
                dateCreated : sectionUpdateData.dateCreated,
                description : sectionUpdateData.description,
                rating: 0
            };

            const response =  await axios.put(`http://localhost:5000/api/section/${id}`, sectionUpdatePayLoad, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('jwt')
                }
            })
            console.log(response.data);
        }
        catch(error){
            errorMessage.value = error.response ? error.response.data.message.message : error.message;
            throw Error(error);
        }
    }

    async function deleteSection(id){
        try{
            await axios.delete(`http://localhost:5000/api/section/${id}`, {
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

    async function getAllSectionNames() {
        await retrieveAllSections();
        allSectionNames.value = [];
        allSections.value.forEach(s => {
            allSectionNames.value.push(s.name);
        })
    }

    return{
        errorMessage,
        section,
        allSections,
        allSectionNames,
        selectedSection,
        sectionRegistration,
        retrieveAllSections,
        currentSection,
        getAllSectionNames,
        updateSection,
        deleteSection
    }
})