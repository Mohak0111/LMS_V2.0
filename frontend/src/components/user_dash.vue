<template>
  <div class="mt-5 p-2 container toggle-hidden">
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
                  <h5 class="offcanvas-title" id="offcanvasDarkNavbarLabel">Hi, {{ adminname }}</h5>
                  <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas"
                      aria-label="Close"></button>
              </div>
              <div class="offcanvas-body">
                  <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
                      <li class="nav-item">
                          <router-link to="/user_dash" class="nav-link active">Home</router-link>
                      </li>
                      <li class="nav-item">
                          <router-link to="/user_requests" class="nav-link">My Requests</router-link>
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
    <h1 id="heading" class="mt-5">Welcome, {{ adminname }}</h1>
    <div v-if="sections.length > 0">
      <div v-for="section in sections" :key="section.section_title"
        class="container bg-dark mt-4 p-3 rounded-4 shadow border">
        <h1 class="text-light">{{ section.section_title }} <span class="fs-5 text-secondary">{{
      section.section_description }}</span></h1>
        <div v-if="section.section_books.length >= 1" :id="'carouselExampleCaptions' + section.section_title"
          class="carousel carousel-dark slide p-5">
          <div class="carousel-indicators">
            <button v-for="(book, index) in section.section_books" :key="index" type="button"
              :data-bs-target="'#carouselExampleCaptions' + section.section_title" :data-bs-slide-to="index"
              :class="{ 'active': index === 0 }" aria-current="true"></button>
          </div>
          <div class="carousel-inner">
            <div v-for="(book, index) in section.section_books" :key="index" class="carousel-item text-center"
              :class="{ 'active': index === 0 }">
              <h5 class="text-light">{{ book.book_name }}</h5>
              <p>Authors: <span>{{ book.book_authors }},</span></p>
              <router-link :to="{ name: 'user_request', params: { book_id: book.book_id } }" v-if="!book.book_issue_flag && user.user_num_requests < 5 && !isBookRequested(book.book_id)" class="btn btn-success">Request</router-link>
              <button v-else-if="book.book_issue_flag" class="btn btn-secondary disabled">Unavailable</button>
              <button v-else-if="user.user_num_requests >= 5" class="btn btn-secondary disabled">Max Req Limit
                Reached</button>
              <button v-else class="btn btn-secondary disabled">Already Requested</button>
            </div>
          </div>
          <button class="carousel-control-prev" type="button"
            :data-bs-target="'#carouselExampleCaptions' + section.section_title" data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
          </button>
          <button class="carousel-control-next" type="button"
            :data-bs-target="'#carouselExampleCaptions' + section.section_title" data-bs-slide="next">
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
</template>

<script>
export default {
  name: 'UserDash',
  props: {
    prop_adminname:String,
    prop_sections: Array,
    prop_user: {},
    prop_issue_flag: ""
  },
  mounted() {
    this.fetchData()
  },
  data() {
    return {
      adminname: this.prop_adminname,
      sections: this.prop_sections,
      user: this.prop_user,
      issue_flag: this.prop_issue_flag,
    }
  },
  methods: {
    async fetchData() {
      try {
        const token = localStorage.getItem('jwtToken');
        console.log(`token: ${token}`);
        const response = await fetch('http://localhost:8080/backend/user_dash', {
          method: 'GET', // Adjust the method as needed
          headers: {
            'Authorization': `Bearer ${token}`, // Include JWT token in the headers
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const data = await response.json();
          // Update the local data properties
          this.adminname = localStorage.getItem("name") // Adjust the property name if necessary
          this.sections = data.sections; // Adjust the property name if 
          this.issue_flag = data.issue_flag; // Adjust the property name if 
          this.user = data.user; // Adjust the property name if 
          console.log('Data received:', data); // Log the received data
        } else {
          console.error('Failed to fetch data:', response.statusText);
        }
      } catch (error) {
        console.error('An error occurred while fetching data:', error);
      }
    },
    isBookRequested(bookId) {
      return this.user.user_requests.some(request => (request.book_id === bookId && request.request_status==="pending"));
    },
    requestBook(section, book) {
      // Perform book request logic here
      console.log('Requesting book:', book.book_name, 'from section:', section.section_title);
    }
  }
};
</script>

<style scoped>
/* Add your component styles here */
</style>
