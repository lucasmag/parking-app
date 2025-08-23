import React, { useState, useEffect } from 'react';
import { View, Text, ScrollView, Alert, ActivityIndicator, TouchableOpacity } from 'react-native';
import { Feather } from '@expo/vector-icons';
import ParkingSpotCard from './ParkingSpotCard';
import { apiService } from '@/src/services/api';

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

interface ParkingCarouselProps {
  userLocation: {
    latitude: number;
    longitude: number;
  } | null;
  onSpotPress?: (spot: ParkingSpot) => void;
}

export const ParkingCarousel: React.FC<ParkingCarouselProps> = ({
  userLocation,
  onSpotPress
}) => {
  const [spots, setSpots] = useState<ParkingSpot[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchNearbySpots = async () => {
    if (!userLocation) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const data = await apiService.getNearbyParkingSpots(
        userLocation.latitude,
        userLocation.longitude,
        10, // 5km radius
        10  // limit to 10 spots
      );
      console.log(data)
      
      setSpots(data.results || []);
    } catch (err) {
      console.error('Error fetching nearby spots:', err);
      setError(err instanceof Error ? err.message : 'Erro ao carregar vagas próximas');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNearbySpots();
  }, [userLocation]);

  const handleSpotPress = (spot: ParkingSpot) => {
    if (onSpotPress) {
      onSpotPress(spot);
    } else {
      // Default action: show spot details
      Alert.alert(
        spot.title,
        `${spot.address}\n\nPreço: R$ ${spot.price_per_hour.toFixed(2)}/hora\nVagas disponíveis: ${spot.available_spots}`,
        [
          { text: 'Cancelar', style: 'cancel' },
          { text: 'Ver no mapa', onPress: () => console.log('Navigate to spot on map') },
        ]
      );
    }
  };

  const handleRetry = () => {
    fetchNearbySpots();
  };

  if (!userLocation) {
    return (
      <View className="bg-white mx-4 p-4 rounded-xl">
        <View className="flex-row items-center">
          <Feather name="map-pin" size={20} color="#6B7280" />
          <Text className="text-gray-600 ml-2">
            Ative a localização para ver vagas próximas
          </Text>
        </View>
      </View>
    );
  }

  if (loading && spots.length === 0) {
    return (
      <View className="bg-white mx-4 p-6 rounded-xl">
        <View className="flex-row items-center justify-center">
          <ActivityIndicator size="small" color="#3B82F6" />
          <Text className="text-gray-600 ml-2">Carregando vagas próximas...</Text>
        </View>
      </View>
    );
  }

  if (error) {
    return (
      <View className="bg-white mx-4 p-4 rounded-xl">
        <View className="flex-row items-center justify-between">
          <View className="flex-1">
            <View className="flex-row items-center mb-2">
              <Feather name="alert-circle" size={16} color="#EF4444" />
              <Text className="text-red-600 font-medium ml-1">Erro</Text>
            </View>
            <Text className="text-gray-600 text-sm">{error}</Text>
          </View>
          <TouchableOpacity
            onPress={handleRetry}
            className="bg-blue-500 px-3 py-2 rounded-lg ml-3"
          >
            <Text className="text-white text-sm font-medium">Tentar novamente</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }

  if (spots.length === 0) {
    return (
      <View className="bg-white mx-4 p-4 rounded-xl">
        <View className="flex-row items-center">
          <Feather name="search" size={20} color="#6B7280" />
          <Text className="text-gray-600 ml-2">
            Nenhuma vaga encontrada nas proximidades
          </Text>
        </View>
      </View>
    );
  }

  return (
    <View className="mb-4">
      {/* Header */}
      <View className="flex-row items-center justify-between px-4 mb-3">
        <View className="flex-row items-center">
          <Feather name="map-pin" size={20} color="#3B82F6" />
          <Text className="text-lg font-semibold text-gray-900 ml-2">
            Vagas próximas
          </Text>
        </View>
        <TouchableOpacity className="flex-row items-center">
          <Text className="text-blue-600 text-sm font-medium">Ver todas</Text>
          <Feather name="chevron-right" size={16} color="#3B82F6" />
        </TouchableOpacity>
      </View>

      {/* Carousel */}
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={{ paddingHorizontal: 8 }}
        snapToInterval={296} // Card width + margin
        snapToAlignment="start"
        decelerationRate="fast"
      >
        {spots.map((spot) => (
          <ParkingSpotCard
            key={spot.id}
            spot={spot}
            onPress={handleSpotPress}
          />
        ))}
        
        {/* Loading indicator for additional content */}
        {loading && (
          <View className="w-16 justify-center items-center">
            <ActivityIndicator size="small" color="#3B82F6" />
          </View>
        )}
      </ScrollView>

      {/* Footer */}
      <View className="flex-row items-center justify-center mt-3 px-4">
        <Text className="text-xs text-gray-500">
          {spots.length} vagas encontradas em um raio de 5km
        </Text>
      </View>
    </View>
  );
};

export default ParkingCarousel;