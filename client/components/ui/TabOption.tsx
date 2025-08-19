import React from "react";
import { View, Text } from "react-native";
import { usePathname } from "expo-router";
import MaterialCommunityIcons from '@expo/vector-icons/MaterialCommunityIcons';
import colors from "tailwindcss/colors";
import AntDesign from '@expo/vector-icons/AntDesign';


type TabOptionProps = {
  iconName: string;
  label: string;
  size?: number;
  color?: string;
};

const displayIcon = (isActive: boolean, iconName: string, color: string) => {
  return {
      home: <AntDesign name="home" size={24} color={color} />,
      bookings: <MaterialCommunityIcons name="car-clock" size={24} color={color} />,
      profile: <AntDesign name="user" size={24} color={color} />,
  }[iconName];
}

const optionMap = {
  home: "/",
  bookings: "/bookings",
  profile: "/profile",
}

const TabOption: React.FC<TabOptionProps> = ({
  iconName,
  label,
}) => {
  const pathname = usePathname();
  const isActive = (path: string) => pathname === optionMap[path as keyof typeof optionMap];
  const color = isActive(iconName) ? colors.cyan[500] : colors.gray[600];
  const textColor = isActive(iconName) ? "text-cyan-500" : "text-gray-600";

  return (
    <View className="w-full flex items-center justify-center h-20">
      {displayIcon(isActive(iconName), iconName, color)}
      <Text className={`mt-1 text-sm font-semibold ${textColor}`}>{label}</Text>
    </View>
  );
};

export default TabOption;
