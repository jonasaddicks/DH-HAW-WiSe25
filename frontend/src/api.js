export async function fetchComments(lat, lng, radius) {
    const response = await fetch(`api/comments/at?lat=${lat}&lng=${lng}&radius=${radius}`);
    if (!response.ok) console.error("Fehler beim Laden:", response.status);
    return response.json();
};

export async function postComment(text, lat, lng, user_id) {
    const response = await fetch(
            `api/comments/post`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                lat: lat,
                lng: lng,
                user_id: user_id
            })
            }
        );
    if (!response.ok) console.error("Fehler beim Speichern:", response.status);
};

export async function fetchRoutes(user_id,startLat, startLng, endLat, endLng) {
    const response = await fetch(
          `api/routing/route?user_id=${user_id}&start_lat=${startLat}&start_lng=${startLng}&end_lat=${endLat}&end_lng=${endLng}`
    );
    if (!response.ok) {
        console.error("Fehler beim Berechnen der Route:", response.status);
        return [];
    }
    const data = await response.json();
    // Flatten RoutingResponse[] ({ score, route: { ... } }) into the shape the template expects
    return data.map((item, index) => ({
        route_id: index + 1,
        name: `Route ${index + 1}`,
        score: item.score,
        distance_m: item.route.distance_m,
        duration_min: item.route.duration_min,
        start: item.route.start,
        end: item.route.end,
        waypoints: item.route.waypoints,
    }));
}