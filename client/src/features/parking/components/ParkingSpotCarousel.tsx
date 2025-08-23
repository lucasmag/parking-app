import { ParkingSpot } from "../types";
import { View, useWindowDimensions } from "react-native";
import React from "react";
import Carousel from "react-native-reanimated-carousel";
import { useSharedValue } from "react-native-reanimated";
import ParkingSpotCard from "./ParkingSpotCard";

interface ParkingSpotCarouselProps {
  spots: ParkingSpot[];
  className?: string;
}

export default function ParkingSpotCarousel(props: ParkingSpotCarouselProps) {
  const {spots, className} = props;
  const scrollOffsetValue = useSharedValue<number>(0);
  const { width: screenWidth } = useWindowDimensions();

  return (
    <View className={className}>
			<Carousel
				loop={false}
				width={screenWidth - 60}
				height={150}
				snapEnabled={true}
				pagingEnabled={true}
				autoPlayInterval={2000}
				data={spots}
				defaultScrollOffsetValue={scrollOffsetValue}
        style={{
          flex: 1,
          justifyContent: 'center',
          width: "100%",
          height: 150,
        }}
				onScrollStart={() => {
					console.log("Scroll start");
				}}
				onScrollEnd={() => {
					console.log("Scroll end");
				}}
				onConfigurePanGesture={(g: { enabled: (arg0: boolean) => any }) => {
					"worklet";
					g.enabled(false);
				}}
				onSnapToItem={(index: number) => console.log("current index:", index)}
				renderItem={({item}) => <ParkingSpotCard spot={item} onPress={() => console.log(item.address)}/>}
			/>
		</View>
  )
}