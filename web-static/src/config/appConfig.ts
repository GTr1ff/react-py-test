export const appConfig = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api',
  appTitle: import.meta.env.VITE_APP_TITLE ?? 'react-py',
  useMocks: (import.meta.env.VITE_USE_MOCKS ?? 'false') === 'true',
  apiNamingConvention: import.meta.env.VITE_API_NAMING_CONVENTION ?? 'snake_case',
  debugMode: (import.meta.env.VITE_DEBUG_MODE ?? 'false') === 'true',
} as const;