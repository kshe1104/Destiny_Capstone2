<template>
  <div>
    <h1 style = "font-size:80px;"> Destiny </h1>
  </div><div>
    <label for="secretKey1" style="font-size: 25px;">Secret Key 1:</label>
    <input v-model="message" id="secretKey1" class="secret-key-input" placeholder="Secret Key 1" style="width: 200px; height: 30px; font-size: 25px;" />
  </div><div>
    <label for="secretKey2" style="font-size: 25px;">Secret Key 2:</label>
    <input v-model="message2" id="secretKey2" class="secret-key-input" placeholder="Secret Key 2" style="width: 200px; height: 30px; font-size: 25px;" />
  </div><div>
    <button @click="postData" class="check-button">확인해보기</button>
  </div>
</template>

<script>
import axios from 'axios';
import { useRoute } from 'vue-router';

const API_URL = process.env.VUE_APP_BACKEND_URL;
let RANDOM_TOKEN = 'analyze';

export default {
  name: 'Last-End',

  data() {
    const route = useRoute();

    const key1 = route.query.key1 ? route.query.key1 : '';
    const key2 = route.query.key2 ? route.query.key2 : '';

    return {
      message: key1,
      message2: key2,
    };
  },

  methods: {
    postData() {
      axios.post(`${API_URL}/${RANDOM_TOKEN}`, {
        key1: this.message,
        key2: this.message2,
        },
      {
        responseType: 'json',
        headers: {
								'Content-Type': 'application/json',
								// Fixed CORS error
								'Access-Control-Allow-Origin': '*',
								'Access-Control-Allow-Methods': '*',
								'Access-Control-Allow-Headers': ''
						}
          }
      )
        .then(response => {
          //console.log(response);
          let result = response.data
          // console.log(result);

          this.$store.commit('setData', result);
          this.$router.push({ name: 'GMap' });

          // Do something with the response data
          // window.location.href = `#/result?lat=${lat}&lng=${lng}`;
          
        })
        .catch(error => {
          console.error(error);
          alert('교차점이 없거나 잘못된 키입니다. 다시 시도해 주세요.');
          window.location.href = `#/last?key1=${this.message}&key2=${this.message2}`;
          location.reload();
        });
    }
  }
  
};
</script>
<style scoped>
.check-button {
  background-color: #2196F3;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
  text-transform: uppercase;
  transition: background-color 0.3s ease;
  margin-top: 10px;
  margin-left : 5px;
  align-items: center;
}

.check-button:hover {
  background-color: #1976D2;
}

.secret-key-input {
  margin-top: 10px;
  padding: 7px;
  font-size: 16px;
}

h1 {
  color: #333;
}

label {
  display: block;
  margin-top: 10px;
  font-weight: bold;
  color: #555;
}

</style>
