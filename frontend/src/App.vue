<script>
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import {LMap, LMarker, LPopup, LTileLayer, LPolyline} from "@vue-leaflet/vue-leaflet";

export default {
  components: {
    LPopup,
    LMarker,
    LMap,
    LTileLayer,
    LPolyline,
  },
  methods: {
    async loadComments() {
      try {
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
    async calculateRoutes() {
      try {
        const response = await fetch(
          `http://localhost:8000/routing/route?start_lat=${this.startLat}&start_lng=${this.startLng}&end_lat=${this.endLat}&end_lng=${this.endLng}`
        );
        
        if (response.ok) {
          this.routes = await response.json();
          console.log("Routen berechnet:", this.routes);
        } else {
          console.error("Fehler beim Laden der Routen:", response.status);
        }
      } catch (error) {
        console.error("API-Fehler:", error);
      }
    },
    onMapClick(event) {
      // Wenn bereits Routen berechnet wurden, nicht erlauben neue Punkte zu setzen
      if (this.routes.length > 0) {
        return;
      }
      
      // Beim Click auf die Karte: Koordinaten setzen
      if (!this.routePointsSet.start) {
        this.startLat = event.latlng.lat;
        this.startLng = event.latlng.lng;
        this.routePointsSet.start = true;
      } else if (!this.routePointsSet.end) {
        this.endLat = event.latlng.lat;
        this.endLng = event.latlng.lng;
        this.routePointsSet.end = true;
        // Sofort Routen berechnen wenn beide Punkte gesetzt
        this.calculateRoutes();
      }
    },
    selectRoute(route) {
      this.selectedRoute = route;
    },
    getRouteColor(routeId) {
      const colors = ['blue', 'purple', 'green'];
      return colors[routeId - 1] || 'blue';
    },
    getCommentIcon() {
      return L.divIcon({
        html: '<span style="font-size: 36px; line-height: 1;">📍</span>',
        iconSize: [36, 36],
        iconAnchor: [18, 36],
        popupAnchor: [0, -36],
        className: 'comment-icon'
      });
    },
    getEndIcon() {
      return L.divIcon({
        html: '<span style="font-size: 36px; line-height: 1;">🏴</span>',
        iconSize: [36, 36],
        iconAnchor: [18, 36],  // halbe Breite, volle Höhe → Spitze zeigt auf Punkt
        popupAnchor: [0, -36],
        className: 'end-icon'
      });
    }
  },
  async mounted() {
    await this.loadComments();
    // Beim Start mit Standard-Koordinaten Routen berechnen
    await this.calculateRoutes();
  },
  data() {
    return {
      zoom: 16,
      center: [53.556270, 10.021785],
      comments: [],
      routes: [],
      selectedRoute: null,
      searchRadius: 2000,
      // Routing-Punkte
      startLat: 53.556548,
      startLng: 10.022222,
      endLat: 53.554763,
      endLng: 10.020078,
      routePointsSet: {
        start: false,
        end: false
      }
    };
  },
};
</script>

<template>
  <div class="mobile-shell">
    <!-- Karte -->
    <div class="map-wrapper">
      <l-map 
        ref="map" 
        v-model:zoom="zoom" 
        :center="center"
        @click="onMapClick"
        style="border: 1px solid #ccc;"
      >
        <l-tile-layer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            layer-type="base"
            name="OpenStreetMap">
        </l-tile-layer>
        <!-- Suchleiste -->
        <div class="search-bar">
          <input type="text" placeholder="Suche" />
        </div>

        <!-- Kommentare als Marker -->
        <l-marker v-for="comment in comments" :key="'comment-' + comment.id" :lat-lng="[comment.lat, comment.lng]" :icon="getCommentIcon()">
          <l-popup>
            <div style="font-size: 12px;">
              <strong>{{ comment.user }}</strong><br>
              <em>{{ comment.created_at }}</em><br>
              <p style="margin: 5px 0;">{{ comment.text }}</p>
            </div>
          </l-popup>
        </l-marker>

        <!-- Routen als farbige Polylines -->
        <l-polyline 
          v-for="route in routes" 
          :key="'route-' + route.route_id"
          :lat-lngs="route.waypoints.map(wp => [wp.lat, wp.lng])"
          :color="getRouteColor(route.route_id)"
          :weight="selectedRoute?.route_id === route.route_id ? 5 : 3"
          :opacity="selectedRoute?.route_id === route.route_id ? 1 : 0.6"
          @click="selectRoute(route)"
          style="cursor: pointer;"
        >
          <l-popup>
            <strong>{{ route.name }}</strong><br>
            {{ route.distance_m }}m | {{ route.duration_min }}min | Schwierigkeit: {{ route.difficulty }}
          </l-popup>
        </l-polyline>


        <!-- Route Start/End Marker für alle Routen -->
        <l-marker v-for="route in routes" :key="'route-start-' + route.route_id" :lat-lng="[route.start.lat, route.start.lng]">
          <l-popup>⭐ START: {{ route.name }}</l-popup>
        </l-marker>

        <l-marker v-for="route in routes" :key="'route-end-' + route.route_id" :lat-lng="[route.end.lat, route.end.lng]" :icon="getEndIcon()">
          <l-popup>⭐ END: {{ route.name }}</l-popup>
        </l-marker>
      </l-map>
    </div>
  </div>
</template>

<style scoped>
.mobile-shell {
  width: 390px;
  height: 844px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-radius: 40px;
  box-shadow: 0 0 0 10px #222, 0 20px 60px rgba(0,0,0,0.5);
}

.map-wrapper {
  flex: 1;
  overflow: hidden;
}

.map-wrapper :deep(.leaflet-container) {
  height: 100%;
  width: 100%;
}

.map-wrapper :deep(.leaflet-top.leaflet-left) {
  top: auto;
  bottom: 10px;
  left: auto;
  right: 10px;
}
.search-bar {
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
  z-index: 1000;
}

.search-bar input {
  width: 80%;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}
</style>
