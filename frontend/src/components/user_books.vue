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
              <h5 class="offcanvas-title" id="offcanvasDarkNavbarLabel">Hi, {{ username }}</h5>
              <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas" aria-label="Close"></button>
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
        <h1 id="heading" class="mt-5">My Books</h1>
        <table class="table table-hover table-dark table-bordered text-center rounded table-striped shadow-lg p-3 m-3 rounded">
          <thead class="fs-2">
            <tr>
              <th scope="col">Title</th>
              <th scope="col">Authors</th>
              <th scope="col">Section</th>
              <th scope="col" colspan="3">Options</th>
            </tr>
          </thead>
          <tbody class="table-group-divider">
            <tr v-for="book in books" :key="book.book_id">
              <td>{{ book.book_name }}</td>
              <td>{{ book.book_authors }}</td>
              <td>{{ book.section_title }}</td>
              <td><router-link :to="{ name: 'user_feedback', params: { book_id: book.book_id } }">Feedback</router-link></td>
              <td><router-link :to="{ name: 'user_return', params: { book_id: book.book_id } }">Return</router-link></td>
              <td><router-link :to="{ name: 'user_view', params: { book_id: book.book_id } }">View</router-link></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'user_books',
    data() {
      return {
        username:"",
        books: [],
      };
    },
    mounted() {
      this.fetchData();
    },
    methods: {
      async fetchData() {
        try {
            this.username=localStorage.getItem("name");
          const token = localStorage.getItem('jwtToken');
          const response = await fetch('http://localhost:8080/backend/user_books', {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          });
  
          if (response.ok) {
            const data = await response.json();
            this.books = data.books;
            console.log('Data received:', data);
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
  