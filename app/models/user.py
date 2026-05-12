# User data structures
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
import uuid

@dataclass
class User:
    """Represents a staff member/admin user."""
    user_id: str
    username: str
    password_hash: str
    email: str
    full_name: str
    role: str  # 'admin', 'cashier', 'manager'
    department: str
    is_active: bool = True
    created_at: str = None
    last_login: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """Convert user to dictionary (excluding password hash)."""
        data = asdict(self)
        data.pop('password_hash', None)  # Don't expose password hash
        return data
    
    @staticmethod
    def from_dict(data: dict) -> 'User':
        """Create user from dictionary."""
        return User(**data)
    
    def update_last_login(self) -> None:
        """Update last login timestamp."""
        self.last_login = datetime.now().isoformat()
    
    def is_admin(self) -> bool:
        """Check if user is admin."""
        return self.role == 'admin'
    
    def is_manager(self) -> bool:
        """Check if user is manager."""
        return self.role == 'manager'
    
    def can_manage_queue(self) -> bool:
        """Check if user can manage queue."""
        return self.role in ['admin', 'manager', 'cashier']

@dataclass
class AdminSession:
    """Represents an active admin session."""
    session_id: str
    user_id: str
    username: str
    login_time: str
    is_active: bool = True
    
    def to_dict(self) -> dict:
        """Convert session to dictionary."""
        return asdict(self)
    
    @staticmethod
    def from_dict(data: dict) -> 'AdminSession':
        """Create session from dictionary."""
        return AdminSession(**data)
