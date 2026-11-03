// 0.2 — Log Analytics workspace + Microsoft Sentinel
param location string = resourceGroup().location
param nome string = 'law-lojapixel'
resource law 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: nome
  location: location
  properties: {
    sku: { name: 'PerGB2018' }
    retentionInDays: 90
    workspaceCapping: { dailyQuotaGb: 1 }   // travão do laboratório: 1 GB/dia
  }
}
resource sentinel 'Microsoft.SecurityInsights/onboardingStates@2024-03-01' = {
  scope: law
  name: 'default'
  properties: {}
}
output workspaceId string = law.id
