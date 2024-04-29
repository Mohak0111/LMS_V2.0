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
                  <h5 class="offcanvas-title" id="offcanvasDarkNavbarLabel">Hi, {{adminname}}</h5>
                  <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas" aria-label="Close"></button>
                </div>
                <div class="offcanvas-body">
                  <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
                    <li class="nav-item">
                      <router-link to="/libr_dash" class="nav-link active">Home</router-link>
                    </li>
                    <li class="nav-item">
                      <router-link to="/requests" class="nav-link">Requests</router-link>
                    </li>
                    <li class="nav-item dropdown">
                      <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        Manage Sections
                      </a>
                      <ul class="dropdown-menu dropdown-menu-dark">
                        <router-link to="/section_create" class="dropdown-item">Create Section</router-link>
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
        <h1 class="mt-5">Welcome, {{ adminname }}</h1>
        <div v-if="sections.length > 0">
          <div v-for="section in sections" :key="section.section_title" class="container bg-dark mt-4 p-3 rounded-4 shadow border">
            <h1 class="text-light">{{ section.section_title }} <span class="fs-5 text-secondary">{{ section.section_description }}</span></h1>
            <div v-if="section.section_books.length >= 1" :id="'carouselExampleCaptions' + section.section_title" class="carousel carousel-dark slide p-5">
              <div class="carousel-indicators">
                <button v-for="(book, index) in section.section_books" :key="index" type="button" :data-bs-target="'#carouselExampleCaptions' + section.section_title" :data-bs-slide-to="index" :class="{ 'active': index === 0 }" aria-current="true"></button>
              </div>
              <div class="carousel-inner">
                <div v-for="(book, index) in section.section_books" :key="index" class="carousel-item text-center" :class="{ 'active': index === 0 }">
                  <h5 class="text-light">{{ book.book_name }}</h5>
                  <p>Authors: <span>{{ book.book_authors }},</span></p>
                </div>
              </div>
              <button class="carousel-control-prev" type="button" :data-bs-target="'#carouselExampleCaptions' + section.section_title" data-bs-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Previous</span>
              </button>
              <button class="carousel-control-next" type="button" :data-bs-target="'#carouselExampleCaptions' + section.section_title" data-bs-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Next</span>
              </button>
            </div>
          </div>
        </div>
        <div v-else>
          <p class="text-secondary">No sections created!</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'libr_dash',
    props:{

        props_adminname: String,
        props_sections: Array,
    },
    data() {
      return {
        adminname: this.props_adminname, // Placeholder for admin name
        sections: this.props_sections, // Placeholder for sections
      };
    },
    mounted() {
      // Add your data fetching logic here (API call)
      const adminname=localStorage.getItem("name")
      this.adminname=adminname
      console.log("calling fetchData");
      this.fetchData(); // Call the fetchData method
    },
    methods: {
      async fetchData() {
        try {
            const token = localStorage.getItem('jwtToken');
            console.log(`token: ${token}`);
            const response = await fetch('http://localhost:8080/backend/libr_dash', {
            method: 'GET', // Adjust the method as needed
            headers: {
              'Authorization': `Bearer ${token}`, // Include JWT token in the headers
              'Content-Type': 'application/json',
            },
          });
  
          if (response.ok) {
            const data = await response.json();
            // Update the local data properties
            // this.adminname = data.name; // Adjust the property name if necessary
            this.sections = data.sections; // Adjust the property name if 
            console.log(this.adminname, this.sections)
            console.log('Data received:', data); // Log the received data
          } else {
            console.error('Failed to fetch data:', response.statusText);
          }
        } catch (error) {
          console.error('An error occurred while fetching data:', error);
        }
      },
    },
  };
  </script>
  
  
  <style>
  /* Add your custom styles here */
  </style>
  