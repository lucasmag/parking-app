import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { Feather } from '@expo/vector-icons';
import Animated from 'react-native-reanimated';
import { ParkingSpot } from '../types';

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
  }1
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

export default function ParkingSpotCard({spot, onPress}: ParkingSpotCardProps) {
  const isAvailable = spot.availableSpots > 0;

  return (
    <Animated.View className="pr-2">
      <View className='bg-white rounded-3xl p-4 shadow-md border border-gray-100 w-full'>
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
            R$ {spot?.pricePerHour?.toFixed(2)}
          </Text>
          <Text className="text-sm text-gray-500 ml-1">/hora</Text>
        </View>
        
        <View className="flex-row items-center">
          {isAvailable ? (
            <>
              <View className="w-2 h-2 bg-green-500 rounded-full mr-2" />
              <Text className="text-sm font-medium text-gray-900">
                {spot.availableSpots} vagas
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
      </View>
    </Animated.View>
  );
} 