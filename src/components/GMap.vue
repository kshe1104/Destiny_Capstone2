<template>
  <div style="width: 90%; height: 90%">
    <!-- <button @click="showMapMethod();">Show Map</button> -->
    <GoogleMap
    v-if="showMap"
    api-key=""
    :center="center"
    :zoom="19"
    style="width: 100%; height: 90%"
    >
      <Polyline :options="crossPath1" />
      <Polyline :options="crossPath2" />
      <Circle :options="circle" />
      <Marker :options="markerOptions" />
    </GoogleMap>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import { useStore } from 'vuex';
import { GoogleMap, Polyline, Circle, Marker } from "vue3-google-map";

// console.log(result);

export default defineComponent({
  components: { GoogleMap, Polyline, Circle, Marker },

  data()  {
    return {
      showMap: true,
    };
  },

  methods: {
    showMapMethod() {
      this.showMap = true;
    },
  },

  setup() {

    const store = useStore();
    let result = JSON.parse(JSON.stringify(store.state.data));
    
    // Refuse direct access to this page
    if (!result) {
      alert('교차점이 없습니다. 다시 시도해 주세요.');
      window.location.href = '#/last';
      location.reload();
    }
    
    // console.log(result);
    // console.log(JSON.parse(JSON.stringify(result)))
    // console.log(result.crossing_point[0]);
    
    let data = result[0].data1[0]
    // let data = result[1].data2[0]

    // console.log(result.data1[0])
    // result = result.data1[0];

    let center = data.crossing_point[0];
    // console.log(center);

    let route1 = data.route1;
    let route2 = data.route2;
    // console.log(route1);
    // console.log(route2);

    const circle = {
      center: center,
      radius: 20,
      strokeColor: "#FF00FF",
      strokeOpacity: 0.8,
      strokeWeight: 3,
      fillColor: "#FF00FF",
      fillOpacity: 0.1,
    };

    const customIcon = {
      url: require('../assets/map-icon-50px.png'),
      // size: { width: 46, height: 46, f: "px", b: "px" }, // 아이콘 크기
      // size: (20, 20),
      // origin: (0, 0), // 아이콘 원점
      // anchor: (25, 50), // 아이콘 기준점
    };

    const markerOptions = {
      position: center,
      // animation: "BOUNCE",
      title: "DESTINY",
      icon: customIcon,
    };

    const crossPath1 = {
      path: route1,
      geodesic: true,
      strokeColor: "#FF0000",
      strokeOpacity: 0.8,
      strokeWeight: 5,
    };
    const crossPath2 = {
      path: route2,
      geodesic: true,
      strokeColor: "#0000ff",
      strokeOpacity: 0.8,
      strokeWeight: 5,
    };
  return { center, crossPath1, crossPath2, circle, markerOptions };
  },
});
</script>