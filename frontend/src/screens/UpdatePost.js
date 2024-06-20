import FormCard from "../components/FormCard.js";
import authMixin from "../mixins/authMixin.js";

export default {
    template: `
    <FormCard title="Update the current post">
            <form @submit.prevent="updatePost">
                <div class="form-group mb-3">
                    <label for="title" class="form-label">Title</label>
                    <input type="text" id="title" v-model="title" class="form-control">
                </div>
                <div class="form-group mb-4">
                    <label for="content" class="form-label">Content</label>
                    <textarea id="content" v-model="content" class="form-control" rows="5"></textarea>
                </div>
                <div class="d-flex justify-content-end">
                    <button type="submit" class="btn btn-dark">Update Post</button>
                </div>
            </form>
        </FormCard>
    `,
    data() {
        return {
            title: "",
            content: "",
        };
    },
    components: {
        FormCard,
    },
    mounted() {
        const postId = parseInt(this.$route.params.id);
        fetch(`http://localhost:8000/api/posts/${postId}/`)
            .then((response) => response.json())
            .then((data) => {
                this.title = data.title;
                this.content = data.content;
            });
    },
    mixins: [authMixin],
    methods: {
        updatePost(event) {
            event.preventDefault();
            const postId = parseInt(this.$route.params.id);
            const token = this.getToken();
            fetch(`http://localhost:8000/api/posts/${postId}/`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Token ${token}`,
                },
                body: JSON.stringify({
                    title: this.title,
                    content: this.content,
                }),
            })
                .then((response) => response.json())
                .then((data) => {
                    this.$router.push("/");
                });
        },
    },
};


