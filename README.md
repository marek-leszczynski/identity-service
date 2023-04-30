# Identity Service

This is a service that provides authentication for both users and machine to machine clients. Users can issue a JWT token using their username and password, while machine clients can use a variety of authentication methods including client id and client secret, client id and RSA key, or client id, client secret, and RSA key at the same time.


## Dependencies

This service relies on the following dependencies:

- [FastAPI](https://fastapi.tiangolo.com/)
- [JWCrypto](https://jwcrypto.readthedocs.io/en/latest/)
- [Argon2-Cffi](https://argon2-cffi.readthedocs.io/en/stable/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [Fernet](https://cryptography.io/en/latest/fernet/)


## Authentication Methods

### User Authentication

To authenticate as a user, send a POST request to `/auth/login` with the following parameters:

```json
{
  "username": "your-username",
  "password": "your-password",
  "audience": "audience"
}
```

If the authentication is successful, the server will respond with a JWT token in the following format:

```json
{
  "token": "your-token",
  "audience": "audience"
}
```

### Machine Authentication
To authenticate as a machine client, send a POST request to /auth/token with one of the following sets of parameters:

- Using client id and client secret:
```json
{
  "client_id": "your-client-id",
  "client_secret": "your-client-secret",
  "audience": "audience"
}
```
- Using client id and RSA key:
```json
{
  "client_id": "your-client-id",
  "signature": "message-signature",
  "audience": "audience"
}
```
- Using client id, client secret, and RSA key:
```json
{
  "client_id": "your-client-id",
  "client_secret": "your-client-secret",
  "signature": "message-signature",
  "audience": "audience"
}
```
If the authentication is successful, the server will respond with a JWT token in the following format:

```json
{
  "token": "your-token",
  "audience": "audience"
}
```

## Security

This service takes security seriously and employs several measures to ensure the safety of user and client information.

### Passwords and Secrets

Passwords and secrets are hashed using the Argon2 algorithm, which is a secure and modern hashing algorithm.

### Private Key

The private key used for signing JWT tokens is encrypted using AES256 and the Fernet library. This ensures that even if the database is compromised, the private key remains secure.

## Setup

To set up this service, follow these steps:

1. Clone this repository.
2. Install PDM by running `pip install pdm`.
3. Install dependencies by running `pdm install`.
4. Configure environment variables.
5. Start the service by running `pdm run start`.

## Environment variables

- `PORT`: the port that the service listens on.
- `DATABASE_HOST`: the hostname of the database server.
- `DATABASE_USERNAME`: the username used to connect to the database.
- `DATABASE_PASSWORD`: the password used to connect to the database.
- `DATABASE_SCHEMA_NAME`: the name of the schema containing the database tables.
- `DATABASE_PORT`: the port number used to connect to the database.
- `DATABASE_DRIVER`: the database driver used by SQLAlchemy.
- `DATABASE_CONNECTION_POOL_SIZE`: the maximum number of connections to maintain in the connection pool.
- `DATABASE_CONNECTION_MAX_OVERFLOW`: the maximum number of connections allowed to overflow from the connection pool.
- `DATABASE_SSL_MODE`: the SSL mode used for database connections (optional).
- `DATABASE_SSL_ROOT_CERT`: the path to the SSL root certificate (optional).
- `DATABASE_SSL_CERT`: the path to the SSL certificate (optional).
- `DATABASE_SSL_KEY`: the path to the SSL private key (optional).
- `ENCRYPTION_KEY`: the key used to encrypt

## Configuration

To configure the service, send a POST request to `/api/configuration` with a JSON object containing the following options:

- `private_key`: the private key in PEM format for signing JWT tokens.
- `jwt_expiration`: the expiration time for JWT tokens (in seconds).
- `jwt_issuer`: the issuer of the JWT tokens.
- `jwt_max_refreshes`: the maximum number of times a token can be refreshed.

## Conclusion

This service provides a secure and reliable way to authenticate both users and machine clients. With its robust security measures and flexible authentication options, it can be used in a variety of applications.
