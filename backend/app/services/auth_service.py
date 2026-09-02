import hashlib
import json
import base64
import time
from typing import Dict, Any, Optional

SECRET_KEY = "postmortem_secret_jwt_key_super_secure"

class AuthService:
    def hash_password(self, password: str) -> str:
        """Hashes password using SHA-256 with salt."""
        salt = "postmortem_salt_2026"
        return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()

    def verify_password(self, password: str, hashed: str) -> bool:
        return self.hash_password(password) == hashed

    def create_token(self, user_id: int, email: str, role: str) -> str:
        """Generates a lightweight JWT token."""
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {
            "sub": str(user_id),
            "email": email,
            "role": role,
            "exp": int(time.time()) + 86400  # 24 hours validity
        }
        
        b64_header = base64.b64encode(json.dumps(header).encode("utf-8")).decode("utf-8").replace("=", "")
        b64_payload = base64.b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8").replace("=", "")
        signature = hashlib.sha256(f"{b64_header}.{b64_payload}.{SECRET_KEY}".encode("utf-8")).hexdigest()
        
        return f"{b64_header}.{b64_payload}.{signature}"

    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Decodes and verifies a lightweight JWT token."""
        try:
            parts = token.split(".")
            if len(parts) != 3:
                return None
            b64_header, b64_payload, signature = parts
            expected_sig = hashlib.sha256(f"{b64_header}.{b64_payload}.{SECRET_KEY}".encode("utf-8")).hexdigest()
            if signature != expected_sig:
                return None
            
            # Add back base64 padding
            padded = b64_payload + "=" * (-len(b64_payload) % 4)
            payload = json.loads(base64.b64decode(padded).decode("utf-8"))
            if payload.get("exp", 0) < time.time():
                return None  # Expired
            return payload
        except Exception:
            return None
