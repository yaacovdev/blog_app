import authMixin from "../mixins/authMixin.js";

export default {
    template: `
    <nav>
    <div class="logo">
      <a href="#/" @click.prevent="$router.push('/')">Home</a>
      <a href="#/most-discuted" @click.prevent="$router.push('/most-commented')">Most Commented</a>
      <a  v-if="isLoggedIn" href="#/post/create" @click.prevent="$router.push('/posts/create')">Create</a>
    </div>
      <div class="auth-links" v-if="!isLoggedIn">
        <a href="#/login" @click.prevent="$router.push('/login')">Login</a>
        </div>
         <div class="auth-links"  v-else >
        <a href="#/login" @click.prevent="logout">Logout</a>
        </div>
    </nav>
    `,
    data() {
        return {
            isLoggedIn: false,
        };
    },
    mounted() {
        this.checkAuth();
    },
    created() {
        this.$root.$on("authChanged", (isLoggedIn) => {
            this.isLoggedIn = isLoggedIn;
        });
    },
    mixins: [authMixin],
    methods: {
        checkAuth() {
            this.isLoggedIn = this.getToken() ? true : false;   
        },
        logout() {
            
            this.deleteToken();
            this.deleteToken();
            if (this.$route.path !== '/') {
                this.$router.push('/');
            }
            this.$root.$emit('authChanged', false);
        },
    },
};
