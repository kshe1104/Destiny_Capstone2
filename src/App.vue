<template>
  <!--
    Replace own logo with Vue logo
  -->
  <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
  <!-- <HelloWorld msg="Welcome to Your Vue.js App"/>-->
  <router-view />
</template>

<script>
//import HelloWorld from './components/HelloWorld.vue'

// export default {
//   name: 'App',
//   components: {
//     //HelloWorld
//   }
// }
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: 0;
  padding: 0;
  background-image: url('./assets/back3.jpg');
  background-size: cover;
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-position: center center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  /* 화면 높이의 100%로 설정하여 화면 전체를 채움 */

}</style>
