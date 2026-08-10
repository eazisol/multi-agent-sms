targetScope = 'resourceGroup'

@description('Environment name: staging or production')
@allowed(['staging', 'production'])
param environmentName string

@description('Organization short name used for resource naming')
param orgShortName string = 'masms'

@description('Azure region')
param location string = resourceGroup().location

@description('Key Vault name (must be globally unique); do not put secrets in this file')
param keyVaultName string

var namePrefix = '${orgShortName}-${environmentName}'

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
    publicNetworkAccess: 'Enabled'
  }
  tags: {
    environment: environmentName
    module: 'MOD-030'
    managedBy: 'bicep-skeleton'
  }
}

output keyVaultUri string = keyVault.properties.vaultUri
output namePrefix string = namePrefix
