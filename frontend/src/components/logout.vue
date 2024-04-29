<template>

</template>
<script>
export default {
    name: 'logout',
    mounted() {
        this.logout()
    },
    methods: {
        async logout() {
            localStorage.clear();
            this.$router.push('/')
        }
    }
}

</script>