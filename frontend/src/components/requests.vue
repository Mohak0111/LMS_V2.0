<template>
    <div>
      <nav class="navbar navbar-dark bg-dark fixed-top shadow">
        <div class="container-fluid">
          <router-link to="/" class="navbar-brand">Library</router-link>
          <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas"
            data-bs-target="#offcanvasDarkNavbar" aria-controls="offcanvasDarkNavbar" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="offcanvas offcanvas-end text-bg-dark" tabindex="-1" id="offcanvasDarkNavbar"
            aria-labelledby="offcanvasDarkNavbarLabel">
            <div class="offcanvas-header">
              <h5 class="offcanvas-title" id="offcanvasDarkNavbarLabel">Hi, {{adminname}}</h5>
              <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas"
                aria-label="Close"></button>
            </div>
            <div class="offcanvas-body">
              <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
                <li class="nav-item">
                  <router-link to="/libr_dash" class="nav-link">Home</router-link>
                </li>
                <li class="nav-item">
                  <router-link to="/requests" class="nav-link active">Requests</router-link>
                </li>
                <li class="nav-item dropdown">
                  <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                    aria-expanded="false">
                    Manage Sections
                  </a>
                  <ul class="dropdown-menu dropdown-menu-dark">
                    <router-link to="/section_create" class="dropdown-item">Create Section</router-link>
                    <router-link to="/section_edit" class="dropdown-item">Edit Section</router-link>
                    <router-link to="/section_delete" class="dropdown-item">Delete Section</router-link>
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
        <h1 class="mt-5">Pending Requests</h1>
        <table class="table table-hover table-dark table-bordered text-center rounded table-striped shadow-lg p-3 m-3 rounded">
          <thead class="fs-2">
            <tr>
              <th scope="col">User</th>
              <th scope="col">Book name</th>
              <th scope="col">Number of days</th>
              <th scope="col" colspan="2">Options</th>
            </tr>
          </thead>
          <tbody class="table-group-divider">
            <tr v-for="request in requests" :key="request.id">
              <template v-if="request.request_status === 'pending'">
                <td>{{ request.user_email }}</td>
                <td v-for="book in books" v-if="book.book_id === request.book_id">
                  {{ book.book_name }}
                </td>
                <td>{{ request.request_num_days }}</td>
                <td>
                  <a class="btn btn-success" @click="grantRequest(user_email=request.user_email, book_id=request.book_id)">Grant</a>
                </td>
                <td>
                  <a class="btn btn-danger" @click="rejectRequest(user_email=request.user_email, book_id=request.book_id)">Reject</a>
                </td>
              </template>
            </tr>
          </tbody>
        </table>
      </div>
  
      <div class="mt-5 p-2 container toggle-hidden">
        <h1 class="mt-5">Approved Requests</h1>
        <table class="table table-hover table-dark table-bordered text-center rounded table-striped shadow-lg p-3 m-3 rounded">
          <thead class="fs-2">
            <tr>
              <th scope="col">User</th>
              <th scope="col">Book name</th>
              <th scope="col">Number of days</th>
              <th scope="col">Options</th>
            </tr>
          </thead>
          <tbody class="table-group-divider">
            <tr v-for="request in requests" :key="request.id">
              <template v-if="request.request_status === 'issued'">
                <td>{{ request.user_email }}</td>
                <td v-for="book in books" v-if="book.book_id === request.book_id">
                  {{ book.book_name }}
                </td>
                <td>{{ request.request_num_days }}</td>
                <td>
                  <a class="btn btn-danger" @click="revokeRequest(user_email=request.user_email, book_id=request.book_id)">Revoke</a>
                </td>
              </template>
            </tr>
          </tbody>
          
        </table>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Requests',
    props: {
        propsadminname:String,
      propsrequests: Array,
      propsbooks: Array,
    },
    data() {
      return {
        adminname: this.propsadminname,
        requests: this.propsrequests,
        books: this.propsbooks,
      };
    },
    mounted() {
      console.log("calling fetchData");
      this.adminname=localStorage.getItem("name")
      this.fetchData();
    },
    methods: {
      async fetchData() {
        try {
          const token = localStorage.getItem('jwtToken');
          console.log(`token: ${token}`);
          const response = await fetch('http://192.168.1.9:8080/backend/requests', {
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
            console.log(this.requests, this.books);
            console.log('Data received:', data);
          } else {
            console.error('Failed to fetch data:', response.statusText);
          }
        } catch (error) {
          console.error('An error occurred while fetching data:', error);
        }
      },
      async grantRequest(user_email, book_id) {
        // Logic to handle granting a request
        try {
          const token = localStorage.getItem('jwtToken');
          console.log(`token: ${token}`);
          const response = await fetch('http://192.168.1.9:8080/backend/grant', {
            method: 'PATCH',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              user_email: user_email,
              book_id: book_id,
            }),
          });
  
          if (response.ok) {
            console.log("granted")
            location.reload()
          } else {
            console.error('Failed to fetch data:', response.statusText);
          }
        } catch (error) {
          console.error('An error occurred while fetching data:', error);
        }

      },
      async rejectRequest(user_email, book_id) {
        // Logic to handle rejecting a request
        try {
          const token = localStorage.getItem('jwtToken');
          console.log(`token: ${token}`);
          const response = await fetch('http://192.168.1.9:8080/backend/reject', {
            method: 'PATCH',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              user_email: user_email,
              book_id: book_id,
            }),
          });
  
          if (response.ok) {
            console.log("rejected")
            location.reload()
          } else {
            console.error('Failed to fetch data:', response.statusText);
          }
        } catch (error) {
          console.error('An error occurred while fetching data:', error);
        }
      },
      async revokeRequest(user_email, book_id) {
        // Logic to handle revoking a request
        try {
          const token = localStorage.getItem('jwtToken');
          console.log(`token: ${token}`);
          const response = await fetch('http://192.168.1.9:8080/backend/revoke', {
            method: 'PATCH',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              user_email: user_email,
              book_id: book_id,
            }),
          });
  
          if (response.ok) {
            console.log("revoked")
            location.reload()
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
  