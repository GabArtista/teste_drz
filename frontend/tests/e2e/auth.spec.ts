import { test, expect } from '@playwright/test'

test.describe('Auth flow', () => {
  test('shows login page by default', async ({ page }) => {
    await page.goto('/')
    await expect(page).toHaveURL(/\/login/)
    await expect(page.getByRole('heading', { name: 'Entrar' })).toBeVisible()
  })

  test('navigates to register page', async ({ page }) => {
    await page.goto('/login')
    await page.getByRole('link', { name: 'Cadastre-se' }).click()
    await expect(page).toHaveURL(/\/register/)
    await expect(page.getByRole('heading', { name: 'Criar conta' })).toBeVisible()
  })

  test('register then login flow', async ({ page }) => {
    const email = `e2e_${Date.now()}@test.com`
    await page.goto('/register')
    await page.getByLabel('Nome').fill('Teste E2E')
    await page.getByLabel('E-mail').fill(email)
    await page.getByLabel(/Senha/).fill('senha123')
    await page.getByRole('button', { name: 'Criar conta' }).click()
    await expect(page).toHaveURL(/\/upload/, { timeout: 10000 })
    await expect(page.getByRole('heading', { name: 'Texto Base' })).toBeVisible()
  })

  test('shows error on invalid login', async ({ page }) => {
    await page.goto('/login')
    await page.getByLabel('E-mail').fill('naoexiste@test.com')
    await page.getByLabel('Senha').fill('senhaerrada')
    await page.getByRole('button', { name: 'Entrar' }).click()
    await expect(page.locator('.feedback-banner')).toBeVisible({ timeout: 8000 })
  })
})
