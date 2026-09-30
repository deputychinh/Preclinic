<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import BaseCard from '@/components/base/BaseCard.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import { getCarePlan, type CarePlan } from '@/services/care-plan.service'

const route = useRoute()
const plan = ref<CarePlan | null>(null)
const error = ref('')
const loading = ref(true)

onMounted(async () => {
  try {
    plan.value = await getCarePlan(route.params.id as string)
  } catch {
    error.value = 'Could not load this care plan.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <PageHeader :title="plan ? plan.title : 'Care plan'" />
    <p v-if="loading">
      Loading…
    </p>
    <p
      v-else-if="error"
      role="alert"
      class="text-danger"
    >
      {{ error }}
    </p>
    <BaseCard v-else-if="plan">
      <p class="text-text-muted">
        {{ plan.goal || 'No goal recorded.' }}
      </p>
      <h2 class="text-base font-bold text-secondary">
        Tasks
      </h2>
      <ul
        v-if="plan.tasks.length"
        class="list-disc pl-4"
      >
        <li
          v-for="task in plan.tasks"
          :key="task.id"
        >
          {{ task.description }}
          <span v-if="task.dueDate"> — due {{ task.dueDate }}</span>
          <span
            v-if="task.completedAt"
            class="font-semibold text-success"
          > (done)</span>
        </li>
      </ul>
      <p v-else>
        No tasks yet.
      </p>
    </BaseCard>
  </div>
</template>
