import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useChatStore } from '../stores/chatStore'

const ELEVATOR_TEXT = `Manual Operacional e de Segurança – Elevador Manual de Carga (Modelo MC-70)
Edição Revisada – 1978
Departamento de Engenharia Mecânica – Fábrica Industrial Metzger & Filhos

1. Finalidade do Equipamento
O Elevador Manual de Carga Modelo MC-70 foi projetado para transporte vertical de materiais em pequenos depósitos, oficinas, mercados e fábricas de baixa escala. É indicado para cargas entre 25 kg e 180 kg, operado exclusivamente por acionamento manual através de manivela e sistema de guincho mecânico.
Este equipamento não é destinado ao transporte de pessoas em hipótese alguma.

2. Princípio de Funcionamento
O MC-70 funciona por meio de um conjunto de:
- Guincho de tambor metálico, acionado manualmente por uma manivela de 42 cm.
- Cabo de aço trançado de 6 mm, com resistência de ruptura de 580 kgf.
- Embreagem de fricção, responsável por controlar descidas.
- Trava de segurança dentada, que impede retorno involuntário da carga.
- Guia lateral de madeira tratada ou metal, onde a cabine se desloca verticalmente.

3. Capacidade e Limites Operacionais
3.1 Peso Máximo
- Capacidade nominal: 120 kg
- Capacidade máxima absoluta: 180 kg
O valor máximo deve ser utilizado apenas em situações excepcionais.

3.2 Velocidade Recomendada
- Elevação: 4 a 6 m/min
- Descida: controlada pela embreagem

4. Procedimentos de Operação
4.1 Elevação
1. Posicione a cabine no pavimento inferior.
2. Verifique se a trava dentada está engatada.
3. Centralize a carga na cabine.
4. Execute duas voltas de teste na manivela.
5. Gire no sentido horário.
6. Nunca solte a manivela abruptamente.

4.2 Descida
1. Desengate a trava dentada.
2. Acione a embreagem gradualmente.
3. Gire a manivela no sentido anti-horário.
4. Controle a velocidade pela embreagem.
5. Reengate a trava ao final.

5. Travamento e Segurança
5.1 Trava Dentada Automática
- Engata durante a subida.
- Deve produzir som metálico a cada dente.
- Se silenciosa, há risco de quebra da mola.

5.2 Freio de Emergência
- Atua se a descida exceder 1,8 m/s.
- Aquecimento > 60°C indica desgaste.

6. Inspeção Diária
Verificar: Integridade do cabo, Mandíbula da trava, Embreagem, Cabine e estrutura, Sons anormais.

7. Manutenção Preventiva
30 dias: Engraxar rolamentos, Lubrificar cabo, Testar freio de emergência
6 meses: Trocar mola da trava, Revisar lonas da embreagem, Apertar suportes do tambor
12 meses: Trocar o cabo de aço, Revisão estrutural completa

8. Superaquecimento da Embreagem
Ocorre por: Descidas longas, Controle inadequado, Carga excessiva, Lonas desgastadas.
Procedimento: Parar operação, Engatar trava dentada, Aguardar 10-15 min, Testar com carga leve.

9. Emergências
1. Travar equipamento com pino
2. Remover carga se seguro
3. Não liberar embreagem
4. Isolar área
5. Registrar ocorrência

10. Avisos Importantes
- Proibido transporte de pessoas
- Não usar cabos improvisados
- Operador não deve estar sob efeito de sedativos
- Uso obrigatório de luvas
- Não retirar proteções
- Afastar curiosos da área`

export function UploadPage() {
  const navigate = useNavigate()
  const { uploadText, hasKnowledge, checkKnowledge } = useChatStore()
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    checkKnowledge()
  }, [checkKnowledge])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!text.trim()) return
    setError(null)
    setLoading(true)
    try {
      await uploadText(text)
      setSuccess(true)
    } catch {
      setError('Erro ao enviar o texto. Tente novamente.')
    } finally {
      setLoading(false)
    }
  }

  const loadExample = () => {
    setText(ELEVATOR_TEXT)
  }

  return (
    <div className="stack">
      <div>
        <h1 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.25rem' }}>
          Texto Base
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
          Cole o texto que a IA usará para responder perguntas. Apenas informações deste texto serão usadas.
        </p>
      </div>

      {hasKnowledge && !success && (
        <div className="feedback-banner feedback-success">
          Texto carregado anteriormente. Você pode substituí-lo ou ir direto para as perguntas.
        </div>
      )}

      {success && (
        <div className="feedback-banner feedback-success">
          Texto enviado com sucesso!
        </div>
      )}

      {error && <div className="feedback-banner feedback-error">{error}</div>}

      <form className="stack stack-tight" onSubmit={handleSubmit}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <label className="field-label">Texto</label>
          <button type="button" className="button button-secondary" onClick={loadExample}
            style={{ fontSize: '0.8rem', padding: '0.2rem 0.6rem' }}>
            Carregar texto do elevador
          </button>
        </div>
        <textarea
          className="input"
          rows={14}
          value={text}
          onChange={e => setText(e.target.value)}
          placeholder="Cole o texto aqui..."
          style={{ resize: 'vertical', fontFamily: 'inherit', fontSize: '0.875rem', lineHeight: 1.6 }}
        />
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            {text.length.toLocaleString('pt-BR')} caracteres
          </span>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            {(hasKnowledge || success) && (
              <button type="button" className="button button-secondary" onClick={() => navigate('/chat')}>
                Ir para perguntas →
              </button>
            )}
            <button className="button" type="submit" disabled={loading || !text.trim()}>
              {loading ? 'Enviando...' : 'Enviar texto para a IA'}
            </button>
          </div>
        </div>
      </form>
    </div>
  )
}
