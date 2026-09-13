export function uCsv(redovi: Record<string, unknown>[], stupci: string[]): string {
  const zaglavlje = stupci.join(',')
  const tijelo = redovi
    .map((r) =>
      stupci
        .map((s) => {
          const v = r[s] ?? ''
          const str = String(v)
          return str.includes(',') || str.includes('"') || str.includes('\n')
            ? `"${str.replace(/"/g, '""')}"`
            : str
        })
        .join(','),
    )
    .join('\n')
  return `${zaglavlje}\n${tijelo}`
}

export function preuzmiCsv(naziv: string, sadrzaj: string): void {
  const blob = new Blob([sadrzaj], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = naziv
  a.click()
  URL.revokeObjectURL(url)
}
