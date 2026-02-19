import * as SecureStore from "expo-secure-store";
import { createContext, PropsWithChildren, useContext, useEffect, useMemo, useState } from "react";

import { fetchHome, login as apiLogin, logout as apiLogout, register as apiRegister } from "./api";

type AuthContextType = {
  ready: boolean;
  signedIn: boolean;
  signIn: (email: string, password: string) => Promise<string | null>;
  signUp: (name: string, email: string, password: string) => Promise<string | null>;
  signOut: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType | null>(null);
const KEY = "ia_finance_mobile_signed_in";

export function AuthProvider({ children }: PropsWithChildren) {
  const [ready, setReady] = useState(false);
  const [signedIn, setSignedIn] = useState(false);

  useEffect(() => {
    SecureStore.getItemAsync(KEY).then((value) => {
      setSignedIn(value === "1");
      setReady(true);
    });
  }, []);

  const signIn = async (email: string, password: string): Promise<string | null> => {
    const response = await apiLogin({ email, password });
    if (!response.ok) {
      return "Falha no login. Verifique e-mail e senha.";
    }

    await SecureStore.setItemAsync(KEY, "1");
    setSignedIn(true);
    return null;
  };

  const signUp = async (name: string, email: string, password: string): Promise<string | null> => {
    const response = await apiRegister({ name, email, password });
    if (!response.ok) {
      return "Não foi possível criar conta. Confira os dados.";
    }

    await SecureStore.setItemAsync(KEY, "1");
    setSignedIn(true);
    return null;
  };

  const signOut = async () => {
    await apiLogout();
    await SecureStore.deleteItemAsync(KEY);
    setSignedIn(false);
  };

  useEffect(() => {
    if (!signedIn) return;
    fetchHome().then((html) => {
      if (html.includes("Entrar") && html.includes("Criar conta")) {
        SecureStore.deleteItemAsync(KEY);
        setSignedIn(false);
      }
    });
  }, [signedIn]);

  const value = useMemo(
    () => ({ ready, signedIn, signIn, signUp, signOut }),
    [ready, signedIn]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return ctx;
}
