<template>
    <div>
        <nav class="navbar navbar-dark bg-dark fixed-top shadow">
            <div class="container-fluid">
                <a class="navbar-brand" href="/">Library</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas"
                    data-bs-target="#offcanvasDarkNavbar" aria-controls="offcanvasDarkNavbar"
                    aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="offcanvas offcanvas-end text-bg-dark" tabindex="-1" id="offcanvasDarkNavbar"
                    aria-labelledby="offcanvasDarkNavbarLabel">
                    <div class="offcanvas-header">
                        <h5 class="offcanvas-title" id="offcanvasDarkNavbarLabel">Hi, {{ name }}</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas"
                            aria-label="Close"></button>
                    </div>
                    <div class="offcanvas-body">
                        <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
                            <li class="nav-item">
                                <a class="nav-link" href="/user_dash">Home</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="/user_requests">My Requests</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link active" href="/user_books">My Books</a>
                            </li>
                            <li class="nav-item">
                                <a class="my-3 btn btn-success" href="/user_search">search</a>
                            </li>
                        </ul>
                        <a href="/logout" class="btn btn-outline-danger mt-5">Logout</a>
                    </div>
                </div>
            </div>
        </nav>

        <div class="mt-5 p-2 container toggle-hidden">
            <h1 id="heading" class="mt-5">Feedback</h1>
            <form class="shadow-lg p-3 border rounded" @submit.prevent="submitFeedback">
                <div class="m-3">
                    <div class="border rounded p-2 shadow text-center">
                        <h1>{{ book.book_name }}</h1>
                        <h1 class="fs-4 text-secondary">{{ book.book_authors }}</h1>
                    </div>
                    <label for="feedback" class="form-label mt-5">Enter Feedback:</label>
                    <input type="text" v-model="feedback" name="feedback" id="feedback" class="form-control">
                    <input type="text" name="book_id" id="book_id" hidden readonly :value="book.book_id">
                </div>
                <button type="submit" class="m-3 btn btn-success">Submit</button>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    name: "user_feedback",
    data() {
        return {
            name:"",
            feedback: '',
            book: {}, // Assuming book object will be passed as a prop
        };
    },
    mounted() {
        this.name=localStorage.getItem("name")
        this.fetchData()
    },
    methods: {
        async fetchData() {
            try {
                const token = localStorage.getItem('jwtToken');
                const bookId = this.$route.params.book_id;
                const response = await fetch('http://localhost:8080/backend/user_feedback', {
                    method: 'PUT',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        book_id: bookId,
                    }),
                });

                if (response.ok) {
            const data = await response.json();
            this.book=data.book;
            this.feedback=data.feedback;

                    console.log(data)

                    // this.$router.push("/user_dash")
                } else {
                    console.error('Failed to fetch data:', response.statusText);
                }
            } catch (error) {
                console.error('An error occurred while fetching data:', error);
            }
        },
        async submitFeedback() {
            try {
                const token = localStorage.getItem('jwtToken');
                const feedback=this.feedback;
                const bookId = this.$route.params.book_id;
                const response = await fetch('http://localhost:8080/backend/user_feedback', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        feedback: feedback,
                        book_id:bookId
                    }),
                });

                if (response.ok) {
            const data = await response.json();
            this.book=data.book;
            this.feedback=data.feedback;

                    console.log(data)

                    this.$router.push("/user_dash")
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

<style scoped>
/* Add your component-specific styles here */
</style>