// 0.3 — A empresa fictícia: App Service com a API Node.js da Loja Pixel (plano B1 Linux)
param location string = resourceGroup().location
param prefixo string = 'lojapixel'
resource plano 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: '${prefixo}-plano'
  location: location
  sku: { name: 'B1' }
  kind: 'linux'
  properties: { reserved: true }
}
resource api 'Microsoft.Web/sites@2023-12-01' = {
  name: '${prefixo}-api-${uniqueString(resourceGroup().id)}'
  location: location
  identity: { type: 'SystemAssigned' }
  properties: {
    serverFarmId: plano.id
    httpsOnly: true
    siteConfig: { linuxFxVersion: 'NODE|20-lts', minTlsVersion: '1.2', ftpsState: 'Disabled' }
  }
}
output url string = 'https://${api.properties.defaultHostName}'
