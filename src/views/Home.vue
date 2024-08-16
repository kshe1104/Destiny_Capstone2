<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div>
    <h1>운명적인 사랑을 시험해보세요.</h1>
    <button class="love-button" @click="goToFirstPage">Start</button>
    <p style="color: #2f00ff; font-weight:bolder ;">파일 업로드를 위한 튜토리얼>> <a href="https://wjs.biblio19.net/ko/information/tutorial" target="_blank" style="color: #ff0000;">여기를 클릭하세요!!</a></p>
  </div>
</template>

<script>
export default {
  methods: {
    goToFirstPage() {
      // 페이지 이동을 수행하는 JavaScript 코드
      window.location.href = '#/first';
    }
  }
};
</script>

<style>
.love-button {
  background-color: #2196F3;
  color: #fff;
  border: none;
  padding: 10px 30px;
  border-radius: 30px;
  cursor: pointer;
  font-size: 25px;
  font-weight: bold;
  text-transform: uppercase;
  transition: background-color 0.3s ease;
  margin-top: 20px;
}
a {
  color: #FFEB3B;
}

a:hover {
  color: #FFC107; 
}

.love-button:hover {
  background-color: #1976D2;
}
</style>