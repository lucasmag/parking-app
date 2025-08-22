// services/api.ts
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_CONFIG } from '@/src/config/api';


interface ParkingSpot {
  id: string;
  title: string;
  address: string;
  latitude: number;
  longitude: number;
  spot_type: string;
  price_per_hour: number;
  available_spots: number;
  total_spots: number;
  distance: number;
  features: string[];
  availability: string;
}

interface NearbyParkinSpotsResponse {
  count: number;
  results: ParkingSpot[];
}

class ApiService {
  private async getAuthToken(): Promise<string | null> {
    try {
      return await AsyncStorage.getItem('auth_token');
    } catch (error) {
      console.error('Error getting auth token:', error);
      return null;
    }
  }

  private async makeRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const token = await this.getAuthToken();

    const defaultHeaders = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
    };

    console.log(`${API_CONFIG.BASE_URL}${endpoint}`);
    console.log(options);

    const response = await fetch(`${API_CONFIG.BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
    }

    return response.json();
  }

  async getNearbyParkingSpots(
    lat: number,
    lng: number,
    radius: number = 5,
    limit: number = 10
  ): Promise<NearbyParkinSpotsResponse> {
    const params = new URLSearchParams({
      lat: lat.toString(),
      lng: lng.toString(),
      radius: radius.toString(),
      limit: limit.toString(),
    });

    return this.makeRequest<NearbyParkinSpotsResponse>(`/nearby/?${params}`);
  }

  async searchParkingSpots(
    lat: number,
    lng: number,
    startTime: string,
    endTime: string,
    radius: number = 10
  ): Promise<NearbyParkinSpotsResponse> {
    const params = new URLSearchParams({
      lat: lat.toString(),
      lng: lng.toString(),
      start_time: startTime,
      end_time: endTime,
      radius: radius.toString(),
    });

    return this.makeRequest<NearbyParkinSpotsResponse>(`/search/?${params}`);
  }

  async getParkingSpotDetails(spotId: string): Promise<ParkingSpot> {
    return this.makeRequest<ParkingSpot>(`/parking-spots/${spotId}/`);
  }

  async createBooking(bookingData: {
    spot: string;
    start_time: string;
    end_time: string;
    duration_hours: number;
    notes?: string;
  }) {
    return this.makeRequest('/bookings/', {
      method: 'POST',
      body: JSON.stringify(bookingData),
    });
  }
}

export const apiService = new ApiService();
export type { ParkingSpot, NearbyParkinSpotsResponse };