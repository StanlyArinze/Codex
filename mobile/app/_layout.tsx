import { Stack } from "expo-router";

export default function Layout() {
  return (
    <Stack
      screenOptions={{
        headerStyle: { backgroundColor: "#5b21b6" },
        headerTintColor: "#fff",
        contentStyle: { backgroundColor: "#f8fafc" }
      }}
    />
  );
}
