import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import 'react-native-reanimated';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useAppFonts } from '@/src/hooks/useFonts';
import { ActivityIndicator, Text, View, StyleSheet } from 'react-native';
import '@/global.css';

const queryClient = new QueryClient();

export default function RootLayout() {
  const { fontsLoaded, onLayoutRootView, fontError } = useAppFonts();

  const LoadingScreen: React.FC = () => (
    <View style={styles.loadingContainer}>
      <ActivityIndicator size="large" color="#3B82F6" />
      <Text style={styles.loadingText}>Loading fonts...</Text>
    </View>
  );

  const ErrorScreen: React.FC<{ error: Error }> = ({ error }) => (
    <View style={styles.errorContainer}>
      <Text style={styles.errorTitle}>Font Loading Error</Text>
      <Text style={styles.errorMessage}>
        {error.message || 'Unable to load fonts. Please restart the app.'}
      </Text>
    </View>
  );

  if (!fontsLoaded) {
    return <LoadingScreen />;
  }

  if (fontError) {
    return <ErrorScreen error={fontError} />;
  }

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SafeAreaProvider>
        <SafeAreaView style={{ flex: 1 }} onLayout={onLayoutRootView}>
          <QueryClientProvider client={queryClient}>
            <StatusBar style="auto" />
            <Stack>
              <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
              <Stack.Screen name="+not-found" />
            </Stack>
          </QueryClientProvider>
        </SafeAreaView>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FAFB',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#6B7280',
    fontFamily: 'System', // Fallback to system font
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    padding: 20,
  },
  errorTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#EF4444',
    marginBottom: 8,
    textAlign: 'center',
  },
  errorMessage: {
    fontSize: 16,
    color: '#6B7280',
    textAlign: 'center',
    lineHeight: 24,
  },
});
