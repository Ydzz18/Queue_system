# Main view showing current/next tickets
import tkinter as tk
from tkinter import ttk, messagebox
from app.utils.constants import COLORS, FONTS, WINDOW_WIDTH, WINDOW_HEIGHT, DEPARTMENTS
from app.ui.components.widgets import TicketCard, InfoCard, StyledButton
from app.services.queue_service import QueueService
from app.database.db_manager import DatabaseManager
import threading

class Dashboard(tk.Tk):
    """Main dashboard showing queue status."""
    
    def __init__(self):
        """Initialize dashboard."""
        super().__init__()
        
        self.title("School Cashier - Queue System")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.configure(bg=COLORS['light'])
        
        self.db = DatabaseManager()
        self.queue_service = QueueService(self.db)
        
        self._create_widgets()
        self._update_display()
        
        # Auto-update every 1 second
        self.after(1000, self._update_display)
    
    def _create_widgets(self):
        """Create dashboard widgets."""
        # Header
        header_frame = tk.Frame(self, bg=COLORS['primary'], height=60)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(
            header_frame,
            text="SCHOOL CASHIER - QUEUE MANAGEMENT SYSTEM",
            font=FONTS['header'],
            fg='white',
            bg=COLORS['primary']
        )
        header_label.pack(pady=10)
        
        # Main content frame
        main_frame = tk.Frame(self, bg=COLORS['light'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Queue status section
        queues_label = tk.Label(
            main_frame,
            text="QUEUE STATUS",
            font=FONTS['subtitle'],
            bg=COLORS['light']
        )
        queues_label.pack(anchor='w', pady=(0, 10))
        
        # Queue scrollable frame
        canvas = tk.Canvas(main_frame, bg=COLORS['light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=COLORS['light'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=COLORS['light'])
        button_frame.pack(fill=tk.X, pady=10)
        
        new_ticket_btn = StyledButton(
            button_frame,
            text="Generate New Ticket",
            command=self._open_ticket_window,
            style='secondary',
            width=20
        )
        new_ticket_btn.pack(side=tk.LEFT, padx=5)
        
        admin_btn = StyledButton(
            button_frame,
            text="Admin Panel",
            command=self._open_admin_panel,
            style='danger',
            width=20
        )
        admin_btn.pack(side=tk.LEFT, padx=5)
    
    def _update_display(self):
        """Update display with current queue status."""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Get queue status for all departments
        statuses = self.queue_service.get_all_queues_status()
        
        if not statuses:
            # Create default queues
            for dept in DEPARTMENTS:
                self.queue_service.enqueue_ticket(dept, "Sample Customer", 5, "Demo")
                self.db.delete_queue(self.db.get_queue_by_department(dept).queue_id)
            statuses = self.queue_service.get_all_queues_status()
        
        # Create ticket cards for each queue
        for status in statuses:
            department = status['department']
            current = status['current_ticket']
            next_ticket = status['next_ticket']
            waiting = status['waiting_count']
            
            # Department frame
            dept_frame = tk.Frame(self.scrollable_frame, bg='white', relief=tk.RAISED, bd=1)
            dept_frame.pack(fill=tk.X, pady=5)
            
            # Department label
            dept_label = tk.Label(
                dept_frame,
                text=f"📍 {department}",
                font=FONTS['subtitle'],
                bg=COLORS['secondary'],
                fg='white',
                padx=10,
                pady=5
            )
            dept_label.pack(fill=tk.X)
            
            # Current ticket
            if current:
                current_label = tk.Label(
                    dept_frame,
                    text="NOW SERVING:",
                    font=FONTS['normal'],
                    bg='white',
                    fg=COLORS['danger']
                )
                current_label.pack(anchor='w', padx=10, pady=(10, 0))
                
                current_card = TicketCard(
                    dept_frame,
                    {
                        'ticket_number': current['ticket_number'],
                        'customer_name': current['customer_name'],
                        'department': current['department'],
                        'status': current['status']
                    }
                )
                current_card.pack(fill=tk.X, padx=10, pady=5)
            
            # Next ticket
            if next_ticket:
                next_label = tk.Label(
                    dept_frame,
                    text="NEXT:",
                    font=FONTS['normal'],
                    bg='white',
                    fg=COLORS['info']
                )
                next_label.pack(anchor='w', padx=10, pady=(10, 0))
                
                next_card = TicketCard(
                    dept_frame,
                    {
                        'ticket_number': next_ticket['ticket_number'],
                        'customer_name': next_ticket['customer_name'],
                        'department': next_ticket['department'],
                        'status': next_ticket['status']
                    }
                )
                next_card.pack(fill=tk.X, padx=10, pady=5)
            
            # Queue info
            info_label = tk.Label(
                dept_frame,
                text=f"Waiting: {waiting} | Total: {status['total_tickets']}",
                font=FONTS['small'],
                bg='white',
                fg=COLORS['text']
            )
            info_label.pack(anchor='w', padx=10, pady=(5, 10))
        
        # Schedule next update
        self.after(1000, self._update_display)
    
    def _open_ticket_window(self):
        """Open ticket generation window."""
        from app.ui.queues.queue_window import TicketGenerationWindow
        TicketGenerationWindow(self)
    
    def _open_admin_panel(self):
        """Open admin panel."""
        from app.ui.queues.admin_panel import AdminPanel
        AdminPanel(self)


if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
