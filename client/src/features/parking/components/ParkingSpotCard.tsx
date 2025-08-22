import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { Feather } from '@expo/vector-icons';

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

interface ParkingSpotCardProps {
  spot: ParkingSpot;
  onPress: (spot: ParkingSpot) => void;
}

const getSpotTypeIcon = (type: string) => {
  switch (type) {
    case 'garage':
      return 'home';
    case 'lot':
      return 'square';
    case 'street':
      return 'map-pin';
    case 'driveway':
      return 'car';
    default:
      return 'map-pin';
  }
};

const getSpotTypeLabel = (type: string) => {
  switch (type) {
    case 'garage':
      return 'Garagem';
    case 'lot':
      return 'Estacionamento';
    case 'street':
      return 'Rua';
    case 'driveway':
      return 'Garagem Privada';
    default:
      return 'Outro';
  }
};

const getAvailabilityLabel = (availability: string) => {
  switch (availability) {
    case 'weekdays_9_5':
      return 'Seg-Sex (9h-17h)';
    case 'weekends':
      return 'Fins de semana';
    case '24_7':
      return '24/7';
    case 'custom':
      return 'Horários personalizados';
    default:
      return availability;
  }
};

export const ParkingSpotCard: React.FC<ParkingSpotCardProps> = ({ spot, onPress }) => {
  const isAvailable = spot.available_spots > 0;

  return (
    <TouchableOpacity
      onPress={() => onPress(spot)}
      className="bg-white rounded-xl p-4 mx-2 shadow-sm border border-gray-100 w-72"
      style={{ elevation: 2 }}
    >
      {/* Header */}
      <View className="flex-row items-start justify-between mb-3">
        <View className="flex-1 mr-3">
          <Text className="text-lg font-semibold text-gray-900 mb-1" numberOfLines={1}>
            {spot.title}
          </Text>
          <Text className="text-sm text-gray-600" numberOfLines={2}>
            {spot.address}
          </Text>
        </View>
        <View className="flex-row items-center bg-blue-50 px-2 py-1 rounded-full">
          <Feather name="map-pin" size={12} color="#3B82F6" />
          <Text className="text-blue-600 text-xs font-medium ml-1">
            {spot.distance}km
          </Text>
        </View>
      </View>

      {/* Type and Availability */}
      <View className="flex-row items-center mb-3">
        <View className="flex-row items-center flex-1">
          <Feather name={getSpotTypeIcon(spot.spot_type)} size={14} color="#6B7280" />
          <Text className="text-sm text-gray-600 ml-1">
            {getSpotTypeLabel(spot.spot_type)}
          </Text>
        </View>
        <View className="flex-row items-center">
          <Feather name="clock" size={14} color="#6B7280" />
          <Text className="text-xs text-gray-600 ml-1" numberOfLines={1}>
            {getAvailabilityLabel(spot.availability)}
          </Text>
        </View>
      </View>

      {/* Price and Spots */}
      <View className="flex-row items-center justify-between">
        <View className="flex-row items-baseline">
          <Text className="text-xl font-bold text-green-600">
            R$ {spot.price_per_hour.toFixed(2)}
          </Text>
          <Text className="text-sm text-gray-500 ml-1">/hora</Text>
        </View>
        
        <View className="flex-row items-center">
          {isAvailable ? (
            <>
              <View className="w-2 h-2 bg-green-500 rounded-full mr-2" />
              <Text className="text-sm font-medium text-gray-900">
                {spot.available_spots} vagas
              </Text>
            </>
          ) : (
            <>
              <View className="w-2 h-2 bg-red-500 rounded-full mr-2" />
              <Text className="text-sm font-medium text-gray-500">
                Lotado
              </Text>
            </>
          )}
        </View>
      </View>

      {/* Features (if any) */}
      {spot.features && spot.features.length > 0 && (
        <View className="flex-row flex-wrap mt-3 pt-3 border-t border-gray-100">
          {spot.features.slice(0, 3).map((feature, index) => {
            let icon = 'info';
            let label = feature;
            
            if (feature === 'covered') {
              icon = 'umbrella';
              label = 'Coberto';
            } else if (feature === 'security') {
              icon = 'shield';
              label = 'Segurança';
            } else if (feature === 'ev_charging') {
              icon = 'zap';
              label = 'Carregador EV';
            }
            
            return (
              <View key={index} className="flex-row items-center bg-gray-50 px-2 py-1 rounded-full mr-2 mb-1">
                <Feather name={icon as any} size={10} color="#6B7280" />
                <Text className="text-xs text-gray-600 ml-1">{label}</Text>
              </View>
            );
          })}
          {spot.features.length > 3 && (
            <View className="flex-row items-center bg-gray-50 px-2 py-1 rounded-full">
              <Text className="text-xs text-gray-600">+{spot.features.length - 3}</Text>
            </View>
          )}
        </View>
      )}
    </TouchableOpacity>
  );
};

export default ParkingSpotCard;