import { onUnmounted, ref } from 'vue'

export function usePolling<T>(fetcher: () => Promise<T>, isDone: (value: T) => boolean, intervalMs: number, timeoutMs: number) {
  const result = ref<T | null>(null) as { value: T | null }
  const timedOut = ref(false)
  let timer: ReturnType<typeof setInterval> | undefined
  let elapsed = 0

  function start() {
    timer = setInterval(async () => {
      elapsed += intervalMs
      const value = await fetcher()
      result.value = value
      if (isDone(value) || elapsed >= timeoutMs) {
        stop()
        if (!isDone(value)) timedOut.value = true
      }
    }, intervalMs)
  }

  function stop() {
    if (timer) clearInterval(timer)
  }

  onUnmounted(stop)

  return { result, timedOut, start, stop }
}
