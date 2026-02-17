import hashlib
import hmac
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict
import secrets

# ============================================================================
# AUTHENTICATION & AUTHORIZATION SERVICE
# ============================================================================

class AuthService:
    """JWT-based authentication service with secure password hashing"""
    
    def __init__(self, secret_key: str, algorithm: str = "HS256", token_expiry_hours: int = 24):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expiry_hours = token_expiry_hours
    
    # ------------------------------------------------------------------------
    # PASSWORD HASHING (using PBKDF2)
    # ------------------------------------------------------------------------
    
    def hash_password(self, password: str, salt: Optional[str] = None) -> str:
        """Hash a password using PBKDF2-SHA256"""
        if salt is None:
            salt = secrets.token_hex(32)
        
        # PBKDF2 with SHA256, 100000 iterations
        pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), 
                                       salt.encode('utf-8'), 100000)
        pwdhash_hex = pwdhash.hex()
        
        # Return salt$hash format
        return f"{salt}${pwdhash_hex}"
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against its hash"""
        try:
            salt, stored_hash = password_hash.split('$')
            new_hash = self.hash_password(password, salt)
            return hmac.compare_digest(new_hash, password_hash)
        except Exception:
            return False
    
    # ------------------------------------------------------------------------
    # JWT TOKEN GENERATION
    # ------------------------------------------------------------------------
    
    def create_access_token(self, user_id: str, email: str, role: str = "user") -> str:
        """Create JWT access token"""
        payload = {
            "user_id": user_id,
            "email": email,
            "role": role,
            "exp": datetime.utcnow() + timedelta(hours=self.token_expiry_hours),
            "iat": datetime.utcnow(),
            "type": "access"
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def create_refresh_token(self, user_id: str) -> str:
        """Create JWT refresh token (longer expiry)"""
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(days=30),
            "iat": datetime.utcnow(),
            "type": "refresh"
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    # ------------------------------------------------------------------------
    # TOKEN VERIFICATION
    # ------------------------------------------------------------------------
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None  # Token expired
        except jwt.InvalidTokenError:
            return None  # Invalid token
    
    def decode_token_payload(self, token: str) -> Optional[Dict]:
        """Decode token without verification (for debugging)"""
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            return payload
        except Exception:
            return None

# ============================================================================
# RBAC (Role-Based Access Control)
# ============================================================================

class RBACService:
    """Role-based access control for authorization"""
    
    ROLES = {
        "user": {
            "permissions": [
                "view_jobs",
                "apply_to_jobs",
                "manage_own_profile",
                "upload_resume",
                "view_applications"
            ]
        },
        "moderator": {
            "permissions": [
                "view_jobs",
                "moderate_jobs",
                "view_all_users",
                "moderate_content",
                "view_analytics"
            ]
        },
        "admin": {
            "permissions": [
                "view_jobs",
                "moderate_jobs",
                "manage_users",
                "manage_admins",
                "view_analytics",
                "manage_system_settings",
                "delete_content"
            ]
        },
        "super_admin": {
            "permissions": [
                "*"  # All permissions
            ]
        }
    }
    
    @classmethod
    def has_permission(cls, role: str, permission: str) -> bool:
        """Check if role has specific permission"""
        if role not in cls.ROLES:
            return False
        
        role_permissions = cls.ROLES[role]["permissions"]
        
        # Super admin has all permissions
        if "*" in role_permissions:
            return True
        
        return permission in role_permissions
    
    @classmethod
    def get_role_permissions(cls, role: str) -> list:
        """Get all permissions for a role"""
        if role not in cls.ROLES:
            return []
        return cls.ROLES[role]["permissions"]

# ============================================================================
# API KEY MANAGEMENT (for programmatic access)
# ============================================================================

class APIKeyService:
    """Manage API keys for external integrations"""
    
    @staticmethod
    def generate_api_key() -> str:
        """Generate secure API key"""
        return f"sk_{secrets.token_urlsafe(32)}"
    
    @staticmethod
    def hash_api_key(api_key: str) -> str:
        """Hash API key for storage using SHA256"""
        salt = secrets.token_hex(16)
        key_hash = hashlib.sha256((api_key + salt).encode()).hexdigest()
        return f"{salt}${key_hash}"
    
    @staticmethod
    def verify_api_key(api_key: str, api_key_hash: str) -> bool:
        """Verify API key against hash"""
        try:
            salt, stored_hash = api_key_hash.split('$')
            new_hash = hashlib.sha256((api_key + salt).encode()).hexdigest()
            return hmac.compare_digest(new_hash, stored_hash)
        except Exception:
            return False

# ============================================================================
# DEMONSTRATION
# ============================================================================

print("=" * 80)
print("AUTHENTICATION & AUTHORIZATION SERVICE - COMPLETE")
print("=" * 80)

# Initialize auth service
auth_service = AuthService(secret_key="demo_secret_key_change_in_production")

print("\n🔐 PASSWORD HASHING DEMO:")
demo_password = "SecurePassword123!"
password_hash = auth_service.hash_password(demo_password)
print(f"  Original: {demo_password}")
print(f"  Hashed: {password_hash[:50]}...")
print(f"  Verification: {auth_service.verify_password(demo_password, password_hash)}")
print(f"  Wrong password: {auth_service.verify_password('WrongPassword', password_hash)}")

print("\n🎫 JWT TOKEN GENERATION DEMO:")
access_token = auth_service.create_access_token(
    user_id="usr_12345",
    email="john.doe@example.com",
    role="user"
)
print(f"  Access Token: {access_token[:50]}...")

refresh_token = auth_service.create_refresh_token(user_id="usr_12345")
print(f"  Refresh Token: {refresh_token[:50]}...")

print("\n🔍 TOKEN VERIFICATION DEMO:")
token_payload = auth_service.verify_token(access_token)
if token_payload:
    print(f"  User ID: {token_payload['user_id']}")
    print(f"  Email: {token_payload['email']}")
    print(f"  Role: {token_payload['role']}")
    print(f"  Expires: {datetime.fromtimestamp(token_payload['exp'])}")

print("\n🛡️ RBAC PERMISSIONS DEMO:")
print(f"  User can view jobs: {RBACService.has_permission('user', 'view_jobs')}")
print(f"  User can moderate: {RBACService.has_permission('user', 'moderate_jobs')}")
print(f"  Admin can moderate: {RBACService.has_permission('admin', 'moderate_jobs')}")
print(f"  Admin permissions: {RBACService.get_role_permissions('admin')}")

print("\n🔑 API KEY MANAGEMENT DEMO:")
api_key_service = APIKeyService()
demo_api_key = api_key_service.generate_api_key()
api_key_hash = api_key_service.hash_api_key(demo_api_key)
print(f"  Generated Key: {demo_api_key[:20]}...")
print(f"  Hashed: {api_key_hash[:50]}...")
print(f"  Verification: {api_key_service.verify_api_key(demo_api_key, api_key_hash)}")

print("\n" + "=" * 80)
print("AUTHENTICATION FEATURES")
print("=" * 80)
print("  ✅ PBKDF2-SHA256 password hashing with salt")
print("  ✅ JWT access tokens (24h expiry)")
print("  ✅ JWT refresh tokens (30d expiry)")
print("  ✅ Token verification and decoding")
print("  ✅ RBAC with 4 roles: user, moderator, admin, super_admin")
print("  ✅ Permission-based authorization")
print("  ✅ API key generation for external access")
print("  ✅ Secure key hashing and verification")
print("  ✅ Timing-safe comparison (hmac.compare_digest)")

print("\n📋 INTEGRATION READY:")
print("  • FastAPI dependency injection for route protection")
print("  • Middleware for token validation")
print("  • Role-based endpoint access control")
print("  • Secure password reset flows")
print("  • API key authentication for scrapers/bots")
