<script>
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import {LMap, LMarker, LPopup, LTileLayer, LPolyline} from "@vue-leaflet/vue-leaflet";
import ConfirmationPopup from './components/ConfirmationPopup.vue';
import CommentPopup from './components/CommentPopup.vue';
import { fetchComments, postComment, fetchRoutes } from './api.js';

export default {
  components: {
    LPopup,
    LMarker,
    LMap,
    LTileLayer,
    LPolyline,
    ConfirmationPopup,
    CommentPopup
  },
  methods: {
    async loadComments() {
      try {
        const lat = this.center[0];
        const lng = this.center[1];
        const radius = this.searchRadius;
        
      this.comments = await fetchComments(lat, lng, radius);

      } catch (error) {
        console.error("API-Fehler:", error);
      }
    },
    async calculateRoutes() {
      this.showConfirmationPopup = false; // Popup schließen
      try {
        this.routes = await fetchRoutes(1,this.startLat, this.startLng, this.endLat, this.endLng); // Für Prototypen nur hardgecodete 1 als user_id
        this.selectedRoute = this.routes[0] ?? null;
      } catch (error) {
        console.error("API-Fehler:", error);
        this.routes = [];
      }
    },
    onMapClick(event) {
      if (this.routes.length > 0) return;

        if (this.routingMode) {
          if (!this.routePointsSet.start) {
            this.startLat = event.latlng.lat;
            this.startLng = event.latlng.lng;
            this.routePointsSet.start = true;
          } else if (!this.routePointsSet.end) {
            this.endLat = event.latlng.lat;
            this.endLng = event.latlng.lng;
            this.routePointsSet.end = true;
            this.showConfirmationPopup = true;
          }
        } else {
          // temporärer Marker für Kommentare
          if (this.tempMarker) {
            this.cancelComment();
          } else {
            this.tempMarker = event.latlng;
            this.showCommentPopup = false;
          }
        }
    },
    setStart() {
      this.startLat = this.tempMarker.lat;
      this.startLng = this.tempMarker.lng;
      this.routePointsSet.start = true;
      this.routingMode = true;
      this.tempMarker = null;
    },
    resetRouting() {
      this.showConfirmationPopup = false;
      this.routePointsSet = { start: false, end: false };
      this.routes = [];
      this.selectedRoute = null;
      this.routingMode = false;
    },
    openCommentPopup() {
      this.showCommentPopup = true;
    },
    cancelComment() {
      this.tempMarker = null;
      this.showCommentPopup = false;
      this.commentText = '';
    },
    async saveComment() {
      try {
        await postComment(this.commentText,this.tempMarker.lat,this.tempMarker.lng,1); // Für Prototypen nur hardgecodete 1
      } catch (error) {
        console.error("API-Fehler:", error);
      }
      this.cancelComment();
      this.loadComments(); // Kommentare neu laden, damit der neue Kommentar angezeigt wird
    },
    selectRoute(route) {
      this.selectedRoute = route;
    },
    getRouteColor(score) {
      return `hsl(${score * 120}, 100%, 40%)`;
    },
    getCommentIcon() {
      return L.divIcon({
        html: '<span style="font-size: 36px; line-height: 1;">👁️‍🗨️</span>',
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
    },
    selectSuggestion(suggestion) {
      if (suggestion === 'Beispielroute') {
        this.startLat = 53.556548;
        this.startLng = 10.022222;
        this.endLat = 53.553207;
        this.endLng = 10.019386;
        this.calculateRoutes();
      }
      this.showSuggestions = false;
    },
    onMapMoveEnd(event){
      const mapCenter = event.target.getCenter();
      this.center = [mapCenter.lat, mapCenter.lng];
      this.loadComments();
    },
    formatDate(isoString) {
      const date = new Date(isoString);
      return date.toLocaleString('de-DE', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      }) + ' Uhr';
    }
  },
  async mounted() {
    await this.loadComments();
  },
  data() {
    return {
      zoom: 16,
      center: [53.556270, 10.021785],
      comments: [],
      routes: [],
      selectedRoute: null,
      searchRadius: 2000,
      showSuggestions: false,
      routingMode: false,
      tempMarker: null,
      commentText: '',
      showCommentPopup: false,
      showConfirmationPopup: false,
      startLat: null,
      startLng: null,
      endLat: null,
      endLng: null,
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
        @moveend="onMapMoveEnd"
        style="border: 1px solid #ccc;"
      >
        <l-tile-layer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            layer-type="base"
            name="OpenStreetMap">
        </l-tile-layer>

        <!-- Suchleiste -->
        <div class="search-bar">
          <input type="text" placeholder="Suche" @focus="showSuggestions = true" @blur="showSuggestions = false" />
          <button class="map-btn">🔊</button>
          <div class="suggestions" v-if="showSuggestions">
            <div class="suggestion-item" @mousedown.stop="selectSuggestion('Beispielroute')">
              Beispielroute
            </div>
          </div>
        </div>

        <!-- Standort-Button -->
        <div class="leaflet-top leaflet-right" style="pointer-events: auto;">
          <div class="leaflet-control">
            <button class="map-btn">🎯</button>
          </div>
        </div>

        <!-- Buttons unten links -->
        <div class="leaflet-bottom leaflet-left" style="pointer-events: auto;">
          <div class="leaflet-control">
            <button class="weather-btn">🌥️</button>
            <button class="map-btn">📝</button>
            <button class="map-btn">🏠</button>
          </div>
        </div>

        <!-- Kommentare als Marker -->
        <l-marker v-for="comment in comments" :key="'comment-' + comment.id" :lat-lng="[comment.lat, comment.lng]" :icon="getCommentIcon()">
          <l-popup>
            <div class="comment-popup-content">
              <strong>{{ comment.user }}</strong><br>
              <em>{{ formatDate(comment.created_at) }}</em><br>
              <p class="comment-popup-text">{{ comment.text }}</p>
            </div>
          </l-popup>
        </l-marker>

        <!-- Temporärer Marker -->
        <l-marker v-if="tempMarker" :lat-lng="tempMarker">
          <l-popup :options="{ autoClose: false, closeOnClick: false }">
            <div class="temp-popup-buttons">
              <button @click="openCommentPopup">Kommentar hinterlassen</button>
              <button @click="setStart">Route hier beginnen</button>
            </div>
          </l-popup>
        </l-marker>

        <!-- Routen als farbige Polylines -->
        <l-polyline 
          v-for="route in routes" 
          :key="'route-' + route.route_id"
          :lat-lngs="route.waypoints.map(wp => [wp.lat, wp.lng])"
          :color="getRouteColor(route.score)"
          :weight="selectedRoute?.route_id === route.route_id ? 5 : 3"
          :opacity="selectedRoute?.route_id === route.route_id ? 1 : 0.6"
          @click="selectRoute(route)"
          style="cursor: pointer;"
        >
          <l-popup>
            <strong>{{ route.name }}</strong><br>
            {{ route.distance_m }}m | {{ route.duration_min }}min | Score: {{ (route.score * 10).toFixed(1) }}
          </l-popup>
        </l-polyline>

        <!-- Startpunkt -->
        <l-marker v-if="routePointsSet.start && routes.length === 0" :lat-lng="[startLat, startLng]"><l-popup>Startpunkt</l-popup></l-marker>
        <!-- Endpunkt -->
        <l-marker v-if="routePointsSet.end && routes.length === 0" :lat-lng="[endLat, endLng]" :icon="getEndIcon()"><l-popup>Ziel</l-popup></l-marker>

        <!-- Route Start/End Marker für alle Routen -->
        <l-marker v-for="route in routes" :key="'route-start-' + route.route_id" :lat-lng="[route.start.lat, route.start.lng]"></l-marker>
        <l-marker v-for="route in routes" :key="'route-end-' + route.route_id" :lat-lng="[route.end.lat, route.end.lng]" :icon="getEndIcon()"></l-marker>
      </l-map>
    </div>
    <CommentPopup v-model="commentText" :visible="showCommentPopup" @save="saveComment" @cancel="cancelComment"/>
    <ConfirmationPopup :visible="showConfirmationPopup" @confirm="calculateRoutes" @cancel="resetRouting"/>
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
  position: relative;
}

@media (max-width: 430px) {
  .mobile-shell {
    width: 100%;
    height: 100dvh;
    border-radius: 0;
    box-shadow: none;
  }
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
.map-wrapper :deep(.leaflet-top.leaflet-right) {
  top: auto;
  bottom: 152px; /* über den Zoom-Buttons */
}
.map-wrapper :deep(.leaflet-control-zoom-in),
.map-wrapper :deep(.leaflet-control-zoom-out) {
  width: 65px !important;
  height: 65px !important;
  line-height: 65px !important;
  font-size: 28px !important;
}
.map-wrapper :deep(.leaflet-popup-pane) {
  z-index: 1100;
}
.search-bar {
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
  z-index: 1000;
  display: flex;
  gap: 8px;
}

.search-bar input {
  flex: 1;  /* nimmt den verbleibenden Platz ein, Button bestimmt seine eigene Größe */
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}

.suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  margin-top: 4px;
  overflow: hidden;
}

.suggestion-item {
  padding: 12px 16px;
  font-size: 14px;
  cursor: pointer;
}

.suggestion-item:hover {
  background: #f5f5f5;
}

.map-btn {
  width: 68px;
  height: 68px;
  background: white;
  border: 2px solid rgba(0,0,0,0.2);
  border-radius: 4px;
  font-size: 36px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 1px 5px rgba(0,0,0,0.2);
}

.weather-btn {
  width: 68px;
  height: 68px;
  background: transparent;
  border: none;
  font-size: 60px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  filter: drop-shadow(0 1px 3px rgba(0,0,0,0.4));
  margin-bottom: 12px;
}

.comment-popup-content{
  font-size: 12px;
}
.comment-popup-text {
  margin: 5px 0;
}
.temp-popup-buttons {
  display: flex;
  gap: 8px;
  margin-top: 10px;
  justify-content: flex-end;
}

.temp-popup-buttons button {
  padding: 4px 8px;
  border-radius: 3px;
  border: none;
  cursor: pointer;
  font-size: 12px;
  background: var(--color-primary);
  color: white;
}

.temp-popup-buttons button:last-child {
  background: var(--color-accent);
  color: white;
}
</style>
