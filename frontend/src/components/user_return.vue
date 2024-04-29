<template>

</template>
<script>
export default {
    name: "user_return",
    mounted() {
        this.fetchData()
    },
    methods: {
        async fetchData() {
            try {
                const token = localStorage.getItem('jwtToken');
                const bookId = this.$route.params.book_id;
                const response = await fetch('http://192.168.1.9:8080/backend/user_return', {
                    method: 'PATCH',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        book_id: bookId,
                    }),
                });

                if (response.ok) {
                    console.log("book returned")
                    this.$router.push("/user_dash")
                } else {
                    console.error('Failed to fetch data:', response.statusText);
                }
            } catch (error) {
                console.error('An error occurred while fetching data:', error);
            }
        },
    }
}

</script>