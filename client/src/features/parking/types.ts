export interface MapLocation {
  latitude: number;
  longitude: number;
  latitudeDelta: number;
  longitudeDelta: number;
}

export interface ParkingSpot {
  id: string;
  title: string;
  address: string;
  latitude: number;
  longitude: number;
  spot_type: string;
  pricePerHour: number;
  availableSpots: number;
  totalSpots: number;
  distance: number;
  features: string[];
  availability: string;
}