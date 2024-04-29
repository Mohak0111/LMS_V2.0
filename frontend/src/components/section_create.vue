<template>
    <div>
        <nav class="navbar navbar-dark bg-dark fixed-top shadow">
            <div class="container-fluid">
              <router-link to="/" class="navbar-brand">Library</router-link>
              <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasDarkNavbar" aria-controls="offcanvasDarkNavbar" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
              </button>
              <div class="offcanvas offcanvas-end text-bg-dark" tabindex="-1" id="offcanvasDarkNavbar" aria-labelledby="offcanvasDarkNavbarLabel">
                <div class="offcanvas-header">
                  <h5 class="offcanvas-title" id="offcanvasDarkNavbarLabel">Hi, {{name}}</h5>
                  <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas" aria-label="Close"></button>
                </div>
                <div class="offcanvas-body">
                  <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
                    <li class="nav-item">
                      <router-link to="/libr_dash" class="nav-link">Home</router-link>
                    </li>
                    <li class="nav-item">
                      <router-link to="/requests" class="nav-link">Requests</router-link>
                    </li>
                    <li class="nav-item dropdown">
                      <a class="nav-link dropdown-toggle active" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        Manage Sections
                      </a>
                      <ul class="dropdown-menu dropdown-menu-dark">
                        <router-link to="/section_create" class="dropdown-item active">Create Section</router-link>
                        <router-link to="/section_edit" class="dropdown-item">Edit Section</router-link>
                        <router-link to="/section_delete" class="dropdown-item">Delete Section</router-link>
                      </ul>
                    </li>
                    <li class="nav-item dropdown">
                      <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        Manage Books
                      </a>
                      <ul class="dropdown-menu dropdown-menu-dark">
                        <router-link to="/book_create" class="dropdown-item">Create Book</router-link>
                        <router-link to="/book_edit" class="dropdown-item">Edit Book</router-link>
                        <router-link to="/book_delete" class="dropdown-item">Delete Book</router-link>
                      </ul>
                    </li>
                    <li class="nav-item">
                      <router-link to="/admin_summary" class="nav-link">Summary</router-link>
                    </li>
                  </ul>
                  <router-link to="/logout" class="btn btn-outline-danger">Logout</router-link>
                </div>
              </div>
            </div>
          </nav>
  
      <div class="mt-5 p-2 container toggle-hidden">
        <h1 id="heading" class="mt-5">Section Create</h1>
        <form class="shadow-lg p-3" @submit.prevent="handleSubmit">
          <div class="m-3">
            <label for="section_title" class="form-label">Section Title</label>
            <input type="text" class="form-control" id="section_title" v-model="formData.section_title">
          </div>
          <div class="m-3">
            <label for="section_description" class="form-label">Section Description</label>
            <input type="text" class="form-control" id="section_description" v-model="formData.section_description">
          </div>
          <button type="submit" class="m-3 btn btn-primary">Submit</button>
        </form>
      </div>
      <div v-if="error" class="text-danger mt-2">
        {{ error }}
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'section_create',
    data() {
      return {
        name: '', // Placeholder for user name
        formData: {
          section_title: '',
          section_description: ''
        },
        error:'',
      };
    },
    mounted() {
      // Add your logic to fetch user data (name) here
      this.name=localStorage.getItem("name")
      console.log("Fetching user data...");
    },
    methods: {
      async handleSubmit() {
        try {
          const token = localStorage.getItem('jwtToken');
          console.log(`token: ${token}`);
          const response = await fetch('http://localhost:8080/backend/section_create', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(this.formData)
          });

          const data=await response.json();
  
          if (response.ok) {
            // Handle success response here
            console.log('Section created successfully.');
            this.$router.push('/libr_dash');
            // Redirect or perform any other actions as needed
          } else {
            this.error=data.error;
            console.error('Failed to create section:', response.statusText);
          }
        } catch (error) {
          console.error('An error occurred while creating section:', error);
        }
      }
    }
  };
  </script>
  
  <style>
  /* Add your custom styles here */
  </style>
  