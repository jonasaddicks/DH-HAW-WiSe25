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
  <div>
    <!-- Info Panel -->
    <div style="margin-bottom: 10px; padding: 10px; background-color: #f5f5f5;">
      <h3>RheumaMap Routing Demo</h3>
      <p v-if="routes.length === 0 && !routePointsSet.start">👉 Klick auf die Karte um einen Startpunkt zu setzen</p>
      <p v-else-if="routes.length === 0 && !routePointsSet.end">👉 Klick auf die Karte um einen Endpunkt zu setzen</p>
      <p v-else-if="routes.length > 0">✅ Routen berechnet! Hovere über die Linien oder klick sie an.</p>
      
      <div v-if="routePointsSet.start && routePointsSet.end" style="margin-top: 10px; font-size: 12px;">
        Start: [{{ startLat.toFixed(4) }}, {{ startLng.toFixed(4) }}]<br>
        End: [{{ endLat.toFixed(4) }}, {{ endLng.toFixed(4) }}]
      </div>
    </div>

    <!-- Karte -->
    <div style="height:700px; width:100%; position: relative;">
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

    <!-- Route Info -->
    <div v-if="selectedRoute" style="margin-top: 10px; padding: 10px; background-color: #e8f4f8; border-left: 4px solid #2196F3;">
      <h4 style="margin-top: 0;">{{ selectedRoute.name }}</h4>
      <div style="font-size: 14px;">
        <strong>Distanz:</strong> {{ selectedRoute.distance_m }}m<br>
        <strong>Dauer:</strong> {{ selectedRoute.duration_min }} Minuten<br>
        <strong>Schwierigkeit:</strong> {{ selectedRoute.difficulty }}<br>
        <strong>Farbe:</strong> <span :style="{color: getRouteColor(selectedRoute.route_id), fontWeight: 'bold'}">●</span>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
