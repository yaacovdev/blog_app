import FormCard from "../components/FormCard.js";
import authMixin from "../mixins/authMixin.js";


const CreatePost = {
    template: `
        <FormCard title="Create a new post">
            <form @submit.prevent="createPost">
                <div class="form-group mb-3">
                    <label for="title" class="form-label">Title</label>
                    <input type="text" id="title" v-model="title" class="form-control">
                </div>
                <div class="form-group mb-4">
                    <label for="content" class="form-label">Content</label>
                    <textarea id="content" v-model="content" class="form-control" rows="5"></textarea>
                </div>
                <div class="d-flex justify-content-end">
                    <button type="submit" class="btn btn-dark">Create Post</button>
                </div>
            </form>
        </FormCard>
    `,
    data() {
        return {
            title: '',
            content: '',
        }
    },
    components: {
        FormCard
    },
    mixins: [authMixin],
    methods: {
        createPost() {
            const token = this.getToken();
            if (!token) {
                console.error('No token found, please log in.');
                return;
            }
            fetch('http://localhost:8000/api/posts/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                },
                body: JSON.stringify({
                    title: this.title,
                    content: this.content
                })
            })
                .then(response => response.json())
                .then(data => {
                    this.$router.push('/');
                });
        }
    }
};

export default CreatePost;