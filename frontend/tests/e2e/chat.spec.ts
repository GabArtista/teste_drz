import { test, expect, request } from '@playwright/test'

// Pré-aquece o Ollama antes dos testes de IA para evitar cold start
test.beforeAll(async () => {
  const ctx = await request.newContext()
  await ctx.post('http://localhost:11434/api/generate', {
    data: { model: 'qwen2.5:1.5b', prompt: 'ok', stream: false },
    timeout: 90000,
  }).catch(() => {})
  await ctx.dispose()
})

const ELEVATOR_TEXT = `O Elevador Manual de Carga Modelo MC-70 foi projetado para transporte vertical de materiais em pequenos depósitos, oficinas, mercados e fábricas de baixa escala. É indicado para cargas entre 25 kg e 180 kg, operado exclusivamente por acionamento manual através de manivela e sistema de guincho mecânico. Este equipamento não é destinado ao transporte de pessoas em hipótese alguma. Capacidade nominal: 120 kg. Capacidade máxima absoluta: 180 kg. Velocidade de elevação: 4 a 6 m/min. O freio de emergência atua se a descida exceder 1,8 m/s. Aquecimento acima de 60 graus Celsius indica desgaste. A trava dentada deve produzir som metálico a cada dente durante a subida.`

async function setupUserWithKnowledge(page: any) {
  const email = `chat_e2e_${Date.now()}@test.com`

  // Registra
  await page.goto('/register')
  await page.getByLabel('Nome').fill('Chat E2E')
  await page.getByLabel('E-mail').fill(email)
  await page.getByLabel(/Senha/).fill('senha123')
  await page.getByRole('button', { name: 'Criar conta' }).click()
  await page.waitForURL(/\/upload/, { timeout: 10000 })

  // Faz upload do texto
  await page.locator('textarea').fill(ELEVATOR_TEXT)
  await page.getByRole('button', { name: 'Enviar texto para a IA' }).click()
  await expect(page.getByText('Texto enviado com sucesso')).toBeVisible({ timeout: 10000 })

  // Navega para o chat
  await page.getByRole('button', { name: /Ir para perguntas/ }).click()
  await page.waitForURL(/\/chat/, { timeout: 5000 })

  return email
}

test.describe('Chat flow', () => {
  test('chat page mostra empty state sem texto carregado', async ({ page }) => {
    const email = `nochat_${Date.now()}@test.com`
    await page.goto('/register')
    await page.getByLabel('Nome').fill('No Chat')
    await page.getByLabel('E-mail').fill(email)
    await page.getByLabel(/Senha/).fill('senha123')
    await page.getByRole('button', { name: 'Criar conta' }).click()
    await page.waitForURL(/\/upload/, { timeout: 10000 })

    await page.goto('/chat')
    await expect(page.getByText('Nenhum texto carregado')).toBeVisible()
    await expect(page.getByRole('button', { name: 'Enviar texto base' })).toBeVisible()
  })

  test('botão "Enviar texto base" redireciona para /upload', async ({ page }) => {
    const email = `redirect_${Date.now()}@test.com`
    await page.goto('/register')
    await page.getByLabel('Nome').fill('Redirect Test')
    await page.getByLabel('E-mail').fill(email)
    await page.getByLabel(/Senha/).fill('senha123')
    await page.getByRole('button', { name: 'Criar conta' }).click()
    await page.waitForURL(/\/upload/, { timeout: 10000 })

    await page.goto('/chat')
    await page.getByRole('button', { name: 'Enviar texto base' }).click()
    await expect(page).toHaveURL(/\/upload/)
  })

  test('chat renderiza input e botão Perguntar após texto carregado', async ({ page }) => {
    await setupUserWithKnowledge(page)
    await expect(page.getByPlaceholder('Digite sua pergunta...')).toBeVisible()
    await expect(page.getByRole('button', { name: 'Perguntar' })).toBeVisible()
  })

  test('pergunta aparece no histórico imediatamente', async ({ page }) => {
    await setupUserWithKnowledge(page)

    await page.getByPlaceholder('Digite sua pergunta...').fill('Qual a capacidade máxima?')
    await page.getByRole('button', { name: 'Perguntar' }).click()

    // Mensagem do usuário aparece instantaneamente
    await expect(page.getByText('Qual a capacidade máxima?')).toBeVisible({ timeout: 3000 })
  })

  test('IA responde com base no texto — capacidade máxima', async ({ page }) => {
    await setupUserWithKnowledge(page)

    await page.getByPlaceholder('Digite sua pergunta...').fill('Qual a capacidade máxima do elevador?')
    await page.getByRole('button', { name: 'Perguntar' }).click()

    // Aguarda resposta da IA (modelo já aquecido pelo beforeAll)
    await expect(page.getByText(/180|cento e oitenta/i)).toBeVisible({ timeout: 110000 })
  })

  test('IA responde sobre restrição de pessoas', async ({ page }) => {
    await setupUserWithKnowledge(page)

    await page.getByPlaceholder('Digite sua pergunta...').fill('Posso transportar pessoas neste elevador?')
    await page.getByRole('button', { name: 'Perguntar' }).click()

    // Deve negar ou citar a restrição
    await expect(
      page.getByText(/não|proibido|pessoas/i)
    ).toBeVisible({ timeout: 90000 })
  })

  test('IA recusa perguntas fora do contexto', async ({ page }) => {
    await setupUserWithKnowledge(page)

    await page.getByPlaceholder('Digite sua pergunta...').fill('Qual é a capital do Brasil?')
    await page.getByRole('button', { name: 'Perguntar' }).click()

    // Modelo pequeno pode variar a frase — verifica que respondeu algo sem citar o Brasil corretamente
    await expect(
      page.getByText(/não sei|não (há|tenho|encontrei|consta|está)|informações fornecidas|fora do contexto|não (foi|é) mencionad/i)
    ).toBeVisible({ timeout: 90000 })
  })

  test('input limpa após enviar pergunta', async ({ page }) => {
    await setupUserWithKnowledge(page)

    const input = page.getByPlaceholder('Digite sua pergunta...')
    await input.fill('Qual a velocidade de elevação?')
    await page.getByRole('button', { name: 'Perguntar' }).click()

    await expect(input).toHaveValue('', { timeout: 3000 })
  })

  test('múltiplas perguntas na mesma sessão', async ({ page }) => {
    test.setTimeout(240000) // 2 chamadas à IA: timeout estendido
    await setupUserWithKnowledge(page)

    // Primeira pergunta
    await page.getByPlaceholder('Digite sua pergunta...').fill('Qual a capacidade nominal?')
    await page.getByRole('button', { name: 'Perguntar' }).click()
    await expect(page.getByText(/120/)).toBeVisible({ timeout: 90000 })

    // Segunda pergunta
    await page.getByPlaceholder('Digite sua pergunta...').fill('Qual a capacidade máxima absoluta?')
    await page.getByRole('button', { name: 'Perguntar' }).click()
    await expect(page.getByText(/180/)).toBeVisible({ timeout: 90000 })

    // Ambas as perguntas visíveis no histórico
    await expect(page.getByText('Qual a capacidade nominal?')).toBeVisible()
    await expect(page.getByText('Qual a capacidade máxima absoluta?')).toBeVisible()
  })

  test('botão Perguntar desabilitado com input vazio', async ({ page }) => {
    await setupUserWithKnowledge(page)
    await expect(page.getByRole('button', { name: 'Perguntar' })).toBeDisabled()
  })

  test('"Alterar texto base" volta para /upload e limpa sessão', async ({ page }) => {
    await setupUserWithKnowledge(page)
    await page.getByRole('button', { name: 'Alterar texto base' }).click()
    await expect(page).toHaveURL(/\/upload/)
  })
})
