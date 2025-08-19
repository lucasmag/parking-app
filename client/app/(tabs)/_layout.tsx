import TabOption from '@/components/ui/TabOption';
import { Tabs, TabList, TabTrigger, TabSlot } from 'expo-router/ui';

export default function TabLayout() {
  return (
    <Tabs className="bg-background">
      <TabSlot />
      <TabList className="border-t border-gray-200 px-4">
        <TabTrigger name="home" href="/" className="flex-1">
          <TabOption iconName="home" label="Inicio" />
        </TabTrigger>
        <TabTrigger name="bookings" href="/bookings" className="flex-1">
          <TabOption iconName="bookings" label="Reservas" />
        </TabTrigger>
        <TabTrigger name="profile" href="/profile" className="flex-1">
          <TabOption iconName="profile" label="Perfil" />
        </TabTrigger>
      </TabList>
    </Tabs>
  );
}
