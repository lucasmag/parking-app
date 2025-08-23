import { useQuery, useMutation } from "@tanstack/react-query";
import { parkingApi, NearbySpotsParams, NearbySpotsResult } from "../api";

export function useNearbySpotsQuery(params?: NearbySpotsParams) {
  return useQuery<NearbySpotsResult>({
    queryKey: [params],
    queryFn: () => parkingApi.getNearbySpots(params as NearbySpotsParams),
    enabled: Boolean(params),
  })
}