// One-time Chart.js registration. Imported once by main.ts so every chart component can assume
// the pieces it needs are already registered — no per-component `Chart.register(...)` calls.
import {
  BarElement,
  CategoryScale,
  Chart,
  Legend,
  LinearScale,
  Tooltip,
} from 'chart.js'

Chart.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend)
