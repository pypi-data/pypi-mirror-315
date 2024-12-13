# Pytography

A Python library that provides secure password hashing and JSON Web Token (JWT) functionality.

## Installation

```bash
pip install pytography
```
## Quick Start

### PHC String Format

The **PHC (Password Hashing Competition) string format** is a standardized way of representing password hashes for various algorithms. It includes all the necessary information to verify the password, including the hashing algorithm, parameters (e.g., cost factor, salt, and iteration count), and the resulting hash.

### Structure

The structure of a PHC string is as follows:
- **`<algorithm>`**: The name of the hashing algorithm used (e.g., `pbkdf2`, `scrypt`).
- **`<parameters>`**: The specific parameters used for the algorithm, such as the cost factor, salt, and iteration count.
- **`<hash>`**: The actual password hash.

### Why Use PHC Format?

1. **Portability**: The PHC format makes it easy to migrate password hashes between different systems.
2. **Security**: It ensures that all relevant parameters for hashing are stored alongside the hash, including salts and iteration counts.
3. **Standardization**: It provides a uniform format for representing password hashes across different hashing algorithms.

### Scrypt (with PHC format)

- `scrypt`: Indicates the scrypt hashing algorithm.
- `16384`: CPU/memory cost.
- `8`: Block size.
- `32`: Parallelization factor.
- The salt and hash are base64 encoded.
- PHC string format \$scrypt\$ln={n}\$r={r}\$p={p}\${salt}\${password_hash}

### Pbkdf2 (with PHC format)

- `pbkdf2`: Indicates the pbkdf2 hashing algorithm.
- `sha256`: The hash function to use.
- `600000`: The number of iterations to use for key derivation.
- The salt and hash are base64 encoded.
- PHC string format \$pbkdf2-{hash_name}\$i={iterations}\${salt}\${password_hash}

### Password Hashing with Scrypt (Default)
```python
from pytography import PasswordHashLibrary

encoded_password = PasswordHashLibrary.encode(password="password", algorithm="scrypt")
is_valid = PasswordHashLibrary.verify(password="password", encoded_password=encoded_password)
```

### Password Hashing with Pbkdf2
```python
from pytography import PasswordHashLibrary

encoded_password = PasswordHashLibrary.encode(password="password", algorithm="pbkdf2")
is_valid = PasswordHashLibrary.verify(password="password", encoded_password=encoded_password)
```

### JSON Web Token (JWT)
```python
from pytography import JsonWebToken
from datetime import datetime, timedelta, UTC

now = datetime.now(UTC)
exp = (now + timedelta(seconds=7200)).timestamp()

# Create a token
token = JsonWebToken.encode(payload={"exp": exp, "user_id": 123}, key="key")

# Decode token to get payload
header, payload, signature = JsonWebToken.decode(token=token)

# Verify token
is_valid = JsonWebToken.verify(token=token, key="key")
```

## License
This project is licensed under the terms of the LICENSE file included in the repository.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.


