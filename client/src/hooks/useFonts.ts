import { Inter_500Medium, Inter_300Light, Inter_600SemiBold, Inter_700Bold, Inter_400Regular} from '@expo-google-fonts/inter';
import { SpaceGrotesk_300Light, SpaceGrotesk_400Regular, SpaceGrotesk_500Medium, SpaceGrotesk_600SemiBold, SpaceGrotesk_700Bold } from '@expo-google-fonts/space-grotesk';
import { useFonts as useExpoFonts } from 'expo-font';
import * as SplashScreen from 'expo-splash-screen';
import { useCallback } from 'react';

SplashScreen.preventAutoHideAsync();

export const useAppFonts = () => {
  const [fontsLoaded, fontError] = useExpoFonts({
    // Space Grotesk (Display)
    'SpaceGrotesk-Light': SpaceGrotesk_300Light,
    'SpaceGrotesk-Regular': SpaceGrotesk_400Regular,
    'SpaceGrotesk-Medium': SpaceGrotesk_500Medium,
    'SpaceGrotesk-SemiBold': SpaceGrotesk_600SemiBold,
    'SpaceGrotesk-Bold': SpaceGrotesk_700Bold,

    // Inter (Body)
    'Inter-Light': Inter_300Light,
    'Inter-Regular': Inter_400Regular,
    'Inter-Medium': Inter_500Medium,
    'Inter-SemiBold': Inter_600SemiBold,
    'Inter-Bold': Inter_700Bold,
  });

  const onLayoutRootView = useCallback(async () => {
    if (fontsLoaded || fontError) {
      await SplashScreen.hideAsync();
    }
  }, [fontsLoaded, fontError]);

  return {
    fontsLoaded: fontsLoaded && !fontError,
    onLayoutRootView,
    fontError
  };
};
