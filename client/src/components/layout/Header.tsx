import { View, Text } from 'react-native';
import AntDesign from '@expo/vector-icons/AntDesign';
import { Typography } from '@/src/components/ui/Typography';


interface HeaderProps {
  title: string;
  onPrevious?: () => void;
}

export const Header = (props: HeaderProps) => {
  const { title, onPrevious } = props;

  return (
    <View className="flex-row items-center justify-center px-4 py-2">
      {onPrevious && <AntDesign name="arrowleft" size={24} color="black" />}
      <Typography variant="h3">{title}</Typography>
      {/* <View className="border-b border-gray-200 my-2" /> */}
    </View>
  );
}