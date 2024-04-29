<template>
    <div>
      <nav class="navbar bg-dark shadow">
        <div class="container-fluid">
          <router-link to="/" class="navbar-brand">Library</router-link>
        </div>
      </nav>
  
      <h1 class="p-5">User Login <span class="text-secondary fs-5 ms-5">New user? <router-link to="/user_register" class="btn btn-outline-secondary">Register</router-link></span> <span class="text-danger fs-3">{{ errorMessage }}</span></h1>
  
      <form @submit.prevent="login" style="margin-top: 5%; width: 60%; margin-left: 20%;">
        <div class="my-3">
          <label for="user_email" class="form-label">Email address</label>
          <input type="email" v-model="userEmail" class="form-control" id="user_email" name="user_email">
        </div>
        <div class="mt-4">
          <label for="user_password" class="form-label">Password</label>
          <input type="password" v-model="userPassword" class="form-control" id="user_password" name="user_password">
        </div>
  
        <button type="submit" class="btn mt-4 btn-outline-primary">Submit</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'user_login',
    data() {
      return {
        userEmail: '',
        userPassword: '',
        errorMessage: '', // New data property to store error message
      };
    },
    methods: {
      async login() {
        try {
          const response = await fetch('http://localhost:8080/backend/user_login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              user_email: this.userEmail,
              user_password: this.userPassword,
            }),
          });
  
          const data = await response.json();
  
          if (data.access_token) {
            console.log(data.access_token)
            localStorage.setItem('jwtToken', data.access_token);
            localStorage.setItem('name', data.name);
            // Redirect to user dashboard upon successful login
            this.$router.push('/user_dash');
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
  
  <style>
  /* Add any custom CSS styles here */
  </style>
  