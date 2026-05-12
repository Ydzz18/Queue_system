# Admin login session handling
import hashlib
import uuid
from typing import Optional
from datetime import datetime, timedelta
from app.models.user import User, AdminSession
from app.database.db_manager import DatabaseManager
from app.utils.validators import validate_password

class AuthService:
    """Service for authentication and session management."""
    
    def __init__(self, db: DatabaseManager):
        """Initialize auth service."""
        self.db = db
        self._initialize_default_admin()
    
    def _initialize_default_admin(self):
        """Create default admin user if none exists."""
        admin = self.db.get_user_by_username('admin')
        if not admin:
            admin_user = User(
                user_id=str(uuid.uuid4()),
                username='admin',
                password_hash=self._hash_password('admin123'),
                email='admin@school.edu',
                full_name='Administrator',
                role='admin',
                department='General'
            )
            self.db.create_user(admin_user)
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username: str, password: str, email: str, full_name: str, role: str, department: str) -> tuple[bool, str]:
        """Register a new user."""
        # Validate inputs
        is_valid, msg = validate_password(password)
        if not is_valid:
            return False, msg
        
        # Check if user exists
        if self.db.get_user_by_username(username):
            return False, "Username already exists"
        
        # Create user
        user = User(
            user_id=str(uuid.uuid4()),
            username=username,
            password_hash=self._hash_password(password),
            email=email,
            full_name=full_name,
            role=role,
            department=department
        )
        
        if self.db.create_user(user):
            return True, "User registered successfully"
        return False, "Error registering user"
    
    def login(self, username: str, password: str) -> tuple[bool, Optional[AdminSession], str]:
        """Authenticate user and create session."""
        user = self.db.get_user_by_username(username)
        
        if not user:
            return False, None, "Invalid username or password"
        
        if not user.is_active:
            return False, None, "User account is inactive"
        
        # Verify password
        if user.password_hash != self._hash_password(password):
            return False, None, "Invalid username or password"
        
        # Update last login
        user.update_last_login()
        self.db.update_user(user)
        
        # Create session
        session = AdminSession(
            session_id=str(uuid.uuid4()),
            user_id=user.user_id,
            username=user.username,
            login_time=datetime.now().isoformat()
        )
        
        self.db.data['sessions'][session.session_id] = session.to_dict()
        self.db.save_database()
        
        return True, session, "Login successful"
    
    def logout(self, session_id: str) -> bool:
        """End a session."""
        if session_id in self.db.data['sessions']:
            self.db.data['sessions'][session_id]['is_active'] = False
            self.db.save_database()
            return True
        return False
    
    def verify_session(self, session_id: str) -> tuple[bool, Optional[User]]:
        """Verify if session is valid."""
        if session_id not in self.db.data['sessions']:
            return False, None
        
        session = self.db.data['sessions'][session_id]
        if not session['is_active']:
            return False, None
        
        # Check session expiry (24 hours)
        login_time = datetime.fromisoformat(session['login_time'])
        if datetime.now() - login_time > timedelta(hours=24):
            session['is_active'] = False
            self.db.save_database()
            return False, None
        
        user = self.db.get_user(session['user_id'])
        return True, user
    
    def change_password(self, user_id: str, old_password: str, new_password: str) -> tuple[bool, str]:
        """Change user password."""
        user = self.db.get_user(user_id)
        if not user:
            return False, "User not found"
        
        # Verify old password
        if user.password_hash != self._hash_password(old_password):
            return False, "Incorrect old password"
        
        # Validate new password
        is_valid, msg = validate_password(new_password)
        if not is_valid:
            return False, msg
        
        # Update password
        user.password_hash = self._hash_password(new_password)
        self.db.update_user(user)
        
        return True, "Password changed successfully"
    
    def reset_password(self, user_id: str, new_password: str) -> tuple[bool, str]:
        """Admin reset user password."""
        user = self.db.get_user(user_id)
        if not user:
            return False, "User not found"
        
        # Validate new password
        is_valid, msg = validate_password(new_password)
        if not is_valid:
            return False, msg
        
        # Reset password
        user.password_hash = self._hash_password(new_password)
        self.db.update_user(user)
        
        return True, "Password reset successfully"
    
    def get_active_sessions(self) -> list:
        """Get all active sessions."""
        active = []
        for session_data in self.db.data['sessions'].values():
            if session_data['is_active']:
                login_time = datetime.fromisoformat(session_data['login_time'])
                if datetime.now() - login_time <= timedelta(hours=24):
                    active.append(session_data)
        return active
