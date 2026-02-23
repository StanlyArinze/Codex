import { Link } from "expo-router";
import { useState } from "react";
import { Pressable, StyleSheet, Text, TextInput, View } from "react-native";

import { useAuth } from "../../src/auth";

export default function LoginScreen() {
  const { signIn } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  const submit = async () => {
    const message = await signIn(email, password);
    setError(message);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Entrar no IA Finance</Text>
      <TextInput style={styles.input} placeholder="E-mail" autoCapitalize="none" value={email} onChangeText={setEmail} />
      <TextInput style={styles.input} placeholder="Senha" secureTextEntry value={password} onChangeText={setPassword} />
      {error ? <Text style={styles.error}>{error}</Text> : null}
      <Pressable style={styles.button} onPress={submit}>
        <Text style={styles.buttonText}>Entrar</Text>
      </Pressable>
      <Link href="/(auth)/register" style={styles.link}>Criar conta</Link>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, gap: 12, justifyContent: "center" },
  title: { fontSize: 26, fontWeight: "700", color: "#111827", marginBottom: 8 },
  input: { backgroundColor: "#fff", borderRadius: 10, borderWidth: 1, borderColor: "#d1d5db", padding: 12 },
  button: { backgroundColor: "#4f46e5", padding: 12, borderRadius: 10, marginTop: 4 },
  buttonText: { color: "#fff", textAlign: "center", fontWeight: "600" },
  link: { textAlign: "center", color: "#4f46e5", marginTop: 10 },
  error: { color: "#b91c1c" }
});
