import { Pressable, View, Text } from "react-native";

interface CardProps {
  children: React.ReactNode;
  className?: string;
}

function Card(props: CardProps) {
  return (
    <View className={`bg-white rounded-2xl p-4 shadow-md ${props.className}`}>
      {props.children}
    </View>
  );
}

interface CardWithHeaderProps extends CardProps {
  title: string;
  linkText?: string;
  linkAction?: () => void;
}

function CardWithHeader(props: CardWithHeaderProps) {
  return (
    <Card className={props.className}>
      <View className="flex-row justify-between items-center mb-4">
        <Text className="font-bold text-lg">{props.title}</Text>
        <Pressable onPress={props.linkAction}>
          <Text className="text-gray-500 font-semibold">{props.linkText}</Text>
        </Pressable>
      </View>
      {props.children}
    </Card>
  );
}

export { Card, CardWithHeader };