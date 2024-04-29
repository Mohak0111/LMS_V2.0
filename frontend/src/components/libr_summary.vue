<template>
  <div>
    <nav class="navbar navbar-dark bg-dark fixed-top shadow">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">Library</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasDarkNavbar"
          aria-controls="offcanvasDarkNavbar" aria-label="Toggle navigation">
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
                <a class="nav-link" href="/libr_dash">Home</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="/requests">Requests</a>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                  aria-expanded="false">
                  Manage Sections
                </a>
                <ul class="dropdown-menu dropdown-menu-dark">
                  <li><a class="dropdown-item" href="/section_create">Create Section</a></li>
                  <li><a class="dropdown-item" href="/section_edit">Edit Section</a></li>
                  <li><a class="dropdown-item" href="/section_delete">Delete Section</a></li>
                </ul>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                  aria-expanded="false">
                  Manage Books
                </a>
                <ul class="dropdown-menu dropdown-menu-dark">
                  <li><a class="dropdown-item" href="/book_create">Create Book</a></li>
                  <li><a class="dropdown-item" href="/book_edit">Edit Book</a></li>
                  <li><a class="dropdown-item" href="/book_delete">Delete Book</a></li>
                </ul>
              </li>
              <li class="nav-item">
                <a class="nav-link active" href="/admin_summary">Summary</a>
              </li>
            </ul>
            <a href="/logout" class="btn btn-outline-danger">Logout</a>
          </div>
        </div>
      </div>
    </nav>

    <div class="mt-5 p-2 container">
      <h1 class="mt-5">Section Wise Request Summary</h1>
      <div class="border">
        <img :src="graph" id="requestsChart" style="margin-left: 25%;">
      </div>
      <h1 class="mt-5 pt-5">Issued Books</h1>
      <table
        class="table table-hover table-dark table-bordered text-center rounded table-striped shadow-lg p-3 m-3 rounded">
        <thead class="fs-2">
          <tr>
            <th scope="col">Book name</th>
            <th scope="col">User</th>
            <th scope="col">Number of days</th>
          </tr>
        </thead>
        <tbody class="table-group-divider">
          <tr v-for="book in books" :key="book.book_id">
            <template v-if="book.book_issue_flag">
              <td>{{ book.book_name }}</td>
              <template v-for="request in book.book_requests">
                <template v-if="request.request_status === 'issued'">
                  <td>{{ request.user_email }}</td>
                  <td>{{ request.request_num_days }}</td>
                </template>
              </template>
            </template>
          </tr>
        </tbody>
      </table>

    </div>
  </div>
</template>

<script>
//   import { Chart } from 'vue-chartjs';

export default {
  name: 'book_delete',
  mounted() {
    this.fetchData();
    this.getgraph()
  },
  data() {
    return {
      books: [],
      section_titles: [],
      numRequests: 0,
      name: '',
      graph: null
    };
  },
  methods: {
    async fetchData() {
      try {
        this.name = localStorage.getItem("name")
        console.log("Fetching data...");
        const token = localStorage.getItem('jwtToken');
        const response = await fetch('http://192.168.1.9:8080/backend/admin_summary', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          }
        });

        if (response.ok) {
          const data = await response.json();
          // Update issuedBooks, sectionTitles, and numRequests data
          this.books = data.books || [];
          this.requests = data.requests || [];
          // this.renderChart();
        } else {
          console.error('Failed to fetch admin summary data:', response.statusText);
        }
      } catch (error) {
        console.error('An error occurred while fetching admin summary data:', error);
      }
    },
    async getgraph() {
      try {
        this.name = localStorage.getItem("name")
        console.log("Fetching data...");
        const token = localStorage.getItem('jwtToken');
        const response = await fetch('http://192.168.1.9:8080/backend/graph', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        });

        if (response.ok) {
          const blob = await response.blob(); // Convert response to blob
          const url = URL.createObjectURL(blob); // Create URL for the blob
          this.graph = url;
          // this.renderChart();
        } else {
          console.error('Failed to fetch graph:', response.statusText);
        }
      } catch (error) {
        console.error('An error occurred while fetching graph:', error);
      }
    }


    // renderChart() {
    //   const ctx = document.getElementById('requestsChart').getContext('2d');
    //   new Chart(ctx, {
    //     type: 'bar',
    //     data: {
    //       labels: this.sectionTitles,
    //       datasets: [{
    //         label: 'Number of Requests',
    //         data: this.numRequests,
    //         backgroundColor: 'rgba(255, 99, 132, 0.2)',
    //         borderColor: 'rgba(255, 99, 132, 1)',
    //         borderWidth: 1
    //       }]
    //     },
    //     options: {
    //       scales: {
    //         yAxes: [{
    //           ticks: {
    //             beginAtZero: true
    //           }
    //         }]
    //       }
    //     }
    //   });
    // }
  }
};
</script>

<style scoped>
/* Add your component's style here */
</style>