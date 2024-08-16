<template>
  <div class="container">
    <div>
      <h2>파일을 2번 업로드 해주세요.</h2>
      <h3>업로드된 파일 수: {{ uploadCount }}</h3>
      <h3>상단에 Secret Key를 기억해주세요!!</h3>
      <hr />
      <label>
        <input type="file" accept="application/json" @change="handleFileUpload($event)" />
      </label>
      <br />
      <button @click="submitFile" class="upload-button">
        <i class="fas fa-upload"></i> 업로드완료
      </button>
      <button @click="goToFinalRouter" class="final-router-button">
        next Step
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const backend_url = process.env.VUE_APP_BACKEND_URL;
let upload_url1 = `${backend_url}/upload_file`;

let key1 = 'Secret Key 1', key2 = 'Secret Key 2';

export default {
  data() {
    return {
      file: '',
      uploadCount: 0, // 업로드된 파일 수를 저장하는 변수
    };
  },
  methods: {
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
    submitFile() {
      let formData = new FormData();
      formData.append('file', this.file);
      axios
        .post(upload_url1, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Accept': 'application/json'
          }
        })
        .then(response => {
          console.log('SUCCESS!!');
          if (key1 == 'Secret Key 1') {
            key1 = response.data;
            alert(`비밀키는 ${key1}입니다.`);
          } else if (key2 == 'Secret Key 2') {
            key2 = response.data;
            alert(`비밀키는 ${key2}입니다.`);
          } else {
            alert('이미 파일을 2번 업로드 하셨습니다.');
          }
          this.uploadCount++; // 업로드 카운트 증가
          // window.location.href = '#/first';
        })
        .catch(function () {
          console.log('FAILURE!!');
          alert('파일 전송에 실패했습니다. 다시 시도해 주십시오.');
        });
    },
    goToFinalRouter() {
      window.location.href = `#/last?key1=${key1}&key2=${key2}`;
    }
  }
};
</script>

<style scoped>
.upload-button {
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
  margin-top: 20px;
}

.upload-button:hover {
  background-color: #1976D2;
}

.final-router-button {
  background-color: #45a049;
  color: #fff;
  border: none;
  padding: 10px 10px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 15px;
  font-weight: bold;
  text-transform: uppercase;
  transition: background-color 0.3s ease;
  margin-top: 20px;
  margin-left: 30px;
}

.final-router-button:hover {
  background-color: rgb(8, 90, 50);
}

.fa-upload {
  margin-right: 3px;
}
</style>
