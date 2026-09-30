// DRF's CursorPagination returns `next`/`previous` as full absolute URLs (e.g.
// "http://host/api/v1/patients?cursor=cD0yMDI2..."), not bare cursor tokens. The frontend only
// ever needs the `cursor` query param value to pass back into the next request.
export function extractCursor(url: string | null): string | undefined {
  if (!url) return undefined
  try {
    return new URL(url).searchParams.get('cursor') ?? undefined
  } catch {
    return undefined
  }
}
