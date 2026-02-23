import AsyncStorage from "@react-native-async-storage/async-storage";
import { useEffect, useMemo, useState } from "react";
import { Appearance, Modal, Pressable, ScrollView, StyleSheet, Text, TextInput, View, useColorScheme } from "react-native";

type TransactionType = "income" | "expense";

type LocalTransaction = {
  id: string;
  amount: string;
  description: string;
  txn_date: string;
  type: TransactionType;
  category: string;
  created_at: number;
};

type ThemeMode = "light" | "dark" | "system";

type Palette = {
  bg: string;
  text: string;
  muted: string;
  card: string;
  border: string;
  yellow: string;
  purple: string;
  income: string;
  expense: string;
};

const STORAGE_TRANSACTIONS = "ia_finance_local_transactions";
const STORAGE_THEME = "ia_finance_theme_mode";

function money(value: number): string {
  return value.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

function monthLabel(period: string): string {
  if (!period) return "Todos";
  const [year, month] = period.split("-");
  if (!year || !month) return period;
  return `${month}/${year}`;
}

function categorize(description: string, type: TransactionType): string {
  if (type === "income") return "Entrada";

  const lower = description.toLowerCase();
  if (lower.includes("uber") || lower.includes("99") || lower.includes("ônibus")) return "Transporte";
  if (lower.includes("mercado") || lower.includes("ifood") || lower.includes("restaurante")) return "Alimentação";
  if (lower.includes("aluguel") || lower.includes("condomínio")) return "Moradia";
  return "Outros";
}

function getPalette(theme: ThemeMode, systemScheme: "light" | "dark" | null): Palette {
  const dark = theme === "dark" || (theme === "system" && systemScheme === "dark");
  if (dark) {
    return {
      bg: "#0f172a",
      text: "#f8fafc",
      muted: "#94a3b8",
      card: "#1e293b",
      border: "#334155",
      yellow: "#facc15",
      purple: "#a855f7",
      income: "#22c55e",
      expense: "#fb7185"
    };
  }

  return {
    bg: "#f8fafc",
    text: "#0f172a",
    muted: "#475569",
    card: "#ffffff",
    border: "#e2e8f0",
    yellow: "#facc15",
    purple: "#7e22ce",
    income: "#15803d",
    expense: "#be123c"
  };
}

export default function DashboardScreen() {
  const systemScheme = useColorScheme();
  const [themeMode, setThemeMode] = useState<ThemeMode>("system");
  const [settingsOpen, setSettingsOpen] = useState(false);

  const [period, setPeriod] = useState("");
  const [status, setStatus] = useState("");
  const [transactions, setTransactions] = useState<LocalTransaction[]>([]);

  const [amount, setAmount] = useState("");
  const [description, setDescription] = useState("");
  const [txnDate, setTxnDate] = useState(new Date().toISOString().slice(0, 10));

  const palette = getPalette(themeMode, systemScheme);

  useEffect(() => {
    AsyncStorage.getItem(STORAGE_THEME).then((saved) => {
      if (saved === "light" || saved === "dark" || saved === "system") {
        setThemeMode(saved);
      }
    });

    AsyncStorage.getItem(STORAGE_TRANSACTIONS).then((saved) => {
      if (!saved) return;
      try {
        const parsed = JSON.parse(saved) as LocalTransaction[];
        setTransactions(parsed);
      } catch {
        setStatus("Não foi possível carregar dados locais.");
      }
    });
  }, []);

  const saveTransactions = async (items: LocalTransaction[]) => {
    setTransactions(items);
    await AsyncStorage.setItem(STORAGE_TRANSACTIONS, JSON.stringify(items));
  };

  const filteredTransactions = useMemo(() => {
    const selected = period.trim();
    const base = selected
      ? transactions.filter((txn) => txn.txn_date.startsWith(selected))
      : transactions;

    return [...base].sort((a, b) => b.created_at - a.created_at);
  }, [transactions, period]);

  const totals = useMemo(() => {
    let income = 0;
    let expense = 0;

    for (const txn of filteredTransactions) {
      const parsed = Number(txn.amount);
      if (Number.isNaN(parsed)) continue;
      if (txn.type === "income") income += parsed;
      else expense += parsed;
    }

    return { income, expense, balance: income - expense };
  }, [filteredTransactions]);

  const hint = useMemo(() => {
    if (totals.expense === 0 && totals.income === 0) {
      return "Adicione sua primeira transação para receber dicas.";
    }
    if (totals.balance >= 0) {
      return "Boa! Você está mantendo saldo positivo neste período.";
    }
    return "Atenção: gastos acima das entradas. Revise despesas fixas.";
  }, [totals]);

  const handleAddTransaction = async (type: TransactionType) => {
    if (!amount || !description.trim() || !txnDate) {
      setStatus("Preencha valor, descrição e data.");
      return;
    }

    const parsedAmount = Number(amount.replace(",", "."));
    if (Number.isNaN(parsedAmount) || parsedAmount <= 0) {
      setStatus("Digite um valor válido.");
      return;
    }

    const next: LocalTransaction = {
      id: `${Date.now()}-${Math.random().toString(16).slice(2)}`,
      amount: String(parsedAmount),
      description: description.trim(),
      txn_date: txnDate,
      type,
      category: categorize(description, type),
      created_at: Date.now()
    };

    await saveTransactions([...transactions, next]);
    setAmount("");
    setDescription("");
    setStatus("");
  };

  const updateTheme = async (mode: ThemeMode) => {
    setThemeMode(mode);
    await AsyncStorage.setItem(STORAGE_THEME, mode);
  };

  return (
    <ScrollView contentContainerStyle={[styles.container, { backgroundColor: palette.bg }]}> 
      <View style={styles.headerRow}>
        <Text style={[styles.title, { color: palette.text }]}>IA Finance Mobile</Text>
        <Pressable onPress={() => setSettingsOpen(true)} style={[styles.settingsBtn, { borderColor: palette.border }]}> 
          <Text style={{ fontSize: 18 }}>⚙️</Text>
        </Pressable>
      </View>

      {status ? <Text style={[styles.status, { color: palette.expense }]}>{status}</Text> : null}

      <View style={styles.filterRow}>
        <TextInput
          style={[styles.input, { backgroundColor: palette.card, borderColor: palette.border, color: palette.text }]}
          placeholder="Filtrar mês (YYYY-MM)"
          placeholderTextColor={palette.muted}
          autoCapitalize="none"
          value={period}
          onChangeText={setPeriod}
        />
        <Pressable style={[styles.actionButton, { backgroundColor: palette.yellow }]} onPress={() => setPeriod(period.trim())}>
          <Text style={[styles.actionButtonText, { color: "#1f2937" }]}>Aplicar</Text>
        </Pressable>
      </View>

      <View style={styles.cardRow}>
        <View style={[styles.card, { backgroundColor: palette.purple }]}> 
          <Text style={styles.cardLabel}>Saldo</Text>
          <Text style={styles.cardValue}>{money(totals.balance)}</Text>
        </View>
        <View style={[styles.card, { backgroundColor: palette.yellow }]}> 
          <Text style={[styles.cardLabel, { color: "#1f2937" }]}>Gastos</Text>
          <Text style={[styles.cardValue, { color: "#1f2937" }]}>{money(totals.expense)}</Text>
        </View>
      </View>

      <View style={[styles.infoCard, { backgroundColor: palette.card, borderColor: palette.border }]}> 
        <Text style={[styles.infoLabel, { color: palette.muted }]}>Período</Text>
        <Text style={[styles.infoValue, { color: palette.text }]}>{monthLabel(period)}</Text>
        <Text style={[styles.infoLabel, { color: palette.muted }]}>Dica</Text>
        <Text style={[styles.infoValue, { color: palette.text }]}>{hint}</Text>
      </View>

      <View style={[styles.formCard, { backgroundColor: palette.card, borderColor: palette.border }]}> 
        <Text style={[styles.sectionTitle, { color: palette.text }]}>Nova transação</Text>
        <TextInput
          style={[styles.input, { backgroundColor: palette.bg, borderColor: palette.border, color: palette.text }]}
          placeholder="Valor (ex: 120.50)"
          placeholderTextColor={palette.muted}
          value={amount}
          onChangeText={setAmount}
          keyboardType="decimal-pad"
        />
        <TextInput
          style={[styles.input, { backgroundColor: palette.bg, borderColor: palette.border, color: palette.text }]}
          placeholder="Descrição"
          placeholderTextColor={palette.muted}
          value={description}
          onChangeText={setDescription}
        />
        <TextInput
          style={[styles.input, { backgroundColor: palette.bg, borderColor: palette.border, color: palette.text }]}
          placeholder="Data (YYYY-MM-DD)"
          placeholderTextColor={palette.muted}
          autoCapitalize="none"
          value={txnDate}
          onChangeText={setTxnDate}
        />

        <View style={styles.typeButtons}>
          <Pressable style={[styles.typeButton, { backgroundColor: palette.yellow }]} onPress={() => handleAddTransaction("expense")}> 
            <Text style={[styles.typeButtonText, { color: "#1f2937" }]}>Salvar saída</Text>
          </Pressable>
          <Pressable style={[styles.typeButton, { backgroundColor: palette.purple }]} onPress={() => handleAddTransaction("income")}> 
            <Text style={styles.typeButtonText}>Salvar entrada</Text>
          </Pressable>
        </View>
      </View>

      <Text style={[styles.sectionTitle, { color: palette.text }]}>Transações ({filteredTransactions.length})</Text>
      {filteredTransactions.map((txn) => (
        <View key={txn.id} style={[styles.txnRow, { backgroundColor: palette.card, borderColor: palette.border }]}> 
          <View>
            <Text style={[styles.txnDescription, { color: palette.text }]}>{txn.description}</Text>
            <Text style={[styles.txnMeta, { color: palette.muted }]}>{txn.category} • {txn.txn_date}</Text>
          </View>
          <Text style={{ color: txn.type === "income" ? palette.income : palette.expense, fontWeight: "700" }}>
            {txn.type === "income" ? "+" : "-"} {money(Number(txn.amount))}
          </Text>
        </View>
      ))}

      <Modal visible={settingsOpen} transparent animationType="fade" onRequestClose={() => setSettingsOpen(false)}>
        <View style={styles.modalBackdrop}>
          <View style={[styles.modalCard, { backgroundColor: palette.card, borderColor: palette.border }]}> 
            <Text style={[styles.modalTitle, { color: palette.text }]}>Configurações</Text>
            <Text style={[styles.modalText, { color: palette.muted }]}>Versão do app: 0.1.0</Text>

            <Pressable style={[styles.themeOption, { borderColor: palette.border }]} onPress={() => updateTheme("light")}> 
              <Text style={{ color: palette.text }}>Tema claro</Text>
            </Pressable>
            <Pressable style={[styles.themeOption, { borderColor: palette.border }]} onPress={() => updateTheme("dark")}> 
              <Text style={{ color: palette.text }}>Tema escuro</Text>
            </Pressable>
            <Pressable style={[styles.themeOption, { borderColor: palette.border }]} onPress={() => updateTheme("system")}> 
              <Text style={{ color: palette.text }}>Tema do dispositivo</Text>
            </Pressable>

            <Pressable style={[styles.closeBtn, { backgroundColor: palette.purple }]} onPress={() => setSettingsOpen(false)}>
              <Text style={styles.typeButtonText}>Fechar</Text>
            </Pressable>
          </View>
        </View>
      </Modal>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20, gap: 14, flexGrow: 1 },
  headerRow: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  title: { fontSize: 28, fontWeight: "700" },
  settingsBtn: { borderWidth: 1, borderRadius: 10, paddingHorizontal: 10, paddingVertical: 6 },
  status: { fontWeight: "600" },
  filterRow: { flexDirection: "row", gap: 8 },
  input: {
    flex: 1,
    borderRadius: 10,
    borderWidth: 1,
    paddingHorizontal: 12,
    paddingVertical: 10
  },
  actionButton: { borderRadius: 10, paddingHorizontal: 14, justifyContent: "center" },
  actionButtonText: { fontWeight: "700" },
  cardRow: { flexDirection: "row", gap: 12 },
  card: { flex: 1, borderRadius: 14, padding: 14 },
  cardLabel: { color: "#fff", fontWeight: "600" },
  cardValue: { color: "#fff", fontSize: 18, fontWeight: "700", marginTop: 6 },
  infoCard: { borderRadius: 12, borderWidth: 1, padding: 12, gap: 4 },
  infoLabel: { fontSize: 12, textTransform: "uppercase" },
  infoValue: { fontWeight: "600" },
  formCard: { borderRadius: 12, borderWidth: 1, padding: 12, gap: 8 },
  sectionTitle: { fontWeight: "700" },
  typeButtons: { flexDirection: "row", gap: 8 },
  typeButton: { flex: 1, borderRadius: 10, paddingVertical: 10 },
  typeButtonText: { color: "#fff", textAlign: "center", fontWeight: "700" },
  txnRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    borderRadius: 12,
    borderWidth: 1,
    padding: 12
  },
  txnDescription: { fontWeight: "600" },
  txnMeta: { fontSize: 12, marginTop: 2 },
  modalBackdrop: { flex: 1, backgroundColor: "rgba(0,0,0,0.4)", justifyContent: "center", padding: 20 },
  modalCard: { borderRadius: 12, borderWidth: 1, padding: 16, gap: 10 },
  modalTitle: { fontSize: 18, fontWeight: "700" },
  modalText: { fontSize: 13 },
  themeOption: { borderWidth: 1, borderRadius: 10, padding: 10 },
  closeBtn: { marginTop: 6, borderRadius: 10, padding: 10 }
});
