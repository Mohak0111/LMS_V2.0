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
                        <h5 class="offcanvas-title" id="offcanvasDarkNavbarLabel">Hi, {{ username }}</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas"
                            aria-label="Close"></button>
                    </div>
                    <div class="offcanvas-body">
                        <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
                            <li class="nav-item">
                                <router-link to="/user_dash" class="nav-link">Home</router-link>
                            </li>
                            <li class="nav-item">
                                <router-link to="/user_requests" class="nav-link">My Requests</router-link>
                            </li>
                            <li class="nav-item">
                                <router-link to="/user_books" class="nav-link active">My Books</router-link>
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
            <h1 id="heading" class="mt-5">Book View</h1>
            <div class="shadow-lg p-3 border rounded">
                <div class="m-3">
                    <div class="border rounded p-2 shadow">
                        <div class="text-center">
                            <h1>{{ book.book_name }}</h1>
                            <h1 class="fs-4 text-secondary">{{ book.book_authors }}</h1>
                        </div>
                        <p>{{ book.book_content }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: "user_view",
    data() {
        return {
            username:"",
            book: {}
        };
    },
    mounted() {
        this.fetchData();
    },
    methods: {
        async fetchData() {
            try {
                this.username = localStorage.getItem("name");
                const token = localStorage.getItem('jwtToken');
                const response = await fetch('http://localhost:8080/backend/user_view', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ book_id: this.$route.params.book_id })
                });

                if (response.ok) {
                    const data = await response.json();
                    this.book = data.book;
                    console.log('Data received:', data);
                } else {
                    console.error('Failed to fetch data:', response.statusText);
                }
            } catch (error) {
                console.error('An error occurred while fetching data:', error);
            }
        },
    }
}
</script>

<style>
/* Add your custom styles here */
</style>