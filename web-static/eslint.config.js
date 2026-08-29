import js from "@eslint/js";
import globals from "globals";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";
import tseslint from "typescript-eslint";
import importPlugin from "eslint-plugin-import";

export default tseslint.config(
  { ignores: ["dist", "src/devtools/**"] },
  {
    extends: [js.configs.recommended, ...tseslint.configs.recommended],
    files: ["**/*.{ts,tsx}"],
    languageOptions: {
      ecmaVersion: 2022,
      globals: globals.browser,
    },
    plugins: {
      "react-hooks": reactHooks,
      "react-refresh": reactRefresh,
      import: importPlugin,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      ...importPlugin.configs.recommended.rules,
      ...importPlugin.configs.typescript.rules,
      "prefer-const": "off",
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "error",
      "@typescript-eslint/no-unused-vars": "off",
      "@typescript-eslint/no-explicit-any": "off",
      "react-refresh/only-export-components": [
        "error",
        { allowConstantExport: true },
      ],
      "import/named": "error",
      "import/default": "error",
      "import/no-unresolved": [
        "error",
        {
          ignore: ["cloudflare:workers", "agents"],
        },
      ],
      "no-restricted-syntax": [
        "error",
        {
          selector:
            ":function[id.name=/^[A-Z]/] CallExpression[callee.name=/^set[A-Z]/]:not(ArrowFunctionExpression CallExpression, FunctionExpression CallExpression)",
          message:
            "State setters should not be called directly in the component's render body. This will cause an infinite render loop. Use useEffect or an event handler instead.",
        },
        {
          selector:
            "CallExpression[callee.name=/^set[A-Z]/] > :function[parent.callee.name='useMemo'], CallExpression[callee.name=/^set[A-Z]/] > :function[parent.callee.name='useCallback']",
          message:
            "State setters should not be called inside useMemo or useCallback. These hooks are for memoization, not for side effects.",
        },
      ],
    },
    settings: {
      "import/resolver": {
        typescript: {
          project: "./tsconfig.app.json",
        },
        node: true,
      },
    },
  },
  {
    // disable rules that the upstream shadcn templates haven't caught up to (react-hooks 7.x).
    files: ["src/components/ui/**/*.{ts,tsx}", "src/hooks/use-mobile.tsx"],
    rules: {
      "react-refresh/only-export-components": "off",
      "react-hooks/set-state-in-effect": "off",
      "react-hooks/purity": "off",
    },
  },
);
