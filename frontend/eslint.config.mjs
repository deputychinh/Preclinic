// @ts-check
import js from '@eslint/js'
import eslintPluginVue from 'eslint-plugin-vue'
import tseslint from 'typescript-eslint'

export default tseslint.config(
  { ignores: ['dist/**', 'src/types/api.generated.ts'] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  ...eslintPluginVue.configs['flat/recommended'],
  {
    files: ['**/*.vue'],
    languageOptions: { parserOptions: { parser: tseslint.parser } },
  },
  {
    rules: {
      'no-console': ['error', { allow: ['warn', 'error'] }],
      '@typescript-eslint/no-explicit-any': 'error',
      'vue/no-v-html': 'error',
      'vue/multi-word-component-names': 'off',
    },
  },
  {
    // The service layer maps raw (snake_case, untyped-until-generated) DRF JSON into typed
    // camelCase view models — `any` is the deliberate boundary for that one mapping step, per
    // docs/plan.md §7.4's Adapter/Mapper pattern.
    files: ['src/services/**/*.ts'],
    rules: { '@typescript-eslint/no-explicit-any': 'off' },
  },
)
