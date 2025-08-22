export const API_CONFIG = {
  BASE_URL: process.env.EXPO_BASE_URL || 'http://localhost:8000/api',

  ENDPOINTS: {
    NEARBY_SPOTS: '/nearby/',
    SEARCH_SPOTS: '/search/',
    PARKING_SPOTS: '/parking-spots/',
    BOOKINGS: '/bookings/',
    DASHBOARD: '/dashboard/',
  },
  
  DEFAULT_PARAMS: {
    NEARBY_RADIUS: 5,
    SEARCH_RADIUS: 10,
    SPOTS_LIMIT: 10,
  }
};

export default API_CONFIG;
