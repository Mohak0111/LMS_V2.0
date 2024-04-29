<template>
    <div>
        <nav class="navbar navbar-dark bg-dark fixed-top shadow">
            <div class="container-fluid">
                <a class="navbar-brand" href="/">Library</a>
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
                                <a class="nav-link" href="/user_dash">Home</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="/user_requests">My Requests</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="/user_books">My Books</a>
                            </li>
                            <li class="nav-item">
                                <a class="my-3 btn btn-success" href="/user_search">search</a>
                            </li>
                        </ul>
                        <a href="/logout" class="btn btn-outline-danger mt-5">Logout</a>
                    </div>
                </div>
            </div>
        </nav>

        <div class="mt-5 p-2 container toggle-hidden">
            <h1 id="heading" class="mt-5">Search</h1>
            <form class="shadow-lg p-3 border rounded" @submit.prevent="submitSearch">
                <h1>Select the parameter to search on</h1>
                <div class="m-3">
                    <label for="book_name" class="form-label">Book Name</label>
                    <input type="radio" class="form-check" id="book_name" name="parameter" value="book_name">
                </div>
                <div class="m-3">
                    <label for="book_authors" class="form-label">Book Authors</label>
                    <input type="radio" class="form-check" id="book_authors" name="parameter" value="book_authors">
                </div>
                <div class="m-3">
                    <label for="book_availability" class="form-label">Book Availability</label>
                    <input type="radio" class="form-check" id="book_availability" name="parameter"
                        value="book_availability">
                </div>
                <div class="m-3">
                    <label for="section_title" class="form-label">Section Title</label>
                    <input type="radio" class="form-check" id="section_title" name="parameter" value="section_title">
                </div>
                <div class="m-3">
                    <label for="section_description" class="form-label">Section Description</label>
                    <input type="radio" class="form-check" id="section_description" name="parameter"
                        value="section_description">
                </div>
                <div class="m-3">
                    <label for="search_string" class="form-label">Enter The search string:</label>
                    <input type="text" class="form-control" id="search_string" name="search_string"
                        v-model="searchString">
                </div>

                <button type="submit" class="m-3 btn btn-primary">Submit</button>
            </form>
        </div>
        <h1 id="heading" class="mt-2 p-2 container">Results</h1>

        <div>
            <div id="section_display">
              <div v-if="results && content === 'section'" v-for="section in results" :key="section.section_title">
                <div class="container bg-dark mt-4 p-3 rounded-4 shadow border">
                  <h1 class="text-light">{{ section.section_title }} <span class="fs-5 text-secondary">{{ section.section_description }}</span></h1>
                  <div v-if="section.section_books.length >= 1" :id="'carouselExampleCaptions'+section.section_title" class="carousel carousel-dark slide p-5">
                    <div class="carousel-indicators">
                      <button type="button" :data-bs-target="'#carouselExampleCaptions' + section.section_title" data-bs-slide-to="0"
                        class="active" aria-current="true"></button>
                      <button v-for="i in section.section_books.length - 1" type="button" :data-bs-target="'#carouselExampleCaptions' + section.section_title"
                        :data-bs-slide-to="i"></button>
                    </div>
                    <div class="carousel-inner">
                      <div v-for="(book, index) in section.section_books" :key="index" class="carousel-item text-center" :class="{ active: index === 0 }">
                        <h5 class="text-light">{{ book.book_name }}</h5>
                        <p>Authors:
                          <span> {{ book.book_authors }},</span>
                        </p>
                      </div>
                    </div>
                    <button class="carousel-control-prev" type="button" :data-bs-target="'#carouselExampleCaptions' + section.section_title"
                      data-bs-slide="prev">
                      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                      <span class="visually-hidden">Previous</span>
                    </button>
                    <button class="carousel-control-next" type="button" :data-bs-target="'#carouselExampleCaptions' + section.section_title"
                      data-bs-slide="next">
                      <span class="carousel-control-next-icon" aria-hidden="true"></span>
                      <span class="visually-hidden">Next</span>
                    </button>
                  </div>
                  <p v-else class="container bg-dark text-center p-3">No books exist</p>
                </div>
              </div>
            </div>
            <div id="book_display">
              <div v-if="results && content === 'book'" class="mt-5 p-2 container toggle-hidden">
                <div v-for="book in results" :key="book.book_id" class="shadow-lg p-3 m-3 rounded-3 border" :id="book.book_id + 'div'">
                  <h1>{{ book.book_name }}</h1>
                  <h1 class="fs-2 text-secondary">{{ book.book_authors }}</h1>
                  <h1>{{ book.section_title }}</h1>
                </div>
              </div>
            </div>
          </div>
    </div>
</template>

<script>
export default {
    name:"user_search",
    props: {
        props_name: String,
        props_searchString: String,
        props_content: String,
        props_results: Array,
    },
    data() {
        return {
            name: localStorage.getItem("name"),
            searchString: this.props_searchString,
            content:this.props_content,
            results:this.props_results,
        };
    },
    methods: {
        async submitSearch() {
            try {
                const token = localStorage.getItem('jwtToken');
                const response = await fetch('http://192.168.1.9:8080/backend/user_search', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        parameter: this.getParameter(),
                        search_string: this.searchString || "none"
                    })
                });

                if (response.ok) {
                    const data = await response.json();
                    this.content=data.content
                    this.results = data.results || [];
                    console.log(this.results)
                } else {
                    console.error('Failed to fetch section data:', response.statusText);
                }
            } catch (error) {
                console.error('An error occurred while fetching section data:', error);
            }
        },
        getParameter() {
            // Get the selected parameter from the radio buttons
            const parameters = document.getElementsByName('parameter');
            for (let i = 0; i < parameters.length; i++) {
                if (parameters[i].checked) {
                    return parameters[i].value;
                }
            }
            return null; // Return null if no parameter is selected
        }
    }
};
</script>

<style scoped>
/* Add your component-specific styles here */
</style>