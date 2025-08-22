import { useQuery, useMutation } from "@tanstack/react-query";
import { parkingApi, NearbySpotsParams } from "../api";
import { ParkingSpot } from "../types";

export function useNearbySpotsQuery(params?: NearbySpotsParams) {
  return useQuery<ParkingSpot[]>({
    queryKey: [params],
    queryFn: () => parkingApi.getNearbySpots(params as NearbySpotsParams),
    enabled: false,
  })
}