import { test, expect } from '@playwright/test'

async function registerAndLogin(page: any) {
  const email = `upload_${Date.now()}@test.com`
  await page.goto('/register')
  await page.getByLabel('Nome').fill('Upload Test')
  await page.getByLabel('E-mail').fill(email)
  await page.getByLabel(/Senha/).fill('senha123')
  await page.getByRole('button', { name: 'Criar conta' }).click()
  await page.waitForURL(/\/upload/, { timeout: 10000 })
  return email
}

test.describe('Upload flow', () => {
  test('upload page is accessible after login', async ({ page }) => {
    await registerAndLogin(page)
    await expect(page.getByRole('heading', { name: 'Texto Base' })).toBeVisible()
    await expect(page.getByText(/Cole o texto/)).toBeVisible()
  })

  test('can load elevator text and submit', async ({ page }) => {
    await registerAndLogin(page)
    await page.getByRole('button', { name: 'Carregar texto do elevador' }).click()
    await expect(page.locator('textarea')).not.toBeEmpty()
    await page.getByRole('button', { name: 'Enviar texto para a IA' }).click()
    await expect(page.getByText('Texto enviado com sucesso')).toBeVisible({ timeout: 10000 })
    await expect(page.getByRole('button', { name: /Ir para perguntas/ })).toBeVisible()
  })
})
