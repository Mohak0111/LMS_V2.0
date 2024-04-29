<template>
    <div>
        <nav class="navbar bg-dark shadow" data-bs-theme="dark">
            <div class="container-fluid">
                <router-link class="navbar-brand" to="/">Library</router-link>
            </div>
        </nav>
        <h1 class="p-5">User Register <span class="text-danger fs-3"><span class="text-secondary fs-5 ms-5">Existing
                    user? <router-link to="/user_login" class="btn btn-outline-secondary">Login</router-link></span>
                <span class="text-danger fs-3"></span> <span v-if="error">{{ error }}</span></span></h1>
        <form @submit.prevent="registerUser" style="margin-top: 5%; width: 60%; margin-left: 20%;">
            <div class="my-3">
                <label for="user_email" class="form-label">Email address</label>
                <input v-model="user_email" type="email" class="form-control" id="user_email" name="user_email">
            </div>
            <div class="my-3">
                <label for="user_name" class="form-label">Name</label>
                <input v-model="user_name" type="text" class="form-control" id="user_name" name="user_name">
            </div>
            <div class="mt-4">
                <label for="user_password" class="form-label">Password</label>
                <input v-model="user_password" type="password" class="form-control" id="user_password"
                    name="user_password">
            </div>
            <button type="submit" class="btn mt-4 btn-outline-primary">Submit</button>
        </form>
    </div>
</template>

<script>
export default {
    data() {
        return {
            user_email: '',
            user_password: '',
            user_name: '',
            error: ''
        };
    },
    methods: {
        async registerUser() {
            try {
                const response = await fetch('http://192.168.1.9:8080/backend/user_register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ "user_email": this.user_email, "user_password": this.user_password, "user_name":this.user_name })
                });

                const data = await response.json();

                if (data.access_token) {
                    console.log(data.access_token)
                    localStorage.setItem('jwtToken', data.access_token);
                    localStorage.setItem('name', this.user_name);
                    // Store the JWT token in the Vuex store
                    this.$store.dispatch('setToken', data.access_token);
                    // Redirect to librarian_dashboard upon successful login
                    this.$router.push('/user_dash');
                } else {
                    // Display the error message from the backend
                    this.error = data.error;
                }
                // Optionally handle successful registration, such as redirecting to a login page
            } catch (error) {
                this.error = error.message;
            }
        }
    }
};
</script>

<style scoped>
/* Add your component-specific styles here */
</style>