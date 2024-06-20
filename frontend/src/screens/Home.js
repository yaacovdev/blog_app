export default {
    template: `
        <div class="container my-5">
        <div class="d-flex justify-content-center">
        <div class="col-12 col-md-10 col-lg-8">
        <h2 class="mb-4">{{ title }}</h2>
        <ul class="list-unstyled">
            <li v-for="post in posts" :key="post.id" class="mb-4">
                <div class="card card-home">
                    <div class="card-body">
                        <h3 class="card-title">{{ post.title }}</h3>
                        <p class="card-text content-preview">{{ post.content }}</p>
                        <span class="text-primary read-more" @click="showDetail(post.id)">Read More</span>
                    </div>
                </div>
            </li>
        </ul>
    </div>
    </div>
    </div>
    `,
    data() {
        return {
            posts: [],
            title: "All Posts"
        };
    },
    mounted() {
        var url = "http://localhost:8000/api/posts/";
        if (this.$route.path === "/most-commented") {
            this .title = "Most Commented Posts";
            url = "http://localhost:8000/api/posts/most-commented";
        }
        fetch(url)
            .then((response) => response.json())
            .then((data) => {
                this.posts = data;
            });
    },
    methods: {
        showDetail(id) {
            if (this.$route.path !== `/post/${id}`) {
                this.$router.push({ path: `/post/${id}` });
            }
        },
    },
};
