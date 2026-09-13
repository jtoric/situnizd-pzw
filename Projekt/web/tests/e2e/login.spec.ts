import { test, expect } from '@playwright/test'

test.beforeEach(async ({ page }) => {
  // Počisti lokalni storage da ne bi ostao token od prethodnog testa
  await page.goto('/prijava')
  await page.evaluate(() => localStorage.clear())
  await page.reload()
})

test('club prijava preusmjerava na klub početnu', async ({ page }) => {
  await page.fill('[data-testid="korisnicko-ime"]', 'behemot')
  await page.fill('[data-testid="lozinka"]', 'klub123')
  await page.click('[data-testid="submit"]')

  await expect(page).toHaveURL('/klub/pocetna')
  await expect(page.getByText('Klub — Početna')).toBeVisible()
})

test('admin prijava preusmjerava na admin početnu', async ({ page }) => {
  await page.fill('[data-testid="korisnicko-ime"]', 'admin')
  await page.fill('[data-testid="lozinka"]', 'admin123')
  await page.click('[data-testid="submit"]')

  await expect(page).toHaveURL('/admin/pocetna')
})

test('pogrešna lozinka prikazuje grešku', async ({ page }) => {
  await page.fill('[data-testid="korisnicko-ime"]', 'behemot')
  await page.fill('[data-testid="lozinka"]', 'kriva-lozinka')
  await page.click('[data-testid="submit"]')

  await expect(page.locator('[data-testid="obavijest-greska"]')).toBeVisible()
  await expect(
    page.getByText('Pogrešno korisničko ime ili lozinka'),
  ).toBeVisible()
})

test('prijavljeni korisnik na /prijava se preusmjerava', async ({ page }) => {
  // Prijava
  await page.fill('[data-testid="korisnicko-ime"]', 'behemot')
  await page.fill('[data-testid="lozinka"]', 'klub123')
  await page.click('[data-testid="submit"]')
  await expect(page).toHaveURL('/klub/pocetna')

  // Pokušaj ručne navigacije na /prijava
  await page.goto('/prijava')
  await expect(page).toHaveURL('/klub/pocetna')
})
