import { createApp } from 'vue'
import { router } from './router'; // 라우터 추가하고 
import App from './App.vue'
import store from './store';

// Create Vue Instance
const app = createApp(App);

app.use(router); // 사용 설정 하기
app.use(store);

app.mount('#app');