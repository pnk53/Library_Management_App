<template>
    <div class="container-fluid">
        <div class="row p-5">
            <div class="col-md-8 offset-md-2 col-lg-8 offset-lg-2 col-sm-10 offset-sm-1 border p-5 rounded-pill">
                <div class="row">
                    <form @submit.prevent="onSearchSubmit" class="col-md-12 col-lg-8 col-sm-12">
                        <div class="row">
                            <div class="col-md-8 col-lg-8 col-sm-12">
                                <input type="text" id="search" class="form-control" name="search"
                                    placeholder="Search for users" v-model="searchState.search"
                                    :class="{ 'is-invalid': vSearch.search.$error }">
                                <div class="invalid-feedback" v-if="vSearch.search.$error">
                                    {{ vSearch.search.$errors[0].$message }}
                                </div>
                            </div>
                            <div class="col-md-4 col-lg-4 col-sm-12">
                                <button class="btn btn-outline-success ps-5 pe-5" type="submit"
                                    :disabled="vSearch.$invalid">Search</button>
                            </div>
                        </div>
                    </form>
                    <div class="col-md-12 col-lg-4 col-sm-12 ms-auto">
                        <button class="btn btn-outline-info ps-4 pe-4" :disabled="vSearch.$invalid"
                            @click="clearSearch">Clear
                            Results</button>
                    </div>
                </div>
            </div>
        </div>
        <div class="row pe-5 ps-5">
            <div v-if="searchedUserResults.length > 0 || searchedUserFlaggedResults.length > 0">
                <h3 class="mt-5">Your search results: </h3>
                <div class="bg-info bg-gradient rounded p-3 mt-3">
                    <h5 class="text-dark">Users</h5>
                    <table class="table">
                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Username</th>
                            <th>Flag</th>
                        </tr>
                        <tr v-for="user in searchedUserResults" :key="user.id">
                            <td>{{ user.firstName }} {{ user.lastName }}</td>
                            <td>{{ user.email }}</td>
                            <td>{{ user.username }}</td>
                            <td>
                                <button class="btn btn-warning pe-5 ps-5"
                                    @click="flagCurrentUser(user.id, true)">Flag</button>
                            </td>
                        </tr>
                    </table>
                </div>
                <div class="bg-warning bg-gradient rounded p-3 mt-3">
                    <h5 class="text-dark">Flagged Users</h5>
                    <table class="table">
                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Username</th>
                            <th>Un-Flag</th>
                        </tr>
                        <tr v-for="user in searchedUserFlaggedResults" :key="user.id">
                            <td>{{ user.firstName }} {{ user.lastName }}</td>
                            <td>{{ user.email }}</td>
                            <td>{{ user.username }}</td>
                            <td>
                                <button class="btn btn-warning pe-5 ps-5"
                                    @click="flagCurrentUser(user.id, false)">Un-Flag</button>
                            </td>
                        </tr>
                    </table>
                </div>
            </div>
        </div>
        <div class="row p-5">
            <div class="btn-group btn-group-lg" role="group">
                <button :class="['btn', selectedGraph === 'users' ? 'btn-warning' : 'btn-outline-warning']"
                    @click="viewCurrentGraph('users')">Users</button>
                <button :class="['btn', selectedGraph === 'sections' ? 'btn-warning' : 'btn-outline-warning']"
                    @click="viewCurrentGraph('sections')">Sections</button>
                <button :class="['btn', selectedGraph === 'books' ? 'btn-warning' : 'btn-outline-warning']"
                    @click="viewCurrentGraph('books')">Books</button>
                <button :class="['btn', selectedGraph === 'issued books' ? 'btn-warning' : 'btn-outline-warning']"
                    @click="viewCurrentGraph('issued books')">Issued Books</button>
            </div>
        </div>
        <div class="row ps-5 pe-5">
            <h3 class="text-center text-uppercase">{{ selectedGraph }} Statistics</h3>
            <iframe ref="chartFrame" height="600" class="myIFrame">

            </iframe>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref, computed, reactive, watch } from 'vue';
import { required } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { useUserStore } from '@/stores/userStore';
import { useEBookStore } from '@/stores/ebookStore';
import { useIssuedBookStore } from '@/stores/issuedBookStore';
import { useSearchStore } from '@/stores/searchStore';
import { useAlertStore } from '@/stores/alertStore';
import { Chart } from 'chart.js/auto';

const userStore = useUserStore();
const eBookStore = useEBookStore();
const issuedBookStore = useIssuedBookStore();
const searchStore = useSearchStore();
const alertStore = useAlertStore();

const searchState = reactive({
    search: ref(null)
})

const searchRules = computed(() => {
    return {
        search: { required }
    }
})

const vSearch = useVuelidate(searchRules, searchState, {
    $autoDirty: true
})

const searchedUserResults = ref([]);
const searchedUserFlaggedResults = ref([]);

const onSearchSubmit = (async () => {
    await searchStore.getAllSearchedUsers(searchState.search.toLowerCase());
    searchedUserResults.value = searchStore.searchedUser.filter(u => u.flagged == false);
    searchedUserFlaggedResults.value = searchStore.searchedUser.filter(u => u.flagged == true);
    if (searchedUserResults.value.length == 0 && searchedUserFlaggedResults.value.length == 0) {
        let message = "No search results for: " + searchState.search
        alertStore.error(message);
    }
})

const clearSearch = (() => {
    searchedUserResults.value = [];
})

const flagCurrentUser = (async (id, status) => {
    try {
        await userStore.flagUser(id, status);
        setTimeout(() => {
            let message = "User "
            if (status == true) {
                message = message + "flagged successfully"
            }
            else {
                message = message + "unflagged successfully"
            }
            alertStore.success(message);
        }, 200)
    }
    catch (error) {
        console.log(userStore.errorMessage);
        let message = "User flag failed: " + userStore.errorMessage;
        alertStore.error(message);
    }
})

const chartFrame = ref(null);
const selectedGraph = ref('users');

const viewCurrentGraph = async (type) => {
    if(type == "users"){
        selectedGraph.value = type;
    }
    else if(type == "sections"){
        await getPopularSection();
        selectedGraph.value = type;
    }
    else if(type == "books"){
        await getTopBooksData();
        selectedGraph.value = type;
    }
    else if(type == "issued books"){
        await getIssuedBooksStats();
        selectedGraph.value = type;
    }
}

watch(selectedGraph, (newType) => {
    loadChart(newType);
})

const aUsers = ref(0);
const bUsers = ref(0);
const rIssuedBooks = ref(0);
const oIssuedBooks = ref(0);
const rEIssuedBooks = ref(0);
const topBooks = ref([]);
const bookNames = [];
const bookRating = [];
const sectionNames = [];
const sectionValues = [];

const userChartData = {
    labels: ['Active', 'Flagged'],
    datasets: [{
        label: 'User Count: ',
        data: [aUsers, bUsers],
        backgroundColor: [
            'rgb(0, 255, 111)',
            'rgb(255, 46, 46)',
        ],
        hoverOffset: 4
    }]
};

const userChartConfig = {
    type: 'doughnut',
    data: userChartData,
    options: {
        radius: '100%',
        responsive: false,
        plugins: {
            legend: {
                position: 'left', // Move the legend to the left side
                labels: {
                    boxWidth: 20,
                    padding: 30,
                    font: {
                        size: 18,     // Increases font size of the legend
                    }
                }
            },
        }
    }
};

const bookChartData = {
    labels: bookNames,
    datasets: [{
        label: 'Rating: ',
        data: bookRating,
        backgroundColor: [
            'rgba(255, 99, 132)',
            'rgba(255, 159, 64)',
            'rgba(255, 205, 86)',
            'rgba(75, 192, 192)',
            'rgba(54, 162, 235)',
            'rgba(153, 102, 255)',
            'rgba(201, 203, 207)',
            'rgba(255, 99, 132)',
            'rgba(255, 159, 64)',
            'rgba(255, 205, 86)',
        ],
        borderColor: [
            'rgb(255, 99, 132)',
            'rgb(255, 159, 64)',
            'rgb(255, 205, 86)',
            'rgb(75, 192, 192)',
            'rgb(54, 162, 235)',
            'rgb(153, 102, 255)',
            'rgb(201, 203, 207)',
            'rgb(255, 99, 132)',
            'rgb(255, 159, 64)',
            'rgb(255, 205, 86)',
        ],
        borderWidth: 1
    }]
};

const bookChartConfig = {
    type: 'bar',
    data: bookChartData,
    options: {
        responsive: false,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true,
                max: 10,           
                ticks: {
                    stepSize: 1,
                    color: 'white'
                },
                title: { 
                    display: true,
                    text: 'Rating', 
                    color: 'white', 
                    font: {
                        size: 18,
                    }
                }
            },
            x: {
                ticks:{
                    color: 'white'
                },
                title: { 
                    display: true,
                    text: 'Books', 
                    color: 'white', 
                    font: {
                        size: 18,
                    }
                }
            }
        },
        plugins: {
            legend: {
                display: false,
            }
        },
    }
};

const sectionChartData = {
    labels: sectionNames,
    datasets: [{
        label: 'Number of Books: ',
        data: sectionValues,
        backgroundColor: [
            'rgba(255, 99, 132)',
            'rgba(255, 159, 64)',
            'rgba(255, 205, 86)',
            'rgba(75, 192, 192)',
            'rgba(54, 162, 235)',
            'rgba(153, 102, 255)',
            'rgba(201, 203, 207)',
            'rgba(255, 99, 132)',
            'rgba(255, 159, 64)',
            'rgba(255, 205, 86)',
        ],
        borderColor: [
            'rgb(255, 99, 132)',
            'rgb(255, 159, 64)',
            'rgb(255, 205, 86)',
            'rgb(75, 192, 192)',
            'rgb(54, 162, 235)',
            'rgb(153, 102, 255)',
            'rgb(201, 203, 207)',
            'rgb(255, 99, 132)',
            'rgb(255, 159, 64)',
            'rgb(255, 205, 86)',
        ],
        borderWidth: 1
    }]
};

const sectionChartConfig = {
    type: 'bar',
    data: sectionChartData,
    options: {
        responsive: false,
        maintainAspectRatio: false,
        indexAxis: 'y',
        scales: {
            y: {           
                ticks: {
                    color: 'white',
                },
                title: { 
                    display: true,
                    text: 'Sections', 
                    color: 'white', 
                    font: {
                        size: 18,
                    }
                }
            },
            x: {
                ticks:{
                    color: 'white',
                    stepSize: 1,
                },
                title: { 
                    display: true,
                    text: 'Number of Books', 
                    color: 'white', 
                    font: {
                        size: 18,
                    }
                }
            }
        },
        plugins: {
            legend: {
                display: false,
            }
        },
    }
};

const issuedBookChartData = {
    labels: ['Revoked', 'Ongoing','Requested'],
    datasets: [{
        label: 'Book Count: ',
        data: [rIssuedBooks, oIssuedBooks, rEIssuedBooks],
        backgroundColor: [
            'rgb(255, 46, 46)',
            'rgb(0, 255, 111)',
            'rgb(255, 255, 46)',
        ],
        hoverOffset: 4
    }]
};

const issuedBookChartConfig = {
    type: 'pie',
    data: issuedBookChartData,
    options: {
        radius: '100%',
        responsive: false,
        plugins: {
            legend: {
                position: 'left', // Move the legend to the left side
                labels: {
                    boxWidth: 20,
                    padding: 30,
                    font: {
                        size: 18,     // Increases font size of the legend
                    }
                }
            },
        }
    }
};

const loadChart = (type) => {
    const ctx = chartFrame.value.contentWindow.document.createElement('canvas');
    chartFrame.value.contentWindow.document.body.innerHTML = '';
    chartFrame.value.contentWindow.document.body.appendChild(ctx);
    ctx.width = 550;
    ctx.height = 550;
    ctx.style.margin = 'auto';
    if (type === 'users') {
        new Chart(ctx, userChartConfig);
    }
    else if (type === 'books') {
        new Chart(ctx, bookChartConfig);
    }
    else if (type === 'sections') {
        new Chart(ctx, sectionChartConfig);
    }
    else if (type === 'issued books'){
        new Chart(ctx, issuedBookChartConfig);
    }
};

onMounted(async () => {
    await userStore.retrieveAllUsers();
    aUsers.value = userStore.allUsers.filter(u => u.flagged == false).length;
    bUsers.value = userStore.allUsers.filter(u => u.flagged == true).length;
    loadChart(selectedGraph.value);
});

const getTopBooksData = (async () => {
    await eBookStore.retrieveAllEBooks();
    bookNames.length = 0;
    bookRating.length = 0;
    topBooks.value = eBookStore.allEBooks.sort((a, b) => b.rating - a.rating).slice(0, 10).sort(() => Math.random() - 0.5);
    for(let b in topBooks.value){
        bookNames.push(topBooks.value[b].title);
        bookRating.push(topBooks.value[b].rating);
    }
})

const getPopularSection = (async () => {
    await eBookStore.retrieveAllEBooks();
    sectionNames.length = 0;
    sectionValues.length = 0;
    const sectionMap = new Map();
    eBookStore.allEBooks.forEach(book => {
        let sectionList = book.section.split(',');
        for (let s in sectionList) {
            if (sectionMap.has(sectionList[s])) {
                sectionMap.set(sectionList[s], sectionMap.get(sectionList[s]) + 1);
            }
            else {
                sectionMap.set(sectionList[s], 1);
            }
        }
    });
    let top10Sections = Array.from(sectionMap).sort((a, b) => b[1] - a[1]).slice(0, 10).sort(() => Math.random() - 0.5);
    for(let x in top10Sections){
        sectionNames.push(top10Sections[x][0]);
        sectionValues.push(top10Sections[x][1]);
    }
})

const getIssuedBooksStats = (async () => {
    await issuedBookStore.retrieveAllIssuedBooks();
    rIssuedBooks.value = issuedBookStore.allIssuedBooks.filter(rb => rb.status === "Revoked").length;
    oIssuedBooks.value = issuedBookStore.allIssuedBooks.filter(ob => ob.status === "Ongoing").length;
    rEIssuedBooks.value = issuedBookStore.allIssuedBooks.filter(reb => reb.status === "Requested").length;
    console.log();
})

</script>

<style scoped>
.myCont {
    min-height: 50dvh;
}

table {
    width: 100%;
    border: 2px solid #000;
    border-collapse: collapse;
}

th,
td {
    padding: 12px;
    text-align: left;
    color: #212529;
    background-color: #f8f9fa;
    border-bottom: 1px solid #ddd;
}

th {
    background-color: #212529;
    color: white;
}

.myIFrame {
    border: 4px solid #6c757d;
    border-radius: 20px;
}
</style>