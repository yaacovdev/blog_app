import FormCard from "../components/FormCard.js";


const Login = {
    template: `
        <FormCard title="Register">
            <form @submit="register">
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" v-model="email" class="form-control">
                </div>
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" v-model="username" class="form-control">
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" v-model="password" class="form-control">
                </div>
                <div class="d-flex justify-content-end">
                <button type="submit" class="btn btn-dark mt-3">Register</button>
                </div>
            </form>
        </FormCard>
    `,
    data() {
        return {
            email: '',
            username: '',
            password: ''
        };
    },
    components: {
        FormCard
    },
    methods: {
        register(event) {
            event.preventDefault();
            fetch('http://localhost:8000/api/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: this.email,
                    username: this.username,
                    password: this.password
                })
            })
                .then(response => response.json())
                .then(data => {
                    document.cookie = `token=${data.token};path=/;Secure`;
                    document.cookie = `username=${this.username};path=/;Secure`;
                    this.$root.$emit('authChanged', true);
                    this.$router.push('/');
                })
                .catch(error => {
                    console.error('Error:', error);
                    // Display an error message to the user
                });
        }
    }  
};

export default Login;
