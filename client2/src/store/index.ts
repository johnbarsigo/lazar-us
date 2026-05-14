import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User } from '../types';

interface AuthStore {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  setAuth: (user: User, token: string) => void;
  logout: () => void;
  setLoading: (loading: boolean) => void;
  isAuthenticated: () => boolean;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isLoading: false,
      
      setAuth: (user: User, token: string) => {
        localStorage.setItem('token', token);
        set({ user, token });
      },
      
      logout: () => {
        localStorage.removeItem('token');
        set({ user: null, token: null });
      },
      
      setLoading: (loading: boolean) => set({ isLoading: loading }),
      
      isAuthenticated: () => get().token !== null,
    }),
    {
      name: 'auth-store',
    }
  )
);

interface UIStore {
  darkMode: boolean;
  sidebarOpen: boolean;
  toggleDarkMode: () => void;
  toggleSidebar: () => void;
}

export const useUIStore = create<UIStore>()(
  persist(
    (set) => ({
      darkMode: localStorage.getItem('darkMode') === 'true',
      sidebarOpen: true,
      
      toggleDarkMode: () => {
        set((state) => {
          const newDarkMode = !state.darkMode;
          localStorage.setItem('darkMode', String(newDarkMode));
          if (newDarkMode) {
            document.documentElement.classList.add('dark');
          } else {
            document.documentElement.classList.remove('dark');
          }
          return { darkMode: newDarkMode };
        });
      },
      
      toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
    }),
    {
      name: 'ui-store',
    }
  )
);
