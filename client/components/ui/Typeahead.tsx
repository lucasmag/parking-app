import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  ActivityIndicator,
  Keyboard,
  Dimensions,
  ListRenderItem
} from 'react-native';
import { Feather } from '@expo/vector-icons';

const { height: screenHeight } = Dimensions.get('window');

// Google Places API Configuration
const GOOGLE_PLACES_API_KEY = 'AIzaSyCMsvXaEm1guNzXM-cK0UGjd2MVHlktfZs'; // Replace with your API key
const GOOGLE_PLACES_BASE_URL = 'https://maps.googleapis.com/maps/api/place';

// Type definitions
interface GooglePlacesLocation {
  lat: number;
  lng: number;
}

interface GooglePlacesGeometry {
  location: GooglePlacesLocation;
  viewport?: {
    northeast: GooglePlacesLocation;
    southwest: GooglePlacesLocation;
  };
}

interface GooglePlacesStructuredFormatting {
  main_text: string;
  main_text_matched_substrings?: Array<{
    offset: number;
    length: number;
  }>;
  secondary_text?: string;
  secondary_text_matched_substrings?: Array<{
    offset: number;
    length: number;
  }>;
}

interface GooglePlacesPrediction {
  description: string;
  matched_substrings: Array<{
    offset: number;
    length: number;
  }>;
  place_id: string;
  reference: string;
  structured_formatting: GooglePlacesStructuredFormatting;
  terms: Array<{
    offset: number;
    value: string;
  }>;
  types: string[];
  distance_meters?: number;
}

interface GooglePlacesAutocompleteResponse {
  predictions: GooglePlacesPrediction[];
  status: 'OK' | 'ZERO_RESULTS' | 'OVER_QUERY_LIMIT' | 'REQUEST_DENIED' | 'INVALID_REQUEST' | 'UNKNOWN_ERROR';
  error_message?: string;
}

interface GooglePlaceDetailsResult {
  formatted_address: string;
  geometry: GooglePlacesGeometry;
  name: string;
  place_id: string;
  types: string[];
  address_components?: Array<{
    long_name: string;
    short_name: string;
    types: string[];
  }>;
}

interface GooglePlaceDetailsResponse {
  result: GooglePlaceDetailsResult;
  status: 'OK' | 'ZERO_RESULTS' | 'OVER_QUERY_LIMIT' | 'REQUEST_DENIED' | 'INVALID_REQUEST' | 'NOT_FOUND' | 'UNKNOWN_ERROR';
  error_message?: string;
}

interface LocationData {
  address: string;
  name?: string;
  location: GooglePlacesLocation;
  types?: string[];
  placeId?: string;
  isCurrentLocation?: boolean;
  addressComponents?: GooglePlaceDetailsResult['address_components'];
}

interface ProximityLocation {
  lat: number;
  lng: number;
}

type PlaceTypes = 'address' | 'establishment' | 'geocode' | '(cities)' | '(regions)';

interface GoogleMapsTypeaheadProps {
  placeholder?: string;
  onAddressSelect?: (address: string, prediction: GooglePlacesPrediction | { isCurrentLocation: boolean }) => void;
  onLocationSelect?: (locationData: LocationData) => void;
  initialValue?: string;
  countryCode?: string;
  types?: PlaceTypes;
  radius?: number;
  location?: ProximityLocation;
  className?: string;
  showCurrentLocation?: boolean;
  currentLocationText?: string;
  maxResults?: number;
  debounceMs?: number;
}

interface SuggestionItemProps {
  item: GooglePlacesPrediction;
  onPress: (item: GooglePlacesPrediction) => void;
}

const GoogleMapsTypeahead: React.FC<GoogleMapsTypeaheadProps> = ({
  placeholder = "Search for address...",
  onAddressSelect,
  onLocationSelect,
  initialValue = "",
  countryCode = "BR",
  radius = null,
  location = null,
  className = "",
  showCurrentLocation = true,
  currentLocationText = "Use current location",
  maxResults = 5,
  debounceMs = 300
}) => {
  const [query, setQuery] = useState<string>(initialValue);
  const [predictions, setPredictions] = useState<GooglePlacesPrediction[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [showSuggestions, setShowSuggestions] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  
  const debounceRef = useRef<number | null>(null);
  const inputRef = useRef<TextInput>(null);

  // Debounced search function
  const searchPlaces = async (searchQuery: string): Promise<void> => {
    if (!searchQuery.trim() || searchQuery.length < 2) {
      setPredictions([]);
      setIsLoading(false);
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      let url = `${GOOGLE_PLACES_BASE_URL}/autocomplete/json?input=${encodeURIComponent(searchQuery)}&key=${GOOGLE_PLACES_API_KEY}`;
      
      // Add country restriction
      if (countryCode) {
        url += `&components=country:${countryCode}`;
      }
      
      // Add location bias for proximity
      if (location) {
        url += `&location=${location.lat},${location.lng}`;
        if (radius) {
          url += `&radius=${radius}`;
        }
      }

      const response = await fetch(url);
      const data: GooglePlacesAutocompleteResponse = await response.json();

      if (data.status === 'OK') {
        setPredictions(data.predictions.slice(0, maxResults));
      } else {
        console.log(data.status)
        setError(data.error_message || 'Error fetching addresses');
        setPredictions([]);
      }
    } catch (err) {
      setError('Network error occurred');
      setPredictions([]);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle text input changes with debouncing
  const handleInputChange = (text: string): void => {
    setQuery(text);
    setShowSuggestions(true);

    // Clear previous debounce
    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }

    // Set new debounce
    debounceRef.current = setTimeout(() => {
      searchPlaces(text);
    }, debounceMs);
  };

  // Get place details (coordinates) from place_id
  const getPlaceDetails = async (placeId: string): Promise<LocationData | null> => {
    try {
      const response = await fetch(
        `${GOOGLE_PLACES_BASE_URL}/details/json?place_id=${placeId}&fields=geometry,formatted_address,name,types,address_components&key=${GOOGLE_PLACES_API_KEY}`
      );
      const data: GooglePlaceDetailsResponse = await response.json();

      if (data.status === 'OK') {
        return {
          address: data.result.formatted_address,
          name: data.result.name,
          location: data.result.geometry.location,
          types: data.result.types,
          placeId: placeId,
          addressComponents: data.result.address_components
        };
      }
      return null;
    } catch (err) {
      console.error('Error fetching place details:', err);
      return null;
    }
  };

  // Handle address selection
  const handleAddressSelect = async (prediction: GooglePlacesPrediction): Promise<void> => {
    setQuery(prediction.description);
    setShowSuggestions(false);
    setPredictions([]);
    Keyboard.dismiss();

    // Get detailed information including coordinates
    const placeDetails = await getPlaceDetails(prediction.place_id);
    
    if (placeDetails) {
      onLocationSelect?.(placeDetails);
    }
    
    onAddressSelect?.(prediction.description, prediction);
  };

  // Handle current location selection
  const handleCurrentLocation = (): void => {
    setQuery(currentLocationText);
    setShowSuggestions(false);
    setPredictions([]);
    
    // Request current location
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const locationData: LocationData = {
            address: currentLocationText,
            location: {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            },
            isCurrentLocation: true
          };
          onLocationSelect?.(locationData);
        },
        (error) => {
          console.error('Error getting current location:', error);
          setError('Unable to get current location');
        },
        { enableHighAccuracy: true, timeout: 15000, maximumAge: 10000 }
      );
    }
    
    onAddressSelect?.(currentLocationText, { isCurrentLocation: true });
  };

  // Clear search
  const handleClear = (): void => {
    setQuery('');
    setPredictions([]);
    setShowSuggestions(false);
    setError(null);
    inputRef.current?.focus();
  };

  // Hide suggestions when input loses focus
  const handleBlur = (): void => {
    // Delay hiding to allow for tap on suggestion
    setTimeout(() => {
      setShowSuggestions(false);
    }, 150);
  };

  // Cleanup debounce on unmount
  useEffect(() => {
    return () => {
      if (debounceRef.current) {
        clearTimeout(debounceRef.current);
      }
    };
  }, []);

  // Suggestion Item Component
  const SuggestionItem: React.FC<SuggestionItemProps> = ({ item, onPress }) => (
    <TouchableOpacity
      onPress={() => onPress(item)}
      className="flex-row items-center py-3 px-4 border-b border-gray-100"
      activeOpacity={0.7}
    >
      <View className="w-8 h-8 bg-gray-100 rounded-full justify-center items-center mr-3">
        <Feather 
          name={item.types?.includes('establishment') ? 'map-pin' : 'map-pin'} 
          size={16} 
          color="#6B7280" 
        />
      </View>
      
      <View className="flex-1">
        <Text className="text-gray-900 font-medium text-base mb-1">
          {item.structured_formatting?.main_text || item.description}
        </Text>
        {item.structured_formatting?.secondary_text && (
          <Text className="text-gray-500 text-sm">
            {item.structured_formatting.secondary_text}
          </Text>
        )}
      </View>
      
      <Feather name="arrow-up-left" size={16} color="#9CA3AF" />
    </TouchableOpacity>
  );

  // Current Location Item Component
  const CurrentLocationItem: React.FC = () => (
    <TouchableOpacity
      onPress={handleCurrentLocation}
      className="flex-row items-center py-3 px-4 border-b border-gray-100"
      activeOpacity={0.7}
    >
      <View className="w-8 h-8 bg-blue-100 rounded-full justify-center items-center mr-3">
        <Feather name="crosshair" size={16} color="#3B82F6" />
      </View>
      
      <View className="flex-1">
        <Text className="text-blue-600 font-medium text-base">
          {currentLocationText}
        </Text>
      </View>
      
      <Feather name="crosshair" size={16} color="#3B82F6" />
    </TouchableOpacity>
  );

  const renderSuggestionItem: ListRenderItem<GooglePlacesPrediction> = ({ item }) => (
    <SuggestionItem item={item} onPress={handleAddressSelect} />
  );

  return (
    <View className={`relative ${className}`}>
      {/* Input Field */}
      <View className="relative">
        <View className="flex-row items-center bg-white rounded-xl border border-gray-200 px-4 py-3">
          <Feather name="search" size={20} color="#9CA3AF" />
          
          <TextInput
            ref={inputRef}
            value={query}
            onChangeText={handleInputChange}
            onFocus={() => setShowSuggestions(true)}
            onBlur={handleBlur}
            placeholder={placeholder}
            placeholderTextColor="#9CA3AF"
            className="flex-1 ml-3 text-gray-900 text-base"
            autoCorrect={false}
            autoCapitalize="none"
          />
          
          {isLoading && (
            <ActivityIndicator size="small" color="#3B82F6" />
          )}
          
          {query.length > 0 && !isLoading && (
            <TouchableOpacity onPress={handleClear} className="p-1">
              <Feather name="x" size={18} color="#9CA3AF" />
            </TouchableOpacity>
          )}
        </View>

        {/* Error Message */}
        {error && (
          <View className="mt-2 px-4">
            <Text className="text-red-500 text-sm">{error}</Text>
          </View>
        )}
      </View>

      {/* Suggestions Dropdown */}
      {showSuggestions && (predictions.length > 0 || showCurrentLocation) && (
        <View className="absolute top-full left-0 right-0 bg-white rounded-xl border border-gray-200 shadow-lg z-50 mt-1">
          <FlatList
            data={predictions}
            keyExtractor={(item) => item.place_id}
            renderItem={renderSuggestionItem}
            ListHeaderComponent={
              showCurrentLocation && query.length === 0 ? (
                <CurrentLocationItem />
              ) : null
            }
            showsVerticalScrollIndicator={false}
            keyboardShouldPersistTaps="handled"
            style={{ 
              maxHeight: Math.min(
                predictions.length * 70 + (showCurrentLocation ? 60 : 0), 
                screenHeight * 0.4
              ) 
            }}
          />
        </View>
      )}
    </View>
  );
};

// Usage Example Component
interface TypeaheadExampleState {
  selectedAddress: string;
  selectedLocation: LocationData | null;
}

const TypeaheadExample: React.FC = () => {
  const [selectedAddress, setSelectedAddress] = useState<string>('');
  const [selectedLocation, setSelectedLocation] = useState<LocationData | null>(null);

  const handleAddressSelect = (
    address: string, 
    prediction: GooglePlacesPrediction | { isCurrentLocation: boolean }
  ): void => {
    console.log('Selected address:', address);
    // console.log('Prediction object:', prediction);
    setSelectedAddress(address);
  };

  const handleLocationSelect = (locationData: LocationData): void => {
    console.log('Location details:', locationData);
    setSelectedLocation(locationData);
  };

  return (
    <View className="flex-1 bg-gray-50 p-4">
      <View>
        <GoogleMapsTypeahead
          placeholder="Onde você quer estacionar?"
          onAddressSelect={handleAddressSelect}
          onLocationSelect={handleLocationSelect}
          countryCode="BR"
          showCurrentLocation={true}
          maxResults={5}
        />
      </View>

      {/* {selectedAddress && (
        <View className="bg-white rounded-xl p-4 border border-gray-200">
          <Text className="text-gray-900 font-semibold text-base mb-2">Selected Address:</Text>
          <Text className="text-gray-700 text-sm mb-3">{selectedAddress}</Text>
          
          {selectedLocation && (
            <View>
              <Text className="text-gray-900 font-semibold text-base mb-2">Coordinates:</Text>
              <Text className="text-gray-700 text-sm">
                Lat: {selectedLocation.location?.lat?.toFixed(6)}, 
                Lng: {selectedLocation.location?.lng?.toFixed(6)}
              </Text>
              
              {selectedLocation.types && (
                <View className="mt-2">
                  <Text className="text-gray-900 font-semibold text-base mb-1">Types:</Text>
                  <Text className="text-gray-700 text-sm">
                    {selectedLocation.types.join(', ')}
                  </Text>
                </View>
              )}
            </View>
          )}
        </View>
      )} */}
    </View>
  );
};

export type { 
  GoogleMapsTypeaheadProps,
  LocationData,
  GooglePlacesPrediction,
  GooglePlacesLocation,
  ProximityLocation,
  PlaceTypes
};
export { GoogleMapsTypeahead };
export default TypeaheadExample;
