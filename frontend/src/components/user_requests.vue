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
                  <router-link to="/user_requests" class="nav-link active">My Requests</router-link>
                </li>
                <li class="nav-item">
                  <router-link to="/user_books" class="nav-link">My Books</router-link>
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
        <h1 id="heading" class="mt-5">My Requests</h1>
        <table class="table table-hover table-dark table-bordered text-center rounded table-striped shadow-lg p-3 m-3 rounded">
          <thead class="fs-2">
            <tr>
              <th scope="col">Title</th>
              <th scope="col">Authors</th>
              <th scope="col">Section</th>
              <th scope="col">Status</th>
            </tr>
          </thead>
          <tbody class="table-group-divider">
            <tr v-for="request in requests" :key="request.request_id">
              <td>{{ getBookName(request.book_id) }}</td>
              <td>{{ getBookAuthors(request.book_id) }}</td>
              <td>{{ getSectionTitle(request.book_id) }}</td>
              <td>{{ request.request_status }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'user_requests',
    data() {
      return {
        username:'',
        requests: [],
        books: [],
      };
    },
    mounted() {
      this.fetchData();
    },
    methods: {
      async fetchData() {
        try {
          const token = localStorage.getItem('jwtToken');
          this.username=localStorage.getItem('name');
          const response = await fetch('http://localhost:8080/backend/user_requests', {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          });
  
          if (response.ok) {
            const data = await response.json();
            this.requests = data.requests;
            this.books = data.books;
            console.log('Data received:', data);
          } else {
            console.error('Failed to fetch data:', response.statusText);
          }
        } catch (error) {
          console.error('An error occurred while fetching data:', error);
        }
      },
      getBookName(bookId) {
        const book = this.books.find(b => b.book_id === bookId);
        return book ? book.book_name : '';
      },
      getBookAuthors(bookId) {
        const book = this.books.find(b => b.book_id === bookId);
        return book ? book.book_authors : '';
      },
      getSectionTitle(bookId) {
        const book = this.books.find(b => b.book_id === bookId);
        return book ? book.section_title : '';
      },
    },
  };
  </script>
  
  <style>
  /* Add your custom styles here */
  </style>
  