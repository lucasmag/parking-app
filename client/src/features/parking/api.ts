import { apiClient, QueryParams } from "@/src/services/api";
import { ParkingSpot } from "./types";


export interface NearbySpotsParams extends QueryParams {
  latitude: number;
  longitude: number;
};

export interface NearbySpotsResult {
  spots: ParkingSpot[];
}

export const parkingApi = {
  getNearbySpots: (params: NearbySpotsParams): Promise<NearbySpotsResult> =>
    apiClient.get('nearby/', params),
}
