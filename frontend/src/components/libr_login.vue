<template>
    <div>
      <nav class="navbar bg-dark shadow">
        <div class="container-fluid">
          <router-link to="/" class="navbar-brand">Library</router-link>
        </div>
      </nav>
  
      <h1 class="p-5">Librarian Login</h1>
  
      <form @submit.prevent="login" style="margin-top: 5%; width: 60%; margin-left: 20%;">
        <div class="my-3">
          <label for="libr_email" class="form-label">Email address</label>
          <input type="email" v-model="librEmail" class="form-control" id="libr_email" name="libr_email">
        </div>
        <div class="mt-4">
          <label for="libr_password" class="form-label">Password</label>
          <input type="password" v-model="librPassword" class="form-control" id="libr_password" name="libr_password">
        </div>
  
        <button type="submit" class="btn mt-4 btn-outline-primary">Submit</button>
      </form>
  
      <div v-if="errorMessage" class="text-danger mt-2">
        {{ errorMessage }}
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'librarian_login',
    data() {
      return {
        librEmail: '',
        librPassword: '',
        errorMessage: '', // New data property to store error message
      };
    },
    methods: {
      async login() {
        // Send a request to your API to authenticate the librarian
        // Replace with your actual API endpoint
        try {
          const response = await fetch('http://localhost:8080/backend/libr_login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              libr_email: this.librEmail,
              libr_password: this.librPassword,
            }),
          });
  
          const data = await response.json();
  
          if (data.access_token) {
            console.log(data.access_token)
            localStorage.setItem('jwtToken', data.access_token);
            localStorage.setItem('name', data.name);
            // Store the JWT token in the Vuex store
            this.$store.dispatch('setToken', data.access_token);
            // Redirect to librarian_dashboard upon successful login
            this.$router.push('/libr_dash');
          } else {
            // Display the error message from the backend
            this.errorMessage = data.error;
          }
        } catch (error) {
          console.error(error);
        }
      },
    },
  };
  </script>
  