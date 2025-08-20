import React, { useState, useEffect, useRef } from 'react';
import { Header } from '@/components/ui/Header';
import TypeaheadExample from '@/components/ui/Typeahead';
import { Typography } from '@/components/ui/Typography';
import { View, Text, StyleSheet, Alert, TouchableOpacity } from 'react-native';
import MapView, { PROVIDER_GOOGLE, Marker, Region } from 'react-native-maps';
import * as Location from 'expo-location';
import { Feather } from '@expo/vector-icons';

interface LocationState {
  latitude: number;
  longitude: number;
  latitudeDelta: number;
  longitudeDelta: number;
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

  return (
    <View className="flex-1 bg-gray-50 space-between">
      {/* Header - Fixed height */}
      <View className="bg-white pt-2.5 pb-1 border-b border-gray-200">
        <Header title="Estaciona" />
      </View>
      
      {/* Search Input - Fixed height */}
      <View className="flex-row items-center h-[65px]">
        <TypeaheadExample onLocationSelect={handleLocationFromTypeahead} />
      </View>

      {/* Messages Container - Dynamic height */}
      <View className="bg-gray-50 pt-2">
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

      {/* Map Container - Takes remaining height */}
      <View className="flex-1 relative">
        <MapView 
          ref={mapRef}
          provider={PROVIDER_GOOGLE} 
          style={styles.map}
          initialRegion={location || DEFAULT_LOCATION}
          showsUserLocation={locationPermission === 'granted'}
          showsMyLocationButton={false} // We'll use custom button
          followsUserLocation={false}
          toolbarEnabled={false} />

        <TouchableOpacity
          onPress={handleCurrentLocationPress}
          className="absolute bottom-6 right-4 bg-white rounded-full p-3 shadow-lg border border-gray-200"
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
    </View>
  );
}

const styles = StyleSheet.create({
  map: {
    flexGrow: 1,
    flexShrink: 1,
    width: '100%',
    height: '80%',
  },
});
