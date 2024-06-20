export default {
    methods: {
        getCookie(name) {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
            return null;
        },
        getToken() {
            return this.getCookie('token');
        },
        getUsername() {
            return this.getCookie('username');
        },
        isAuthenticated() {
            const token = this.getToken();
            return !!token; // Retourne true si un token est présent
        },
        deleteToken() {
            document.cookie = 'token=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;';
        }
    }
};
