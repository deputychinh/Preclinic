import { computed, type Ref } from 'vue'

export function useStatusColor<T extends string>(status: Ref<T>, colorMap: Record<T, string>) {
  return computed(() => colorMap[status.value])
}
