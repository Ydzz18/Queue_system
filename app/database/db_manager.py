# CRUD operations for JSON database
import json
import os
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.queue import Queue, Ticket
from app.models.user import User
from app.utils.constants import DATABASE_PATH

class DatabaseManager:
    """Manages database operations using JSON files."""
    
    def __init__(self, db_path: str = DATABASE_PATH):
        """Initialize database manager."""
        self.db_path = db_path
        self.data = self._load_database()
    
    def _load_database(self) -> dict:
        """Load database from JSON file."""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._get_default_structure()
        return self._get_default_structure()
    
    def _get_default_structure(self) -> dict:
        """Get default database structure."""
        return {
            'queues': {},
            'users': {},
            'sessions': {},
            'tickets_history': [],
            'settings': {}
        }
    
    def save_database(self) -> bool:
        """Save database to JSON file."""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            with open(self.db_path, 'w') as f:
                json.dump(self.data, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving database: {e}")
            return False
    
    # Queue operations
    def create_queue(self, department: str) -> Queue:
        """Create a new queue for a department."""
        from uuid import uuid4
        queue_id = str(uuid4())
        queue = Queue(
            queue_id=queue_id,
            department=department,
            created_at=datetime.now().isoformat()
        )
        self.data['queues'][queue_id] = queue.to_dict()
        self.save_database()
        return queue
    
    def get_queue(self, queue_id: str) -> Optional[Queue]:
        """Get queue by ID."""
        if queue_id in self.data['queues']:
            return Queue.from_dict(self.data['queues'][queue_id])
        return None
    
    def get_queue_by_department(self, department: str) -> Optional[Queue]:
        """Get queue by department name."""
        for queue_data in self.data['queues'].values():
            if queue_data['department'] == department and queue_data['is_active']:
                return Queue.from_dict(queue_data)
        return None
    
    def get_all_queues(self) -> List[Queue]:
        """Get all active queues."""
        queues = []
        for queue_data in self.data['queues'].values():
            if queue_data['is_active']:
                queues.append(Queue.from_dict(queue_data))
        return queues
    
    def update_queue(self, queue: Queue) -> bool:
        """Update queue."""
        if queue.queue_id in self.data['queues']:
            self.data['queues'][queue.queue_id] = queue.to_dict()
            self.save_database()
            return True
        return False
    
    def delete_queue(self, queue_id: str) -> bool:
        """Delete queue (soft delete - set is_active to False)."""
        if queue_id in self.data['queues']:
            self.data['queues'][queue_id]['is_active'] = False
            self.save_database()
            return True
        return False
    
    # Ticket operations
    def add_ticket_to_queue(self, queue_id: str, ticket: Ticket) -> bool:
        """Add ticket to a queue."""
        if queue_id in self.data['queues']:
            queue = Queue.from_dict(self.data['queues'][queue_id])
            queue.add_ticket(ticket)
            self.data['queues'][queue_id] = queue.to_dict()
            self.save_database()
            return True
        return False
    
    def get_ticket(self, ticket_id: str) -> Optional[Ticket]:
        """Get ticket by ID from all queues."""
        for queue_data in self.data['queues'].values():
            for ticket_data in queue_data['tickets']:
                if ticket_data['ticket_id'] == ticket_id:
                    return Ticket.from_dict(ticket_data)
        return None
    
    def update_ticket(self, queue_id: str, ticket: Ticket) -> bool:
        """Update ticket in a queue."""
        if queue_id in self.data['queues']:
            queue = Queue.from_dict(self.data['queues'][queue_id])
            for i, t in enumerate(queue.tickets):
                if t.ticket_id == ticket.ticket_id:
                    queue.tickets[i] = ticket
                    self.data['queues'][queue_id] = queue.to_dict()
                    self.save_database()
                    return True
        return False
    
    def save_ticket_history(self, ticket: Ticket) -> bool:
        """Save ticket to history."""
        self.data['tickets_history'].append(ticket.to_dict())
        self.save_database()
        return True
    
    def get_tickets_history(self, limit: int = 100) -> List[Ticket]:
        """Get ticket history."""
        tickets = [Ticket.from_dict(t) for t in self.data['tickets_history'][-limit:]]
        return list(reversed(tickets))
    
    # User operations
    def create_user(self, user: User) -> bool:
        """Create a new user."""
        if user.user_id not in self.data['users']:
            self.data['users'][user.user_id] = asdict(user)
            self.save_database()
            return True
        return False
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        if user_id in self.data['users']:
            return User.from_dict(self.data['users'][user_id])
        return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        for user_data in self.data['users'].values():
            if user_data['username'] == username:
                return User.from_dict(user_data)
        return None
    
    def get_all_users(self) -> List[User]:
        """Get all users."""
        return [User.from_dict(u) for u in self.data['users'].values()]
    
    def update_user(self, user: User) -> bool:
        """Update user."""
        if user.user_id in self.data['users']:
            self.data['users'][user.user_id] = asdict(user)
            self.save_database()
            return True
        return False
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user (soft delete)."""
        if user_id in self.data['users']:
            self.data['users'][user_id]['is_active'] = False
            self.save_database()
            return True
        return False

def asdict(obj):
    """Convert dataclass to dict."""
    if hasattr(obj, '__dataclass_fields__'):
        from dataclasses import asdict as dc_asdict
        return dc_asdict(obj)
    return obj.__dict__
