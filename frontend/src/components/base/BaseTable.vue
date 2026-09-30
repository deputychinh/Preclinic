<script setup lang="ts">
export interface TableColumn {
  key: string
  label: string
}

defineProps<{
  columns: TableColumn[]
  rows: Record<string, unknown>[]
  loading?: boolean
  emptyMessage?: string
}>()

defineSlots<{
  actions?: (props: { row: Record<string, unknown> }) => unknown
}>()
</script>

<template>
  <div class="overflow-x-auto rounded-2xl bg-white shadow-sm">
    <table class="w-full text-left text-sm">
      <thead>
        <tr class="bg-bg-soft text-xs font-semibold uppercase tracking-wide text-text-muted">
          <th
            v-for="col in columns"
            :key="col.key"
            class="px-4 py-3"
          >
            {{ col.label }}
          </th>
          <th
            v-if="$slots.actions"
            class="px-4 py-3 text-right"
          >
            Actions
          </th>
        </tr>
      </thead>
      <tbody class="divide-y divide-border">
        <tr v-if="loading">
          <td
            :colspan="columns.length + ($slots.actions ? 1 : 0)"
            class="px-4 py-6 text-center text-text-muted"
          >
            Loading…
          </td>
        </tr>
        <tr v-else-if="!rows.length">
          <td
            :colspan="columns.length + ($slots.actions ? 1 : 0)"
            class="px-4 py-6 text-center text-text-muted"
          >
            {{ emptyMessage ?? 'No data' }}
          </td>
        </tr>
        <tr
          v-for="(row, index) in rows"
          v-else
          :key="index"
          class="hover:bg-bg-soft"
        >
          <td
            v-for="col in columns"
            :key="col.key"
            class="px-4 py-3 text-text"
          >
            {{ row[col.key] }}
          </td>
          <td
            v-if="$slots.actions"
            class="px-4 py-3 text-right"
          >
            <slot
              name="actions"
              :row="row"
            />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
