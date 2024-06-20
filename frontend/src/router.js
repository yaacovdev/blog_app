import Home from './screens/Home.js';
import PostDetail from './components/PostDetail.js';
import CreatePost from './screens/CreatePost.js';
import UpdatePost from './screens/UpdatePost.js';
import Register from './screens/Register.js';
import Login from './screens/Login.js';

export default new VueRouter({
    routes: [
        { path: '/', component: Home },
        { path: '/most-commented', component: Home },
        { path: '/post/:id', component: PostDetail, props: true },
        { path: '/posts/create', component: CreatePost },
        { path: '/post/:id/update', component: UpdatePost },
        { path: '/login', component: Login },
        { path: '/register', component: Register}
        
    ]
});
