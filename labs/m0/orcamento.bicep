// 0.1 — Alerta de orçamento na subscrição (avisa a 50%, 80% e 100% de 20 EUR/mês)
targetScope = 'subscription'
param email string
param inicio string = '2026-11-01'
resource orcamento 'Microsoft.Consumption/budgets@2023-11-01' = {
  name: 'curso-sentinel-orcamento'
  properties: {
    category: 'Cost'
    amount: 20
    timeGrain: 'Monthly'
    timePeriod: { startDate: inicio }
    notifications: {
      aviso50: { enabled: true, operator: 'GreaterThan', threshold: 50, thresholdType: 'Actual', contactEmails: [ email ] }
      aviso80: { enabled: true, operator: 'GreaterThan', threshold: 80, thresholdType: 'Actual', contactEmails: [ email ] }
      previsao100: { enabled: true, operator: 'GreaterThan', threshold: 100, thresholdType: 'Forecasted', contactEmails: [ email ] }
    }
  }
}
