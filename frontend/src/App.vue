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
    async loadComments() {
      try {
        // Backend API aufrufen mit der Karten-Mittelposition
        const lat = this.center[0];
        const lng = this.center[1];
        const radius = this.searchRadius;
        
        const response = await fetch(
          `http://localhost:8000/comments/at?lat=${lat}&lng=${lng}&radius=${radius}`
        );
        
        if (response.ok) {
          this.comments = await response.json();
          console.log("Kommentare geladen:", this.comments);
        } else {
          console.error("Fehler beim Laden:", response.status);
        }
      } catch (error) {
        console.error("API-Fehler:", error);
      }
    },
    async search() {
      // Suche mit den eingegebenen Worten (für später)
      await this.loadComments();
    }
  },
  async mounted() {
    // Beim Start: Kommentare um Hamburg laden
    await this.loadComments();
  },
  data() {
    return {
      zoom: 16,
      center: [53.556090564417296, 10.021469080512393],
      comments: [],
      searchQuery: '',
      searchRadius: 2000  // 2 km Radius
    };
  },
};
</script>

<template>
  <div>
    <div style="margin-bottom: 10px;">
      <input type="text" v-model="searchQuery" placeholder="Suche...">
      <button @click="search">Suchen</button>
      <button @click="loadComments">Alle Kommentare laden</button>
    </div>
    <div style="height:600px; width:800px">
      <l-map ref="map" v-model:zoom="zoom" :center="center">
        <l-tile-layer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            layer-type="base"
            name="OpenStreetMap">
        </l-tile-layer>
        <!-- Kommentare als Marker auf der Karte -->
        <l-marker v-for="comment in comments" :key="comment.id" :lat-lng="[comment.lat, comment.lng]">
          <l-popup>
            <div>
              <strong>{{ comment.user }}</strong><br>
              <em>{{ comment.created_at }}</em><br>
              <p>{{ comment.text }}</p>
            </div>
          </l-popup>
        </l-marker>
      </l-map>
    </div>
  </div>
</template>

<style scoped>

</style>
