import { useEffect, useMemo, useState } from "react";
import { Pressable, ScrollView, StyleSheet, Text, TextInput, View } from "react-native";

import { createTransaction, DashboardPayload, fetchDashboard } from "../../src/api";
import { useAuth } from "../../src/auth";

function money(value: string): string {
  const parsed = Number(value || "0");
  if (Number.isNaN(parsed)) return "R$ 0,00";
  return parsed.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

export default function DashboardScreen() {
  const { signOut } = useAuth();
  const [period, setPeriod] = useState("");
  const [status, setStatus] = useState("Carregando dados...");
  const [data, setData] = useState<DashboardPayload | null>(null);
  const [loading, setLoading] = useState(false);

  const [amount, setAmount] = useState("");
  const [description, setDescription] = useState("");
  const [txnDate, setTxnDate] = useState(new Date().toISOString().slice(0, 10));

  const loadDashboard = async (selectedPeriod?: string) => {
    setLoading(true);
    try {
      const payload = await fetchDashboard(selectedPeriod);
      if (!payload) {
        setStatus("Não foi possível carregar o dashboard.");
        return;
      }

      setData(payload);
      setStatus("Dashboard atualizado ✅");
    } catch {
      setStatus("Erro de conexão com o backend.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  const handleAddTransaction = async (transactionType: "income" | "expense") => {
    if (!amount || !description.trim() || !txnDate) {
      setStatus("Preencha valor, descrição e data antes de salvar.");
      return;
    }

    const ok = await createTransaction({
      transaction_type: transactionType,
      amount,
      description: description.trim(),
      txn_date: txnDate
    });

    if (!ok) {
      setStatus("Não foi possível salvar a transação.");
      return;
    }

    setAmount("");
    setDescription("");
    setStatus("Transação salva com sucesso.");
    await loadDashboard(period || undefined);
  };

  const transactionCountLabel = useMemo(() => {
    const total = data?.transactions.length ?? 0;
    if (total === 1) return "1 transação";
    return `${total} transações`;
  }, [data]);

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>IA Finance Mobile</Text>
      <Text style={styles.status}>{status}</Text>

      <View style={styles.filterRow}>
        <TextInput
          style={styles.input}
          placeholder="Período (YYYY-MM)"
          autoCapitalize="none"
          value={period}
          onChangeText={setPeriod}
        />
        <Pressable style={styles.actionButton} onPress={() => loadDashboard(period || undefined)}>
          <Text style={styles.actionButtonText}>{loading ? "..." : "Filtrar"}</Text>
        </Pressable>
      </View>

      <View style={styles.cardRow}>
        <View style={[styles.card, styles.balance]}>
          <Text style={styles.cardLabel}>Saldo</Text>
          <Text style={styles.cardValue}>{money(data?.summary.balance ?? "0")}</Text>
        </View>
        <View style={[styles.card, styles.expense]}>
          <Text style={styles.cardLabel}>Gastos</Text>
          <Text style={styles.cardValue}>{money(data?.summary.expense ?? "0")}</Text>
        </View>
      </View>

      <View style={styles.infoCard}>
        <Text style={styles.infoLabel}>Período</Text>
        <Text style={styles.infoValue}>{data?.period ?? "-"}</Text>
        <Text style={styles.infoLabel}>Top categoria</Text>
        <Text style={styles.infoValue}>{data?.top_category ?? "-"}</Text>
        <Text style={styles.infoLabel}>Insight</Text>
        <Text style={styles.infoValue}>{data?.insight ?? "-"}</Text>
      </View>

      <View style={styles.formCard}>
        <Text style={styles.sectionTitle}>Nova transação</Text>
        <TextInput
          style={styles.input}
          placeholder="Valor (ex: 120.50)"
          value={amount}
          onChangeText={setAmount}
          keyboardType="decimal-pad"
        />
        <TextInput
          style={styles.input}
          placeholder="Descrição"
          value={description}
          onChangeText={setDescription}
        />
        <TextInput
          style={styles.input}
          placeholder="Data (YYYY-MM-DD)"
          autoCapitalize="none"
          value={txnDate}
          onChangeText={setTxnDate}
        />

        <View style={styles.typeButtons}>
          <Pressable style={[styles.typeButton, styles.expenseButton]} onPress={() => handleAddTransaction("expense")}>
            <Text style={styles.typeButtonText}>Salvar saída</Text>
          </Pressable>
          <Pressable style={[styles.typeButton, styles.incomeButton]} onPress={() => handleAddTransaction("income")}>
            <Text style={styles.typeButtonText}>Salvar entrada</Text>
          </Pressable>
        </View>
      </View>

      <Text style={styles.sectionTitle}>Transações ({transactionCountLabel})</Text>
      {(data?.transactions ?? []).map((txn) => (
        <View key={`${txn.date}-${txn.description}-${txn.amount}`} style={styles.txnRow}>
          <View>
            <Text style={styles.txnDescription}>{txn.description}</Text>
            <Text style={styles.txnMeta}>{txn.category} • {txn.date}</Text>
          </View>
          <Text style={txn.type === "income" ? styles.incomeText : styles.expenseText}>
            {txn.type === "income" ? "+" : "-"} {money(txn.amount)}
          </Text>
        </View>
      ))}

      <Pressable style={styles.logoutButton} onPress={signOut}>
        <Text style={styles.logoutText}>Sair</Text>
      </Pressable>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20, gap: 14 },
  title: { fontSize: 28, fontWeight: "700", color: "#111827" },
  status: { color: "#4b5563" },
  filterRow: { flexDirection: "row", gap: 8 },
  input: {
    flex: 1,
    backgroundColor: "#fff",
    borderRadius: 10,
    borderWidth: 1,
    borderColor: "#d1d5db",
    paddingHorizontal: 12,
    paddingVertical: 10
  },
  actionButton: { backgroundColor: "#4f46e5", borderRadius: 10, paddingHorizontal: 14, justifyContent: "center" },
  actionButtonText: { color: "#fff", fontWeight: "700" },
  cardRow: { flexDirection: "row", gap: 12 },
  card: { flex: 1, borderRadius: 14, padding: 14 },
  balance: { backgroundColor: "#16a34a" },
  expense: { backgroundColor: "#dc2626" },
  cardLabel: { color: "#fff", fontWeight: "600" },
  cardValue: { color: "#fff", fontSize: 18, fontWeight: "700", marginTop: 6 },
  infoCard: { backgroundColor: "#fff", borderRadius: 12, borderWidth: 1, borderColor: "#e5e7eb", padding: 12, gap: 4 },
  infoLabel: { color: "#6b7280", fontSize: 12, textTransform: "uppercase" },
  infoValue: { color: "#111827", fontWeight: "600" },
  formCard: { backgroundColor: "#fff", borderRadius: 12, borderWidth: 1, borderColor: "#e5e7eb", padding: 12, gap: 8 },
  sectionTitle: { color: "#111827", fontWeight: "700" },
  typeButtons: { flexDirection: "row", gap: 8 },
  typeButton: { flex: 1, borderRadius: 10, paddingVertical: 10 },
  expenseButton: { backgroundColor: "#dc2626" },
  incomeButton: { backgroundColor: "#16a34a" },
  typeButtonText: { color: "#fff", textAlign: "center", fontWeight: "700" },
  txnRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: "#fff",
    borderRadius: 12,
    borderWidth: 1,
    borderColor: "#e5e7eb",
    padding: 12
  },
  txnDescription: { color: "#111827", fontWeight: "600" },
  txnMeta: { color: "#6b7280", fontSize: 12, marginTop: 2 },
  incomeText: { color: "#15803d", fontWeight: "700" },
  expenseText: { color: "#b91c1c", fontWeight: "700" },
  logoutButton: { marginTop: 8, backgroundColor: "#111827", borderRadius: 10, padding: 12 },
  logoutText: { color: "#fff", textAlign: "center", fontWeight: "600" }
});
