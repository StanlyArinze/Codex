import { Redirect, Stack, useSegments } from "expo-router";

import { AuthProvider, useAuth } from "../src/auth";

function Gate() {
  const { ready, signedIn } = useAuth();
  const segments = useSegments();
  const inAuthGroup = segments[0] === "(auth)";

  if (!ready) return null;
  if (!signedIn && !inAuthGroup) return <Redirect href="/(auth)/login" />;
  if (signedIn && inAuthGroup) return <Redirect href="/(app)" />;

  return (
    <Stack
      screenOptions={{
        headerStyle: { backgroundColor: "#4f46e5" },
        headerTintColor: "#fff",
        contentStyle: { backgroundColor: "#f6f8ff" }
      }}
    />
  );
}

export default function Layout() {
  return (
    <AuthProvider>
      <Gate />
    </AuthProvider>
  );
}
