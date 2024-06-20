import authMixin from "../mixins/authMixin.js";

export default {
    props: ["posts"],
    data() {
        return {
            post: null,
            newComment: {
                content: "",
            },
            editingComment: null,
            editedContent: '',
        };
    },
    template: `
    <div v-if="post" class="container mt-5">
    <button class="btn btn-secondary mt-4" @click="$router.push('/')">Back</button>
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-6">
            <div class="d-flex justify-content-end">
                <button v-if="isCommentAuthor(post)" @click="updatePost(post)" class="btn btn-sm m-1 btn-dark">Update</button>
                <button v-if="isCommentAuthor(post)" @click="deletePost(post.id)" class="btn btn-sm m-1 btn-danger">Delete</button>
                </div>
                <h3 class="mb-4 ">{{ post.title }}</h3>
            <div class="d-flex justify-content-end">

                <div class="mb-3"><strong>Author:</strong> <span class="text-uppercase">{{ post.author }}</span>
                <br>
                <strong>Created at:</strong> {{ post.created_at }}</div>
                </div>
                <div class="card">
                    <p class="card-body">{{ post.content }}</p>
                </div>
                <div class="container ps-5">
                <h5 class="mt-5 mb-4">Comments</h5>
                <ul class="list-unstyled">
                    <div v-for="comment in post.comments" :key="comment.id" class="mb-3" @click="toggleComment(comment)">
                        <div class="card">
                            <div class="mt-3 mb-3 container">
                                <p><strong>Author:</strong> {{ comment.author }}   
                                <strong>Created at:</strong>  {{ comment.created_at }}</p>
                                <div class="d-flex justify-content-end">
                                <button v-if="isCommentAuthor(comment)" @click="startEditingComment(comment)" class="btn m-1 btn-sm btn-dark">Update</button>
                                <button v-if="isCommentAuthor(comment)" @click="deleteComment(comment.id)" class="btn btn-sm m-1 btn-danger">Delete</button>
                                </div>
                                    <p v-if="editingComment !== comment.id">{{ comment.content }}</p>
                                    <textarea v-else v-model="editedContent" class="form-control"></textarea>
                                <div class="d-flex justify-content-end">
                                    <button v-if="editingComment === comment.id" @click="saveUpdateComment" class="btn mt-3 btn-sm btn-dark">Save</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </ul>
                <form @submit.prevent="addComment" class="mt-5">
                    <div class="card">
                    <div class="card-body">
                        <div class="form-group">
                            <label for="content">Add Comment</label>
                            <textarea id="content" v-model="newComment.content" class="form-control" rows="3" placeholder="..."></textarea>
                            </div>
                            <button type="submit" class="btn btn-dark mt-3">Submit</button>
                        </div>
                    </div>
                </form>
                </div>
            </div>
        </div>
    </div>
    `,
    mounted() {
        const postId = parseInt(this.$route.params.id);
        fetch(`http://localhost:8000/api/posts/${postId}/`)
            .then((response) => response.json())
            .then((data) => {
                this.post = data;
            });
    },
    mixins: [authMixin],
    methods: {
        isCommentAuthor(comment) {
            return comment.author === this.getUsername() && !this.editingComment;
        },
        updatePost(post) {
            this.$router.push({ path: `/post/${post.id}/update` });
        },
        startEditingComment(comment) {
            this.editingComment = comment.id;
            this.editedContent = comment.content;
        },
        toggleComment(comment) {
            console.log(comment.expanded);
            comment.expanded = !comment.expanded;
            this.post = { ...this.post };
        },
        addComment(event) {
            event.preventDefault();
            const postId = parseInt(this.$route.params.id);
            const token = this.getToken();
            fetch(`http://localhost:8000/api/posts/${postId}/comments/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Token ${token}`,
                },
                body: JSON.stringify(this.newComment),
            })
                .then((response) => response.json())
                .then((data) => {
                    this.post.comments.push(data);
                    this.newComment = {
                        content: "",
                    };
                });
        },
        saveUpdateComment(event){
            event.preventDefault();
            const comment = this.post.comments.find(comment => comment.id === this.editingComment);
            const token = this.getToken();
            fetch(`http://localhost:8000/api/comments/${this.editingComment}/`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Token ${token}`,
                },
                body: JSON.stringify({
                    content: this.editedContent,
                }),
            })
                .then((response) => response.json())
                .then((data) => {
                    comment.content = data.content;
                    this.editingComment = null;
                });
        },
        deleteComment(commentId) {
            const token = this.getToken();
            fetch(`http://localhost:8000/api/comments/${commentId}/`, {
                method: "DELETE",
                headers: {
                    "Authorization": `Token ${token}`,
                },
            })
                .then(() => {
                    this.post.comments = this.post.comments.filter(comment => comment.id !== commentId);
                });
        },
        deletePost(postId) {
            const token = this.getToken();
            fetch(`http://localhost:8000/api/posts/${postId}/`, {
                method: "DELETE",
                headers: {
                    "Authorization": `Token ${token}`,
                },
            })
                .then(() => {
                    this.$router.push('/');
                });
        }
    },
};
