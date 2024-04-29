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
              <h5 class="offcanvas-title" id="offcanvasDarkNavbarLabel">Hi, {{ name }}</h5>
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
                  <a class="nav-link dropdown-toggle active" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    Manage Books
                  </a>
                  <ul class="dropdown-menu dropdown-menu-dark">
                    <router-link to="/book_create" class="dropdown-item active">Create Book</router-link>
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
        <h1 id="heading" class="mt-5">Book Create</h1>
        <form @submit.prevent="handleSubmit" class="shadow-lg p-3 border rounded">
          <div class="m-3">
            <label for="book_name" class="form-label">Book Title</label>
            <input v-model="bookName" type="text" class="form-control" id="book_name" name="book_name">
          </div>
          <div class="m-3">
            <label for="book_content" class="form-label">Book content</label>
            <input v-model="bookContent" type="text" class="form-control" id="book_content" name="book_content">
          </div>
          <div class="m-3">
            <label for="book_authors" class="form-label">Book Authors (strictly separate by comma)</label>
            <input v-model="bookAuthors" type="text" name="book_authors" id="book_authors" class="form-control">
          </div>
          <div class="m-3">
            <h1>Select Section</h1>
            <div v-for="section in sections" :key="section.section_title">
              <label :for="section.section_title" class="form-label">{{ section.section_title }}</label>
              <input v-model="selectedSection" type="radio" class="form-check" :id="section.section_title" :name="section.section_title" :value="section.section_title">
            </div>
          </div>
  
          <button type="submit" class="m-3 btn btn-primary">Submit</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'book_create',
    props: {
      props_adminname: String,
      props_sections: Array,
    },
    data() {
      return {
        name: this.props_adminname || '',
        sections: this.props_sections || [],
        bookName: '',
        bookContent: '',
        bookAuthors: '',
        selectedSection: ''
      };
    },
    mounted() {
      this.fetchData();
    },
    methods: {
      async fetchData() {
        try {
          console.log("Fetching data...");
          const token = localStorage.getItem('jwtToken');
          const response = await fetch('http://localhost:8080/backend/book_create', {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            }
          });
  
          if (response.ok) {
            const data = await response.json();
            // Update user name if not provided as prop
            if (!this.props_adminname) {
              this.name = localStorage.getItem("name"); // Replace with actual user name
            }
            // Update section data
            this.sections = data.sections || [];
          } else {
            console.error('Failed to fetch section data:', response.statusText);
          }
        } catch (error) {
          console.error('An error occurred while fetching section data:', error);
        }
      },
      async handleSubmit() {
        try {
          const token = localStorage.getItem('jwtToken');
          const response = await fetch('http://localhost:8080/backend/book_create', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              book_name: this.bookName,
              book_content: this.bookContent,
              book_authors: this.bookAuthors,
              section: this.selectedSection
            }),
          });
  
          if (response.ok) {
            console.log('Book created successfully.');
            // You may want to update the UI here to reflect the book creation
            // Redirect or perform any other actions as needed
            this.$router.push("/libr_dash");
          } else {
            console.error('Failed to create book:', response.statusText);
          }
        } catch (error) {
          console.error('An error occurred while creating book:', error);
        }
      }
    },
  };
  </script>
  
  <style>
  /* Add your custom styles here */
  </style>
  