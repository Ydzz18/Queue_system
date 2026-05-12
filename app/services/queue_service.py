# Queue logic (enqueue, dequeue, next_ticket)
from typing import Optional
from app.models.queue import Queue, Ticket
from app.database.db_manager import DatabaseManager
from app.utils.helpers import get_current_datetime
from datetime import datetime
import uuid

class QueueService:
    """Service for managing queue operations."""
    
    def __init__(self, db: DatabaseManager):
        """Initialize queue service."""
        self.db = db
    
    def enqueue_ticket(self, department: str, customer_name: str, priority: int = 5, notes: str = "") -> Optional[Ticket]:
        """Add a ticket to queue and return the ticket."""
        # Get or create queue for department
        queue = self.db.get_queue_by_department(department)
        if not queue:
            queue = self.db.create_queue(department)
        
        # Create ticket
        ticket_id = str(uuid.uuid4())
        ticket_number = f"{department[:1].upper()}{queue.get_queue_count() + 1:04d}"
        
        ticket = Ticket(
            ticket_id=ticket_id,
            ticket_number=ticket_number,
            customer_name=customer_name,
            department=department,
            issued_at=datetime.now().isoformat(),
            status='waiting',
            priority=priority,
            notes=notes
        )
        
        # Add to queue
        self.db.add_ticket_to_queue(queue.queue_id, ticket)
        return ticket
    
    def call_next_ticket(self, queue_id: str) -> Optional[Ticket]:
        """Call the next ticket in queue."""
        queue = self.db.get_queue(queue_id)
        if not queue:
            return None
        
        # Get current called ticket and mark as completed if exists
        current = queue.get_current_ticket()
        if current:
            current.status = 'completed'
            current.completed_at = datetime.now().isoformat()
            self.db.update_ticket(queue_id, current)
            self.db.save_ticket_history(current)
        
        # Get next waiting ticket
        next_ticket = queue.get_next_ticket()
        if next_ticket:
            next_ticket.status = 'called'
            next_ticket.called_at = datetime.now().isoformat()
            self.db.update_ticket(queue_id, next_ticket)
            self.db.update_queue(queue)
            return next_ticket
        
        return None
    
    def skip_ticket(self, queue_id: str, ticket_id: str) -> bool:
        """Skip a ticket and move to next."""
        queue = self.db.get_queue(queue_id)
        if not queue:
            return False
        
        ticket = self.db.get_ticket(ticket_id)
        if ticket:
            ticket.status = 'skipped'
            self.db.update_ticket(queue_id, ticket)
            self.db.save_ticket_history(ticket)
        
        # Call next ticket
        self.call_next_ticket(queue_id)
        return True
    
    def recall_ticket(self, queue_id: str, ticket_id: str) -> bool:
        """Recall a ticket (move back to waiting status)."""
        ticket = self.db.get_ticket(ticket_id)
        if ticket:
            ticket.status = 'waiting'
            ticket.called_at = None
            self.db.update_ticket(queue_id, ticket)
            return True
        return False
    
    def complete_ticket(self, queue_id: str, ticket_id: str) -> bool:
        """Mark ticket as completed."""
        ticket = self.db.get_ticket(ticket_id)
        if ticket:
            ticket.status = 'completed'
            ticket.completed_at = datetime.now().isoformat()
            self.db.update_ticket(queue_id, ticket)
            self.db.save_ticket_history(ticket)
            return True
        return False
    
    def get_queue_status(self, queue_id: str) -> dict:
        """Get current queue status."""
        queue = self.db.get_queue(queue_id)
        if not queue:
            return {}
        
        current = queue.get_current_ticket()
        next_ticket = queue.get_next_ticket()
        
        return {
            'queue_id': queue_id,
            'department': queue.department,
            'current_ticket': current.to_dict() if current else None,
            'next_ticket': next_ticket.to_dict() if next_ticket else None,
            'waiting_count': queue.get_queue_count('waiting'),
            'total_tickets': len(queue.tickets)
        }
    
    def get_all_queues_status(self) -> list:
        """Get status of all queues."""
        queues = self.db.get_all_queues()
        return [self.get_queue_status(q.queue_id) for q in queues]
    
    def reset_queue(self, queue_id: str) -> bool:
        """Reset queue (clear all tickets)."""
        queue = self.db.get_queue(queue_id)
        if queue:
            queue.tickets = []
            self.db.update_queue(queue)
            return True
        return False
