import json
import hmac
import base64
from typing import Any, Literal
from secrets import compare_digest
from .segments import DigestMod, Header, Payload


class JsonWebToken:
    """
    A class to handle the creation, decoding, and verification of JSON Web Tokens (JWT).

    JSON Web Tokens (JWT) are a compact, URL-safe means of representing claims to be transferred between two parties.
    This class provides methods to encode, decode, and verify JWTs using a specified signing algorithm (HS256, HS384, HS512).

    Methods:
        - encode: Encode a JWT from a header, payload, and secret key.
        - decode: Decode a JWT string into its header, payload, and signature.
        - verify: Verify the validity of a JWT by checking the signature, header, and payload.
    """

    @classmethod
    def _urlsafe_b64encode_dict(cls, obj: Any) -> str:
        """
         Encodes a Python object into a URL-safe base64 string.

         The object is serialized to a JSON string using `json.dumps()` and then URL-safe base64
         encoded. This is typically used for encoding the JWT header and payload.

        Args:
             obj (Any): The Python object to be serialized and encoded. It should be serializable
                         by `json.dumps()`.

         Returns:
             str: A URL-safe base64-encoded string representing the serialized JSON object.

         Example:
             data = {'key': 'value'}
             encoded_data = JsonWebToken._urlsafe_b64encode_dict(data)
        """
        return base64.urlsafe_b64encode(json.dumps(obj).encode("utf-8")).decode("utf-8")

    @classmethod
    def _urlsafe_b64decode_dict(cls, s: str) -> dict:
        """
        Decodes a URL-safe base64 string into a Python dictionary.

        The input string is first decoded from URL-safe base64 into bytes, then the byte data
        is deserialized into a Python dictionary using `json.loads()`.

        Args:
            s (str): A URL-safe base64-encoded string to be decoded and parsed into a dictionary.

        Returns:
            dict: A Python dictionary parsed from the decoded JSON data.

        Example:
            encoded_data = 'eyJrZXkiOiAidmFsdWUifQ=='  # Example URL-safe base64 encoded string
            decoded_data = JsonWebToken._urlsafe_b64decode_dict(encoded_data)
        """
        return json.loads(base64.urlsafe_b64decode(s))

    @classmethod
    def _generate_signature(
        cls, base64_header: str, base64_payload: str, key: str, algorithm: str
    ) -> str:
        """
        Generates a cryptographic signature for a JSON Web Token (JWT).

        This method combines the base64-encoded header and payload, applies HMAC (Hash-based
        Message Authentication Code) using the provided secret key and signing algorithm,
        then URL-safe base64 encodes the resulting signature.

        Args:
            base64_header (str): The base64-encoded JWT header string.
            base64_payload (str): The base64-encoded JWT payload string.
            key (str): The secret key used for signing the token.
            algorithm (str): The signing algorithm (e.g., "HS256", "HS384", "HS512").

        Returns:
            str: A URL-safe base64-encoded signature for the JWT.

        Example:
            header = 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9'
            payload = 'eyJ1c2VyX2lkIjogMSwgIm5hbWUiOiAiSm9obiBEb2UifQ=='
            key = 'secretkey'
            algorithm = 'HS256'
            signature = JsonWebToken._generate_signature(header, payload, key, algorithm)
        """
        msg = f"{base64_header}.{base64_payload}".encode("utf-8")
        digest = hmac.new(
            key=key.encode("utf-8"), msg=msg, digestmod=DigestMod[algorithm]
        ).digest()
        return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")

    @classmethod
    def _verify_signature(
        cls, header: dict, payload: dict, key: str, algorithm: str, signature: str
    ) -> bool:
        """
        Verify the signature of the JWT.

        This method generates the signature by encoding the header and payload, then compares it with the provided
        signature using the specified algorithm and secret key.

        Args:
            header (dict): The header part of the JWT.
            payload (dict): The payload part of the JWT.
            key (str): The secret key used for signing.
            algorithm (str): The signing algorithm to use (e.g., 'HS256', 'HS384', 'HS512').
            signature (str): The provided signature to verify.

        Returns:
            bool: True if the signature is valid, False otherwise.

        Example:
            is_valid_signature = JsonWebToken._verify_signature(header, payload, key, 'HS256', signature)
        """
        base64_header = cls._urlsafe_b64encode_dict(header)
        base64_payload = cls._urlsafe_b64encode_dict(payload)

        computed_signature = cls._generate_signature(
            base64_header, base64_payload, key, algorithm
        )

        return compare_digest(signature, computed_signature)

    @classmethod
    def encode(
        cls,
        payload: dict,
        key: str,
        algorithm: Literal["HS256", "HS384", "HS512"] = "HS256",
        header: dict | None = None,
    ) -> str:
        """
        Encode a payload into a JWT.

        This method encodes the payload and header into a JWT using the specified algorithm and secret key.
        It creates a base64-encoded JWT in the format:
        header.payload.signature.

        Args:
            payload (dict): The payload to include in the JWT.
            key (str): The secret key used for signing the JWT.
            algorithm (str): The signing algorithm to use ('HS256', 'HS384', 'HS512'). Default is 'HS256'.
            header (dict, optional): The header of the JWT. If None, the default header with 'alg' and 'typ' is used.

        Returns:
            str: The JWT string in the format 'header.payload.signature'.

        Example:
            token = JsonWebToken.encode(payload, key, 'HS256')
        """
        header = {**{"alg": algorithm, "typ": "JWT"}, **(header or {})}
        base64_header = cls._urlsafe_b64encode_dict(header)
        base64_payload = cls._urlsafe_b64encode_dict(payload)

        signature = cls._generate_signature(
            base64_header, base64_payload, key, algorithm
        )

        return f"{base64_header}.{base64_payload}.{signature}"

    @classmethod
    def decode(cls, token: str) -> tuple[dict, dict, str]:
        """
        Decode a JWT string into its components.

        This method splits the JWT into its header, payload, and signature parts, then decodes the header and payload
        from base64 and returns them along with the signature.

        Args:
            token (str): The JWT string to decode.

        Returns:
            tuple: A tuple containing the decoded header (dict), decoded payload (dict), and signature (str).

        Example:
            header, payload, signature = JsonWebToken.decode(token)
        """
        header, payload, signature = token.split(".")
        header = cls._urlsafe_b64decode_dict(header)
        payload = cls._urlsafe_b64decode_dict(payload)
        return header, payload, signature

    @classmethod
    def verify(
        cls,
        token: str,
        key: str,
        algorithm: Literal["HS256", "HS384", "HS512"] = "HS256",
        iss: str | None = None,
        sub: str | None = None,
        aud: str | None = None,
    ) -> bool:
        """
        Verify the validity of a JWT.

        This method verifies the JWT by checking the signature, header, and payload. It ensures that the header is valid,
        the payload contains the expected claims (such as 'iss', 'sub', and 'aud'), and the signature is correct.

        Args:
            token (str): The JWT string to verify.
            key (str): The secret key used to verify the signature.
            algorithm (str): The signing algorithm used for verification ('HS256', 'HS384', 'HS512').
            iss (str, optional): The expected issuer of the JWT. If None, no check is performed.
            sub (str, optional): The expected subject of the JWT. If None, no check is performed.
            aud (str, optional): The expected audience of the JWT. If None, no check is performed.

        Returns:
            bool: True if the JWT is valid (signature, header, and payload are verified), False otherwise.

        Example:
            is_valid = JsonWebToken.verify(token, key, 'HS256', iss='issuer', sub='subject', aud='audience')
        """
        header, payload, signature = cls.decode(token=token)

        is_header_verified = Header(**header).verify(algorithm=algorithm)
        if not is_header_verified:
            return False

        is_payload_verified = Payload(**payload).verify(iss=iss, sub=sub, aud=aud)
        if not is_payload_verified:
            return False

        is_signature_verified = cls._verify_signature(
            header=header,
            payload=payload,
            key=key,
            algorithm=algorithm,
            signature=signature,
        )
        if not is_signature_verified:
            return False

        return True
