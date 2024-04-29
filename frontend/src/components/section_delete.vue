<template>
    <div>
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
              <h5 class="offcanvas-title" id="offcanvasDarkNavbarLabel">Hi, {{ name }}</h5>
              <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas"
                      aria-label="Close"></button>
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
                  <a class="nav-link dropdown-toggle active" href="#" role="button" data-bs-toggle="dropdown"
                     aria-expanded="false">
                    Manage Sections
                  </a>
                  <ul class="dropdown-menu dropdown-menu-dark">
                    <router-link to="/section_create" class="dropdown-item">Create Section</router-link>
                    <router-link to="/section_edit" class="dropdown-item">Edit Section</router-link>
                    <router-link to="/section_delete" class="dropdown-item active">Delete Section</router-link>
                  </ul>
                </li>
                <li class="nav-item dropdown">
                  <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                     aria-expanded="false">
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
        <h1 id="heading" class="mt-5">Section Delete</h1>
        <div v-for="section in sections" :key="section.section_title">
          <form @submit.prevent="handleSubmit(section.section_title)"
                class="shadow-lg p-3 m-3 rounded-3 border" :id="`${section.section_title}form`">
            <h1>{{ section.section_title }}</h1>
            <h1 class="fs-2 text-secondary">{{ section.section_description }}</h1>
            <input type="text" hidden readonly :value="section.section_title" name="section_title">
            <div v-for="book in section_books[section.section_title]" :key="book.book_id">
              <h1>{{ book.book_name }}</h1>
            </div>
            <button type="submit" class="m-3 btn btn-danger">Delete</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'section_delete',
    props: {
      props_adminname: String,
      props_sections: Array,
    },
    data() {
      return {
        name: this.props_adminname || '',
        sections: this.props_sections || [],
        section_books: {},
      };
    },
    mounted(){
      this.fetchdata();
    },
    methods: {
        async fetchdata() {
        try {
          console.log("Fetching data...");
          const token = localStorage.getItem('jwtToken');
          const response = await fetch('http://192.168.1.9:8080/backend/section_delete', {
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
      async handleSubmit(sectionTitle) {
        try {
          const confirmed = confirm(`Are you sure you want to delete ${sectionTitle}?`);
          if (!confirmed) return;
  
          const token = localStorage.getItem('jwtToken');
          const response = await fetch('http://192.168.1.9:8080/backend/section_delete', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              section_title: sectionTitle,
            }),
          });
  
          if (response.ok) {
            console.log(`Section ${sectionTitle} deleted successfully.`);
            // You may want to update the UI here to reflect the deletion
            this.$router.push("/libr_dash");
          } else {
            console.error('Failed to delete section:', response.statusText);
          }
        } catch (error) {
          console.error('An error occurred while deleting section:', error);
        }
      }
    },
  };
  </script>
  
  <style>
  /* Add your custom styles here */
  </style>
  