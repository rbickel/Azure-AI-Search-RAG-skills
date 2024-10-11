
@description('The url of the Azure Cognitive Search instance')
param azureAiSearchName string


resource azureAiSearch 'Microsoft.Search/searchServices@2024-03-01-preview' = {
  name: azureAiSearchName
  location: resourceGroup().location
  sku: {
    name: 'standard'
  }
  properties: {}
}
