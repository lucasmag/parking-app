import { Link, Stack } from 'expo-router';
import { StyleSheet } from 'react-native';
import Screen from '@/components/ui/Screen';
import { Text } from 'react-native';


export default function NotFoundScreen() {
  return (
    <Screen>
      <Stack.Screen options={{ title: 'Oops!' }} />
        <Text>This screen does not exist.</Text>
        <Link href="/" style={styles.link}>
          <Text>Go to home screen!</Text>
        </Link>
    </Screen>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  link: {
    marginTop: 15,
    paddingVertical: 15,
  },
});
