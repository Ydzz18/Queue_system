# Formatting and saving tickets
from typing import Optional
from app.models.queue import Ticket
from app.database.db_manager import DatabaseManager
from app.utils.helpers import get_current_datetime, format_ticket_number
from datetime import datetime
import os

# Optional PDF support
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class TicketService:
    """Service for ticket operations like formatting and saving."""
    
    def __init__(self, db: DatabaseManager):
        """Initialize ticket service."""
        self.db = db
    
    def format_ticket_for_display(self, ticket: Ticket) -> dict:
        """Format ticket data for UI display."""
        return {
            'ticket_id': ticket.ticket_id,
            'ticket_number': ticket.ticket_number,
            'customer_name': ticket.customer_name,
            'department': ticket.department,
            'status': ticket.status,
            'issued_at': self._format_time(ticket.issued_at),
            'called_at': self._format_time(ticket.called_at) if ticket.called_at else '-',
            'completed_at': self._format_time(ticket.completed_at) if ticket.completed_at else '-',
            'priority': self._get_priority_label(ticket.priority),
            'notes': ticket.notes
        }
    
    def _format_time(self, iso_time: str) -> str:
        """Format ISO datetime to readable format."""
        if not iso_time:
            return '-'
        dt = datetime.fromisoformat(iso_time)
        return dt.strftime("%H:%M:%S")
    
    def _get_priority_label(self, priority: int) -> str:
        """Get human-readable priority label."""
        labels = {
            1: "High Priority",
            2: "Senior Citizen",
            3: "PWD",
            4: "Pregnant",
            5: "Normal"
        }
        return labels.get(priority, "Normal")
    
    def generate_ticket_pdf(self, ticket: Ticket, output_path: str = None) -> Optional[str]:
        """Generate a PDF ticket."""
        if not REPORTLAB_AVAILABLE:
            print("Warning: reportlab not installed. Cannot generate PDF. Install with: pip install reportlab")
            return None
        
        if not output_path:
            output_path = os.path.join(os.path.expanduser("~"), "Desktop", f"Ticket_{ticket.ticket_number}.pdf")
        
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            c = canvas.Canvas(output_path, pagesize=letter)
            width, height = letter
            
            # Header
            c.setFont("Helvetica-Bold", 16)
            c.drawString(inch, height - inch, "SCHOOL CASHIER - QUEUE TICKET")
            
            # Line
            c.setLineWidth(1)
            c.line(inch, height - 1.3*inch, width - inch, height - 1.3*inch)
            
            # Ticket number (large)
            c.setFont("Helvetica-Bold", 48)
            c.drawString(2*inch, height - 2.5*inch, ticket.ticket_number)
            
            # Details
            c.setFont("Helvetica", 12)
            y = height - 3.5*inch
            c.drawString(inch, y, f"Customer: {ticket.customer_name}")
            y -= 0.3*inch
            c.drawString(inch, y, f"Department: {ticket.department}")
            y -= 0.3*inch
            c.drawString(inch, y, f"Priority: {self._get_priority_label(ticket.priority)}")
            y -= 0.3*inch
            c.drawString(inch, y, f"Time: {self._format_time(ticket.issued_at)}")
            y -= 0.3*inch
            c.drawString(inch, y, f"Status: {ticket.status.upper()}")
            
            # Footer
            y -= 0.5*inch
            c.setFont("Helvetica-Oblique", 8)
            c.drawString(inch, y, "Please keep this ticket safe. Your ticket will expire after 2 hours.")
            
            c.save()
            return output_path
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return None
    
    def generate_text_ticket(self, ticket: Ticket) -> str:
        """Generate text representation of ticket."""
        text = "=" * 50 + "\n"
        text += "SCHOOL CASHIER - QUEUE TICKET\n"
        text += "=" * 50 + "\n\n"
        text += f"TICKET NUMBER: {ticket.ticket_number}\n"
        text += f"Customer: {ticket.customer_name}\n"
        text += f"Department: {ticket.department}\n"
        text += f"Priority: {self._get_priority_label(ticket.priority)}\n"
        text += f"Issued: {self._format_time(ticket.issued_at)}\n"
        text += f"Status: {ticket.status.upper()}\n"
        if ticket.notes:
            text += f"Notes: {ticket.notes}\n"
        text += "\n" + "=" * 50 + "\n"
        text += "Please keep this ticket safe.\n"
        text += "Your ticket will expire after 2 hours.\n"
        text += "=" * 50 + "\n"
        return text
    
    def save_ticket_to_file(self, ticket: Ticket, output_path: str = None) -> Optional[str]:
        """Save ticket as text file."""
        if not output_path:
            output_path = os.path.join(os.path.expanduser("~"), "Desktop", f"Ticket_{ticket.ticket_number}.txt")
        
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(self.generate_text_ticket(ticket))
            return output_path
        except Exception as e:
            print(f"Error saving ticket: {e}")
            return None
    
    def get_ticket_summary(self, ticket: Ticket) -> str:
        """Get a summary of ticket."""
        return f"{ticket.ticket_number} - {ticket.customer_name} ({ticket.status})"
