<template>
<div class="">
    <nav class="navbar navbar-dark bg-dark fixed-top shadow">
        <div class="container-fluid">
            <router-link to="/" class="navbar-brand">Library</router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas"
                data-bs-target="#offcanvasDarkNavbar" aria-controls="offcanvasDarkNavbar"
                aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="offcanvas offcanvas-end text-bg-dark" tabindex="-1" id="offcanvasDarkNavbar"
                aria-labelledby="offcanvasDarkNavbarLabel">
                <div class="offcanvas-header">
                    <h5 class="offcanvas-title" id="offcanvasDarkNavbarLabel">Hi, {{ user_name }}</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas"
                        aria-label="Close"></button>
                </div>
                <div class="offcanvas-body">
                    <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
                        <li class="nav-item">
                            <router-link to="/user_dash" class="nav-link active">Home</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/user_requests" class="nav-link">My Requests</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/user_books" class="nav-link">My Books</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/user_search" class="my-3 btn btn-success">Search</router-link>
                        </li>
                    </ul>
                    <router-link to="/logout" class="btn btn-outline-danger mt-5">Logout</router-link>
                </div>
            </div>
        </div>
    </nav>
    <div class="mt-5 p-2 container toggle-hidden">
        <h1 id="heading" class="mt-5">Book Request</h1>
        <form class="shadow-lg p-3 border rounded" @submit.prevent="handleSubmit()">
          <div class="m-3">
            <div class="border rounded p-2 shadow text-center">
            <h1>{{book.book_name}}</h1>
            <h1 class="fs-4 text-secondary">{{book.book_authors}}</h1>
        </div>
            <label for="days" class="form-label mt-5">How many days do you want the book for? (max=7)</label>
            <input v-model="num_days" type="number" class="form-control" id="days" name="days" min="1" step="1" max="7" required>
          </div>
          <button type="submit" class="m-3 btn btn-success">Request</button>
        </form>
      </div>
</div>
</template>
<script>
export default {
    name: "user_request",
    mounted() {
        this.fetchData()
    },
    data(){
        return {
            book:{},
            user:{},
            user_name:"",
            num_days:""

        }
    },
    methods: {
        async fetchData() {
            const token = localStorage.getItem("jwtToken")
            this.user_name = localStorage.getItem("name")
            const response = await fetch('http://localhost:8080/backend/user_request', {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body:JSON.stringify({book_id: this.$route.params.book_id})
            });
            if (response.ok) {
                const data = await response.json();
                this.user_name=localStorage.getItem("name")
                this.book=data.book 
                this.user=data.user
            }
        },
        async handleSubmit() {
            const token = localStorage.getItem("jwtToken")
            const response = await fetch('http://localhost:8080/backend/user_request', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body:JSON.stringify({book_id: this.$route.params.book_id, days:this.num_days})
            });
            if (response.ok) {
                this.$router.push("/user_dash")
            }
        }
    }
}
</script>