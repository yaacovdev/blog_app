import FormCard from "../components/FormCard.js";
import authMixin from "../mixins/authMixin.js";
const Login = {
    template: `
        <FormCard title="login">
            <form @submit="login">
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" v-model="username" class="form-control">
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" v-model="password" class="form-control">
                </div>
                <div class="d-flex justify-content-end">
                    <button type="submit" class="btn btn-dark mt-3">Login</button>
                </div>
            </form>
            <router-link to="/register" class="btn btn-link">Register</router-link>
        </FormCard>
    `,
    data() {
        return {
            username: "",
            password: "",
        };
    },
    components: {
        FormCard
    },
    mixins: [authMixin],
    methods: {
        login(event) {
            event.preventDefault();
            fetch("http://localhost:8000/api/token/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    username: this.username,
                    password: this.password,
                }),
            })
                .then((response) => response.json())
                .then(data => {
                    document.cookie = `token=${data.token};path=/;Secure`;
                    document.cookie = `username=${this.username};path=/;Secure`;
                    console.log('data.token:', data.token); // Log the cookies
                    console.log('Cookies set:', document.cookie); // Log the cookies
                    this.$root.$emit('authChanged', true);
                    this.$router.push('/');
                })
                .catch(error => {
                    console.error('Error:', error);
                    // Display an error message to the user
                });
        },
    },
};

export default Login;
