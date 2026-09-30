import { API_ENDPOINTS } from '@/constants/api'
import { http } from '@/services/http'
import type { LabImportJob } from '@/types/models'

function mapJob(raw: any): LabImportJob {
  return {
    id: raw.id,
    status: raw.status,
    totalRows: raw.total_rows,
    importedRows: raw.imported_rows,
    errorReport: raw.error_report,
    createdAt: raw.created_at,
  }
}

export async function uploadLabImport(file: File): Promise<{ job: LabImportJob; alreadyImported: boolean }> {
  const form = new FormData()
  form.append('file', file)
  const response = await http.post(API_ENDPOINTS.labImports, form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return { job: mapJob(response.data.data), alreadyImported: response.data.data.already_imported }
}

export async function getLabImportJob(id: number | string): Promise<LabImportJob> {
  const response = await http.get(API_ENDPOINTS.labImport(id))
  return mapJob(response.data.data)
}
