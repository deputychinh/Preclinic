<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import BaseButton from '@/components/base/BaseButton.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import { useAuthStore } from '@/stores/auth.store'

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const auth = useAuthStore()
const router = useRouter()

async function onSubmit() {
  loading.value = true
  error.value = ''
  try {
    await auth.login(email.value, password.value)
    router.push({ name: 'dashboard' })
  } catch {
    error.value = 'Invalid email or password.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="flex min-h-screen items-center justify-center bg-secondary px-4">
    <form
      class="flex w-full max-w-[360px] flex-col gap-4 rounded-2xl bg-white p-8 shadow-lg"
      @submit.prevent="onSubmit"
    >
      <h1 class="mb-2 text-2xl font-bold text-primary">
        CarePath
      </h1>
      <BaseInput
        v-model="email"
        label="Email"
        type="email"
        required
        autocomplete="username"
      />
      <BaseInput
        v-model="password"
        label="Password"
        type="password"
        required
        autocomplete="current-password"
      />
      <p
        v-if="error"
        class="m-0 text-sm text-danger"
        role="alert"
      >
        {{ error }}
      </p>
      <BaseButton
        type="submit"
        :disabled="loading"
      >
        {{ loading ? 'Signing in…' : 'Sign in' }}
      </BaseButton>
    </form>
  </div>
</template>
