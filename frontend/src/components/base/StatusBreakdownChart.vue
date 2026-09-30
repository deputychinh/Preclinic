<script setup lang="ts">
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'

export interface BreakdownRow {
  label: string
  count: number
}

const props = defineProps<{
  data: BreakdownRow[]
  colorMap: Record<string, string>
  labelMap?: Record<string, string>
}>()

const chartData = computed(() => ({
  labels: props.data.map((row) => props.labelMap?.[row.label] ?? row.label),
  datasets: [
    {
      data: props.data.map((row) => row.count),
      backgroundColor: props.data.map((row) => props.colorMap[row.label] ?? '#6b7680'),
      borderRadius: 4,
      maxBarThickness: 28,
    },
  ],
}))

const chartOptions = {
  indexAxis: 'y' as const,
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    x: { beginAtZero: true, ticks: { precision: 0 } },
  },
}
</script>

<template>
  <div class="flex h-56 items-center justify-center">
    <Bar
      v-if="data.length"
      :data="chartData"
      :options="chartOptions"
    />
    <p
      v-else
      class="text-sm text-text-muted"
    >
      No data yet.
    </p>
  </div>
</template>
