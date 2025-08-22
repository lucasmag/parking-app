import React, { useState, useEffect, useRef } from 'react';
import { Header } from '@/src/components/layout/Header';
import TypeaheadExample from '@/src/components/ui/Typeahead';
import ParkingCarousel from '@/src/features/parking/components/ParkingSpotCarousel';
import { View, Text, StyleSheet, Alert, TouchableOpacity, ScrollView } from 'react-native';
import MapView, { PROVIDER_GOOGLE } from 'react-native-maps';
import * as Location from 'expo-location';
import { Feather } from '@expo/vector-icons';
import { Typography } from '@/src/components/ui/Typography';

interface LocationState {
  latitude: number;
  longitude: number;
  latitudeDelta: number;
  longitudeDelta: number;
}

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

const DEFAULT_LOCATION: LocationState = {
  latitude: -7.2137, // Juazeiro do Norte, Ceará coordinates as fallback
  longitude: -39.3157,
  latitudeDelta: 0.01,
  longitudeDelta: 0.01,
};

export default function HomeScreen() {
  const [location, setLocation] = useState<LocationState | null>(null);
  const [locationPermission, setLocationPermission] = useState<Location.PermissionStatus | null>(null);
  const [isLoadingLocation, setIsLoadingLocation] = useState(false);
  const [locationError, setLocationError] = useState<string | null>(null);
  const [showPermissionDeniedMessage, setShowPermissionDeniedMessage] = useState(false);

  const mapRef = useRef<MapView>(null);

  // Request location permission and get current location
  const requestLocationPermission = async () => {
    try {
      setIsLoadingLocation(true);
      setLocationError(null);
      setShowPermissionDeniedMessage(false);

      // Request permission
      const { status } = await Location.requestForegroundPermissionsAsync();
      setLocationPermission(status);

      if (status === 'granted') {
        // Get current location
        const currentLocation = await Location.getCurrentPositionAsync({
          accuracy: Location.Accuracy.Balanced,
          timeInterval: 10000,
          distanceInterval: 100,
        });

        const newLocation: LocationState = {
          latitude: currentLocation.coords.latitude,
          longitude: currentLocation.coords.longitude,
          latitudeDelta: 0.01,
          longitudeDelta: 0.01,
        };

        setLocation(newLocation);

        // Animate map to current location
        if (mapRef.current) {
          mapRef.current.animateToRegion(newLocation, 1000);
        }

      } else {
        // Permission denied
        setShowPermissionDeniedMessage(true);
        setLocation(DEFAULT_LOCATION); // Use default location

        // Show alert explaining why location is needed
        Alert.alert(
          'Localização Negada',
          'Para uma melhor experiência, permita o acesso à sua localização para encontrar vagas de estacionamento próximas. Você pode alterar isso nas configurações do app.',
          [
            {
              text: 'Usar Localização Padrão',
              style: 'cancel',
              onPress: () => {
                if (mapRef.current) {
                  mapRef.current.animateToRegion(DEFAULT_LOCATION, 1000);
                }
              }
            },
            {
              text: 'Tentar Novamente',
              onPress: () => requestLocationPermission()
            }
          ]
        );
      }
    } catch (error) {
      console.error('Error requesting location permission:', error);
      setLocationError('Erro ao obter localização. Usando localização padrão.');
      setLocation(DEFAULT_LOCATION);

      if (mapRef.current) {
        mapRef.current.animateToRegion(DEFAULT_LOCATION, 1000);
      }
    } finally {
      setIsLoadingLocation(false);
    }
  };

  // Check permission status on component mount
  useEffect(() => {
    const checkInitialPermission = async () => {
      const { status } = await Location.getForegroundPermissionsAsync();
      setLocationPermission(status);

      if (status === 'granted') {
        // If already granted, get location immediately
        requestLocationPermission();
      } else {
        // Set default location but don't show permission denied message yet
        setLocation(DEFAULT_LOCATION);
      }
    };

    checkInitialPermission();
  }, []);

  // Handle current location button press
  const handleCurrentLocationPress = () => {
    if (locationPermission === 'granted' && location) {
      // Already have permission and location, just animate to it
      if (mapRef.current) {
        mapRef.current.animateToRegion(location, 1000);
      }
    } else {
      // Need to request permission
      requestLocationPermission();
    }
  };

  // Handle location selection from typeahead
  const handleLocationFromTypeahead = (locationData: any) => {
    if (locationData.location) {
      const newRegion: LocationState = {
        latitude: locationData.location.lat,
        longitude: locationData.location.lng,
        latitudeDelta: 0.01,
        longitudeDelta: 0.01,
      };

      if (mapRef.current) {
        mapRef.current.animateToRegion(newRegion, 1000);
      }
    }
  };

  // Handle parking spot selection from carousel
  const handleSpotPress = (spot: ParkingSpot) => {
    const spotLocation: LocationState = {
      latitude: spot.latitude,
      longitude: spot.longitude,
      latitudeDelta: 0.01,
      longitudeDelta: 0.01,
    };

    // Animate map to spot location
    if (mapRef.current) {
      mapRef.current.animateToRegion(spotLocation, 1000);
    }

    // Show spot details
    Alert.alert(
      spot.title,
      `${spot.address}\n\nPreço: R$ ${spot.price_per_hour.toFixed(2)}/hora\nVagas disponíveis: ${spot.available_spots}\nDistância: ${spot.distance}km`,
      [
        { text: 'Cancelar', style: 'cancel' },
        {
          text: 'Reservar',
          onPress: () => {
            // Navigate to booking screen or show booking modal
            console.log('Navigate to booking for spot:', spot.id);
          }
        },
      ]
    );
  };

  return (
    <View className="flex-1 bg-gray-50">
      <View className='px-4 pt-4'>
        <Typography variant='body'>Bom dia, Lucas!</Typography>
        <Typography variant='h3'>Onde voce quer estacionar?</Typography>
      </View>
      {/* Search Input - Fixed height */}
      <View className="flex-row items-center px-4 py-4 shaddow-lg">
        <TypeaheadExample onLocationSelect={handleLocationFromTypeahead} />
      </View>

      {/* Messages Container */}
      <View className="bg-gray-50 mt-4">
        {/* Permission Denied Message */}
        {showPermissionDeniedMessage && (
          <View className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mx-4 mb-2">
            <View className="flex flex-row items-start">
              <Feather name="alert-triangle" size={20} color="#F59E0B" />
              <View className="flex-1 ml-2">
                <Text className="text-yellow-800 font-medium text-sm">
                  Localização desabilitada
                </Text>
                <Text className="text-yellow-700 text-xs mt-1">
                  Ative a localização para encontrar vagas próximas a você.
                </Text>
                <TouchableOpacity
                  onPress={requestLocationPermission}
                  className="mt-2"
                >
                  <Text className="text-yellow-800 font-medium text-xs underline">
                    Tentar novamente
                  </Text>
                </TouchableOpacity>
              </View>
            </View>
          </View>
        )}

        {/* Location Error Message */}
        {locationError && (
          <View className="bg-red-50 border-l-4 border-red-400 p-4 mx-4 mb-2">
            <View className="flex flex-row items-start">
              <Feather name="alert-circle" size={20} color="#EF4444" />
              <View className="flex-1 ml-2">
                <Text className="text-red-800 font-medium text-sm">
                  Erro de localização
                </Text>
                <Text className="text-red-700 text-xs mt-1">
                  {locationError}
                </Text>
              </View>
            </View>
          </View>
        )}
      </View>

      <View className="flex-1 relative">
        <MapView 
          ref={mapRef}
          provider={PROVIDER_GOOGLE}
          style={styles.map}
          initialRegion={location || DEFAULT_LOCATION}
          showsUserLocation={locationPermission === 'granted'}
          showsMyLocationButton={false} // We'll use custom button
          followsUserLocation={false}
          toolbarEnabled={false}
        />

        <TouchableOpacity
          onPress={handleCurrentLocationPress}
          className="absolute bottom-4 right-4 bg-white rounded-full p-3 shadow-lg border border-gray-200"
          disabled={isLoadingLocation}
        >
          {isLoadingLocation ? (
            <Feather name="loader" size={24} color="#3B82F6" />
          ) : (
            <Feather
              name="crosshair"
              size={24}
              color={locationPermission === 'granted' ? '#3B82F6' : '#9CA3AF'}
            />
          )}
        </TouchableOpacity>
      </View>

      {/* Quick Actions */}
      {/* <View className="px-4 pb-6">
        <Text className="text-lg font-semibold text-gray-900 mb-3">Ações rápidas</Text>
        <View className="flex-row justify-between">
          <TouchableOpacity className="flex-1 bg-white p-4 rounded-xl mr-2 items-center shadow-sm border border-gray-100">
            <Feather name="search" size={24} color="#3B82F6" className="mb-2" />
            <Text className="text-sm font-medium text-gray-900">Buscar vaga</Text>
          </TouchableOpacity>

          <TouchableOpacity className="flex-1 bg-white p-4 rounded-xl mx-1 items-center shadow-sm border border-gray-100">
            <Feather name="clock" size={24} color="#10B981" className="mb-2" />
            <Text className="text-sm font-medium text-gray-900">Minhas reservas</Text>
          </TouchableOpacity>

          <TouchableOpacity className="flex-1 bg-white p-4 rounded-xl ml-2 items-center shadow-sm border border-gray-100">
            <Feather name="plus" size={24} color="#F59E0B" className="mb-2" />
            <Text className="text-sm font-medium text-gray-900">Anunciar vaga</Text>
          </TouchableOpacity>
        </View>
      </View> */}
    </View>
  );
}

const styles = StyleSheet.create({
  map: {
    flex: 1,
    width: '100%',
    height: '100%',
  },
});
