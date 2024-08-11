import { defineStore } from "pinia";
import { ref } from "vue";
import { useSectionStore } from "./sectionStore";
import { useEBookStore } from "./ebookStore";
import { useUserStore } from "./userStore";

export const useSearchStore = defineStore('searchStore', () => {
    const errorMessage = ref(null);
    const searchedSections = ref([]);
    const searchedEBooks = ref([]);
    const searchedUser = ref([]);
    const sectionStore = useSectionStore();
    const eBookStore = useEBookStore();
    const userStore = useUserStore();

    async function getAllSearchedSectionsAndEBooks(searchedData){
        await sectionStore.retrieveAllSections();
        searchedSections.value = sectionStore.allSections.filter(s => s.name.toLowerCase().includes(searchedData));

        await eBookStore.retrieveAllEBooks();
        searchedEBooks.value = eBookStore.allEBooks.filter(e => e.title.toLowerCase().includes(searchedData) || e.author.toLowerCase().includes(searchedData) || e.section.toLowerCase().includes(searchedData));
    }

    async function getAllSearchedUsers(searchedData){
        await userStore.retrieveAllUsers();
        searchedUser.value = userStore.allUsers.filter(u => u.firstName.toLowerCase().includes(searchedData) || u.username.toLowerCase().includes(searchedData))
    }

    return{
        errorMessage,
        searchedUser,
        searchedSections,
        searchedEBooks,
        getAllSearchedSectionsAndEBooks,
        getAllSearchedUsers
    }
})