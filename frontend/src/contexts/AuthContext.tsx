import React, { createContext, useContext, useState, useEffect } from 'react';
import { User } from '../types';
import { authApi } from '../api/endpoints';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (formData: FormData) => Promise<void>;
  register: (data: { email: string; password: string; full_name: string; preferred_currency?: string }) => Promise<void>;
  logout: () => void;
  refreshProfile: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const refreshProfile = async () => {
    try {
      const res = await authApi.getProfile();
      setUser(res.data);
    } catch {
      // Ignored
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      authApi
        .getProfile()
        .then((res) => setUser(res.data))
        .catch(() => {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
        })
        .finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = async (formData: FormData) => {
    const res = await authApi.login(formData);
    const { access_token, refresh_token } = res.data;
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    const profileRes = await authApi.getProfile();
    setUser(profileRes.data);
  };

  const register = async (data: { email: string; password: string; full_name: string; preferred_currency?: string }) => {
    await authApi.register(data);
    const loginData = new FormData();
    loginData.append('username', data.email);
    loginData.append('password', data.password);
    await login(loginData);
  };

  const logout = () => {
    authApi.logout().catch(() => {});
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
    window.location.href = '/login';
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, register, logout, refreshProfile }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
