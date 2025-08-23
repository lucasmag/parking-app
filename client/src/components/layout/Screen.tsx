import React from 'react';
import { View } from 'react-native';

/**
 * A reusable Screen component that handles safe area and default padding.
 * It uses View from React Native to apply theme-based padding.
 * All screens in the app should be wrapped with this component.
 */
const Screen = ({ children }: { children: React.ReactNode }) => {
  return (
    <View 
      className="flex-1 bg-background px-4"
    >
      {children}
    </View>
  );
};

export default Screen;
