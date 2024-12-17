# Vault Service

The **Vault Service** package provides a convenient interface for interacting with HashiCorp Vault. It offers various methods to manage secrets for different tenants and connectors. This package is designed for seamless integration into your applications.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Methods](#methods)
  - [store_secret](#store_secret)
  - [get_secret](#get_secret)
  - [update_secret](#update_secret)
  - [delete_secret](#delete_secret)
  - [get_all_secrets_for_tenant](#get_all_secrets_for_tenant)
  - [delete_all_secrets_for_tenant](#delete_all_secrets_for_tenant)
- [License](#license)

## Installation

You can install the Vault Service package using pip:

```bash
pip install vault-service
```

## Usage

To use the Vault Service, you need to initialize the `VaultController` and then call the utility functions. Make sure to set the required environment variables for Vault connection:

```bash
export VAULT_ADDR='https://your-vault-address'
export BASE_PATH='your-base-path'
export APP_ROLE_ID='your-app-role-id'
export APP_SECRET_ID='your-app-secret-id'
```

## Methods

### `store_secret(root_path: str, sub_path: str, secret_name: str, secret_data: SecretData, credentials: dict)`

Stores a new secret in HashiCorp Vault under the specified path.

**Parameters:**
- `root_path`: The root path in Vault.
- `sub_path`: The sub path in Vault.
- `secret_name`: The name of the secret to store.
- `secret_data`: An instance of `SecretData`, containing the secret information to be stored.
- `credentials`: Dictionary containing Vault credentials:
  ```python
  {
      'base_path': 'your-base-path',
      'app_role_id': 'your-app-role-id',
      'app_secret_id': 'your-app-secret-id'
  }
  ```

**Returns:** 
- `dict`: Response object containing:
  - `status`: "success" or "error"
  - `message`: Description of the operation result

**Sample Payload for `secret_data`:**
```json
{
  "auth_key": "<auth-key>",
  "database_credentials": {
    "host": "localhost",
    "port": 5432,
    "database": "my_database",
    "user": "my_user",
    "password": "my_password"
  },
  "redis_credentials": {
    "host": "localhost",
    "port": 6379,
    "password": "my_password"
  }
}
```

---

### `get_secret(root_path: str, sub_path: str, secret_name: str, credentials: dict)`

Retrieves a secret from HashiCorp Vault.

**Parameters:**
- `root_path`: The root path in Vault.
- `sub_path`: The sub path in Vault.
- `secret_name`: The name of the secret to retrieve.
- `credentials`: Dictionary containing Vault credentials.

**Returns:**
- `dict`: Response object containing:
  - `status`: "success" or "error"
  - `message`: Description of the operation result
  - `data`: The retrieved secret data (when successful)

---

### `update_secret(service_id: str, tenant_id: str, secret_name: str, secret_data: SecretData, credentials: Optional[dict] = None)`

Updates an existing secret in HashiCorp Vault for the specified service, tenant, and secret name.

**Parameters:**
- `service_id`: The ID of the service.
- `tenant_id`: The ID of the tenant.
- `secret_name`: The name of the secret to update.
- `secret_data`: An instance of `SecretData`, containing the updated secret information.
- `credentials`: Optional dictionary containing Vault credentials:
  ```python
  {
      'base_path': 'your-base-path',
      'app_role_id': 'your-app-role-id',
      'app_secret_id': 'your-app-secret-id'
  }
  ```

**Returns:** A message indicating the success or failure of the operation.

**Sample Payload for `secret_data`:**
```json
{
  "auth_key": "<new-auth-key>",
  "database_credentials": {
    "host": "localhost",
    "port": 5432,
    "database": "my_database",
    "user": "my_user",
    "password": "new_password"
  },
  "redis_credentials": {
    "host": "localhost",
    "port": 6379,
    "password": "new_password"
  }
}
```

---

### `delete_secret(service_id: str, tenant_id: str, secret_name: str)`

Deletes a secret from HashiCorp Vault for the specified service, tenant, and secret name.

**Parameters:**
- `service_id`: The ID of the service.
- `tenant_id`: The ID of the tenant.
- `secret_name`: The name of the secret to delete.

**Returns:** A message indicating the success or failure of the deletion.

---

### `get_all_secrets_for_tenant(root_path: str, sub_path: str, credentials: dict)`

Retrieves all secrets for a specific path from HashiCorp Vault.

**Parameters:**
- `root_path`: The root path in Vault.
- `sub_path`: The sub path in Vault.
- `credentials`: Dictionary containing Vault credentials.

**Returns:** 
- `dict`: Response object containing:
  - `status`: "success" or "error"
  - `message`: Description of the operation result
  - `data`: List of all secrets (when successful)

---

### `delete_all_secrets_for_tenant(service_id: str, tenant_id: str)`

Deletes all secrets associated with a specific tenant and service from HashiCorp Vault.

**Parameters:**
- `service_id`: The ID of the service.
- `tenant_id`: The ID of the tenant.

**Returns:** A message indicating the success or failure of the deletion.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

### Changes:
- Added `service_id` as the first required parameter for each method.
- Specified that `tenant_id` is not optional in each method.
- Added `credentials` parameter to each method signature.
- Specified that `credentials` is optional in each method documentation.