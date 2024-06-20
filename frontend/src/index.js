import NavBar from './components/NavBar.js';
import router from './router.js';


const App = {
    template: `
        <main>
            <nav-bar></nav-bar>
            <router-view :key="$route.fullPath"></router-view>
        </main>
    `,
    components: {
        NavBar,
    }
};



new Vue({
    el: '#app',
    router,
    data: {
        posts: []
    },
    mounted() {
        fetch('http://localhost:8000/api/posts/')
            .then(response => response.json())
            .then(data => {
                this.posts = data;
            });
    },
    render: h => h(App)
});

