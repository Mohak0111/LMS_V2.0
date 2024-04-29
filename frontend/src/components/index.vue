<template>
    <div class="bg-dark">
        <nav class="navbar bg-dark shadow">
            <div class="container-fluid">
                <a class="navbar-brand" href="/">Library</a>
            </div>
        </nav>



        <div class="row  text-center" style="margin-top: 10%; width: 60%; margin-left: 20%;">
            <div class="col-sm-6">
                <div class="shadow card">
                    <div class="card-body">
                        <h5 class="card-title mb-3 mt-3 p-1">Librarian Login</h5>
                        <router-link to="/libr_login" class="mb-2 btn btn-outline-primary btn-lg">Librarian</router-link>
                    </div>
                </div>
            </div>
            <div class="col-sm-6">
                <div class="shadow card">
                    <div class="card-body">
                        <h5 class="card-title mb-3 mt-3 p-1">User Login</h5>
                        <router-link to="/user_login" class="mb-2 btn btn-outline-primary btn-lg">User</router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'index'
}
</script>
