import { useEffect, useState } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";

import { fetchHome } from "../../src/api";
import { useAuth } from "../../src/auth";

export default function DashboardScreen() {
  const { signOut } = useAuth();
  const [status, setStatus] = useState("Carregando dashboard...");

  useEffect(() => {
    fetchHome()
      .then((html) => {
        setStatus(html.includes("Transações do período") ? "Dashboard conectado ✅" : "Sessão inválida / backend offline");
      })
      .catch(() => setStatus("Não foi possível conectar ao backend"));
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>IA Finance Mobile</Text>
      <Text style={styles.status}>{status}</Text>

      <View style={styles.cardRow}>
        <View style={[styles.card, styles.balance]}>
          <Text style={styles.cardLabel}>Saldo</Text>
          <Text style={styles.cardValue}>Conectado</Text>
        </View>
        <View style={[styles.card, styles.expense]}>
          <Text style={styles.cardLabel}>Gastos</Text>
          <Text style={styles.cardValue}>Conectado</Text>
        </View>
      </View>

      <Pressable style={styles.logoutButton} onPress={signOut}>
        <Text style={styles.logoutText}>Sair</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, gap: 16 },
  title: { fontSize: 28, fontWeight: "700", color: "#111827" },
  status: { color: "#4b5563" },
  cardRow: { flexDirection: "row", gap: 12 },
  card: { flex: 1, borderRadius: 14, padding: 14 },
  balance: { backgroundColor: "#16a34a" },
  expense: { backgroundColor: "#dc2626" },
  cardLabel: { color: "#fff", fontWeight: "600" },
  cardValue: { color: "#fff", fontSize: 18, fontWeight: "700", marginTop: 6 },
  logoutButton: { marginTop: 12, backgroundColor: "#111827", borderRadius: 10, padding: 12 },
  logoutText: { color: "#fff", textAlign: "center", fontWeight: "600" }
});
