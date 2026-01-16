<script>
import "leaflet/dist/leaflet.css";
import {LMap, LMarker, LPopup, LTileLayer} from "@vue-leaflet/vue-leaflet";

export default {
  components: {
    LPopup,
    LMarker,
    LMap,
    LTileLayer,
  },
  methods: {
    async search() {
      const response = await fetch('http://localhost:3000/', {
        method: "POST",
        body: JSON.stringify({
          "search": this.searchQuery
        })
      })
      if (response.ok) {
        console.log(await response.json())
      } else {
        console.log("Failure when posting search query: " + response.status)
      }
    }
  },
  async mounted() {
    const response = await fetch('http://localhost:3000/markers')
    this.markers = await response.json()
    this.markers.forEach(value => {
      console.log(value.lat)
    })
  },
  data() {
    return {
      zoom: 16,
      markers: [],
      searchQuery: ''
    };
  },
};
</script>

<template>
  <input type="text" v-model="searchQuery" placeholder="Suche...">
  <button @click="search">Suchen</button>
  <div style="height:600px; width:800px">
    <l-map ref="map" v-model:zoom="zoom" :center="[53.556090564417296, 10.021469080512393]">
      <l-tile-layer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          layer-type="base"
          name="OpenStreetMap">
      </l-tile-layer>
      <l-marker v-for="marker in markers" :lat-lng="[marker.lat, marker.lon]">
        <l-popup> {{ marker.desc }} </l-popup>
      </l-marker>
    </l-map>
  </div>
</template>

<style scoped>

</style>
