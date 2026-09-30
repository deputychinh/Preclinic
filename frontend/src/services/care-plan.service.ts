import { API_ENDPOINTS } from '@/constants/api'
import { http } from '@/services/http'

export interface CarePlanTask {
  id: number
  description: string
  dueDate: string | null
  completedAt: string | null
}

export interface CarePlan {
  id: number
  patient: number
  title: string
  goal: string
  tasks: CarePlanTask[]
}

function mapTask(raw: any): CarePlanTask {
  return { id: raw.id, description: raw.description, dueDate: raw.due_date, completedAt: raw.completed_at }
}

function mapCarePlan(raw: any): CarePlan {
  return {
    id: raw.id,
    patient: raw.patient,
    title: raw.title,
    goal: raw.goal,
    tasks: raw.tasks.map(mapTask),
  }
}

export async function getCarePlan(id: number | string): Promise<CarePlan> {
  const response = await http.get(`${API_ENDPOINTS.carePlans}/${id}`)
  return mapCarePlan(response.data.data)
}

export async function listCarePlansForPatient(patientId: number | string): Promise<CarePlan[]> {
  const response = await http.get(API_ENDPOINTS.carePlans, { params: { patient_id: patientId } })
  return response.data.data.map(mapCarePlan)
}
