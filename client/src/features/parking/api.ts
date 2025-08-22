import { apiClient, QueryParams } from "@/src/services/api";
import { ParkingSpot } from "./types";


export interface NearbySpotsParams extends QueryParams {
  latitude: number;
  longitude: number;
};

export const parkingApi = {
  getNearbySpots: (params: NearbySpotsParams): Promise<ParkingSpot[]> => apiClient.get('/nearby', params),
}
