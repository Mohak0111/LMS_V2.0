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
                    <router-link to="/book_create" class="dropdown-item">Create Book</router-link>
                    <router-link to="/book_edit" class="dropdown-item">Edit Book</router-link>
                    <router-link to="/book_delete" class="dropdown-item active">Delete Book</router-link>
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
        <h1 id="heading" class="mt-5">Book Delete</h1>
        <div v-for="book in books" :key="book.book_id">
          <form @submit.prevent="handleSubmit(book.book_id)" class="shadow-lg p-3 m-3 rounded-3 border" :id="`${book.book_id}form`">
            <h1>{{ book.book_name }}</h1>
            <h1 class="fs-2 text-secondary">{{ book.book_authors }}</h1>
            <input type="text" hidden readonly :value="book.book_id" name="book_id">
            <h1>{{ book.section_title }}</h1>
            <button type="submit" class="m-3 btn btn-danger">Delete</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'book_delete',
    props: {
      props_adminname: String,
      props_books: Array,
    },
    data() {
      return {
        name: this.props_adminname || '',
        books: this.props_books || [],
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
          const response = await fetch('http://192.168.1.9:8080/backend/book_delete', {
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
            // Update book data
            this.books = data.books || [];
          } else {
            console.error('Failed to fetch book data:', response.statusText);
          }
        } catch (error) {
          console.error('An error occurred while fetching book data:', error);
        }
      },
      async handleSubmit(bookId) {
        try {
          const confirmed = confirm(`Are you sure you want to delete this book?`);
          if (!confirmed) return;
  
          const token = localStorage.getItem('jwtToken');
          const response = await fetch('http://192.168.1.9:8080/backend/book_delete', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              book_id: bookId,
            }),
          });
  
          if (response.ok) {
            console.log(`Book ${bookId} deleted successfully.`);
            // You may want to update the UI here to reflect the deletion
            this.$router.push("/libr_dash")
        } else {
            console.error('Failed to delete book:', response.statusText);
        }
    } catch (error) {
        console.error('An error occurred while deleting book:', error);
    }
},

    },
  };
  </script>
  
  <style>
  /* Add your custom styles here */
  </style>
  