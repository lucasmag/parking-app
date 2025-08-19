import { Header } from '@/components/ui/Header';
import TypeaheadExample from '@/components/ui/Typeahead';
import { Typography } from '@/components/ui/Typography';
import { View, Text, StyleSheet} from 'react-native';
import MapView, { PROVIDER_GOOGLE } from 'react-native-maps';

export default function HomeScreen() {
  return (
    <View className="flex flex-col space-between">
      <Header title="Estaciona" /> 
      <View className="flex flex-row items-center justify-center">  
        <TypeaheadExample />
      </View>
      
      <View className="">
        <MapView provider={PROVIDER_GOOGLE} style={styles.map} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  map: {
    width: '100%',
    height: '100%',},
});