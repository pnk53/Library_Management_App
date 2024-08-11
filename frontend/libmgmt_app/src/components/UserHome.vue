<template>
    <div class="container-fluid">
        <div class="row p-3">
            <div class="col-md-12 col-lg-12 col-sm-12">
                <h1 class="text-warning">
                    Welcome {{ user.name }}
                </h1>
                <p class="text-secondary">
                    This is user homepage, where user can see the details related requests and books.
                </p>
            </div>
        </div>
        <div class="row">
            <div class="col-md-5 col-lg-5 col-sm-12">
                <div class="border border-light rounded p-4">
                    <h3 class="text-white">Book Request Details</h3>
                    <div class="myReqCont">
                        <h3 class="text-white" v-if="allOngoingBooks.length == 0 && allRequestedBooks.length == 0 && allRevokedBooks.length ==0">No request histroy</h3>
                        <table class="table" v-else>
                            <tr class="bg-gradient">
                                <th>Book Name</th>
                                <th>Status</th>
                                <th>Revoke Date</th>
                            </tr>
                            <tr v-for="obook in allOngoingBooks" :key="obook.id" class="bg-success bg-gradient">
                                <td>{{ obook.bookName}}</td>
                                <td>{{ obook.status }}</td>
                                <td>{{ obook.returnedDate }}</td>
                            </tr>
                            <tr v-for="rbook in allRequestedBooks" :key="rbook.id" class="bg-warning bg-gradient">
                                <td>{{ rbook.bookName}}</td>
                                <td>{{ rbook.status }}</td>
                                <td>{{ rbook.returnedDate }}</td>
                            </tr>
                            <tr v-for="book in allRevokedBooks" :key="book.id" class="bg-danger bg-gradient">
                                <td>{{ book.bookName}}</td>
                                <td>{{ book.status }}</td>
                                <td>{{ book.returnedDate }}</td>
                            </tr>
                    </table>
                    </div>
                </div>
            </div>
            <div class="col-md-7 col-lg-7 col-sm-12">
                <div class="border border-info rounded p-4">
                    <h3 class="text-info">Issued Books Details</h3>
                    <div class="myReqCont">
                        <h3 class="text-info" v-if="allIssuedBooks.length ==0">No Books issued at the moment.</h3>
                        <table class="table" v-else>
                            <tr class="bg-gradient">
                                <th>Book Name</th>
                                <th>Status</th>
                                <th>Revoke Date</th>
                                <th>View</th>
                            </tr>
                            <tr v-for="book in allIssuedBooks" :key="book.id" class="bg-info bg-gradient">
                                <td>{{ book.title}}</td>
                                <td>{{ book.status }}</td>
                                <td>{{ book.returnedDate }}</td>
                                <td><button class="btn btn-sm btn-dark ps-5 pe-5" @click="viewEBook(book.id)">View</button></td>
                            </tr>
                    </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useIssuedBookStore } from '@/stores/issuedBookStore';
import { useEBookStore } from '@/stores/ebookStore';

const user = {
    "name": localStorage.getItem('name'),
    "user_id": localStorage.getItem('user_id')
}

const allRequestedBooks = ref([]);
const allOngoingBooks = ref([]);
const allRevokedBooks = ref([]);
const allIssuedBooks = ref([]);

const issuedBookStore = useIssuedBookStore();
const eBookStore = useEBookStore();
const router = useRouter();

onMounted(async()=>{
    await issuedBookStore.retrieveAllIssuedBooks();
    allRequestedBooks.value = issuedBookStore.allIssuedBooks.filter(rb => rb.status == "Requested" && rb.userId == user.user_id);
    allOngoingBooks.value = issuedBookStore.allIssuedBooks.filter(ob => ob.status == "Ongoing" && ob.userId == user.user_id);
    allRevokedBooks.value = issuedBookStore.allIssuedBooks.filter(b => b.status == "Revoked" && b.userId == user.user_id);

    await eBookStore.retrieveAllEBooks();
    allIssuedBooks.value = eBookStore.allEBooks.filter(b => b.currentIssuer == user.user_id && b.status == "Issued");
})

function viewEBook(id) {
    router.push({ name: 'ViewEBook', params: { eBookId: id } });
}

</script>

<style scoped>
.myReqCont{
    max-height: 80dvh;
    overflow-y: auto;
}

table {
    width: 100%;
    border-collapse: collapse;
    border-spacing: 0;
}

th,
td {
    padding: 12px;
    text-align: left;
    color: #212529;
    border: 2px solid #212529;
}

th {
    background-color: #fff;
    color: #212529;
}
</style>