# Staff controls (call, skip, recall, complete)
import tkinter as tk
from tkinter import messagebox, ttk
from app.utils.constants import COLORS, FONTS, DEPARTMENTS
from app.ui.components.widgets import StyledButton, InputField, TicketCard
from app.services.queue_service import QueueService
from app.services.auth_service import AuthService
from app.database.db_manager import DatabaseManager

class AdminPanel(tk.Toplevel):
    """Admin panel for managing queue."""
    
    def __init__(self, parent):
        """Initialize admin panel."""
        super().__init__(parent)
        
        self.title("Admin Panel - Queue Control")
        self.geometry("900x600")
        self.configure(bg=COLORS['light'])
        
        self.db = DatabaseManager()
        self.queue_service = QueueService(self.db)
        self.auth_service = AuthService(self.db)
        
        self.current_session = None
        self.selected_queue_id = None
        
        self._create_login_window()
    
    def _create_login_window(self):
        """Create login window."""
        # Clear window
        for widget in self.winfo_children():
            widget.destroy()
        
        # Login frame
        login_frame = tk.Frame(self, bg='white')
        login_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Label(
            login_frame,
            text="Admin Login",
            font=FONTS['header'],
            bg=COLORS['primary'],
            fg='white',
            pady=20
        )
        header.pack(fill=tk.X)
        
        # Form
        form_container = tk.Frame(login_frame, bg='white')
        form_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Username
        self.username_field = InputField(
            form_container,
            label="Username:",
            placeholder="Enter username"
        )
        self.username_field.pack(fill=tk.X, pady=20)
        
        # Password
        self.password_field = InputField(
            form_container,
            label="Password:",
            placeholder="Enter password",
            input_type="password"
        )
        self.password_field.pack(fill=tk.X, pady=20)
        
        # Login button
        login_btn = StyledButton(
            form_container,
            text="Login",
            command=self._login,
            style='secondary',
            width=20
        )
        login_btn.pack(pady=20)
        
        # Demo credentials label
        demo_label = tk.Label(
            form_container,
            text="Demo: username=admin, password=admin123",
            font=FONTS['small'],
            bg='white',
            fg=COLORS['text']
        )
        demo_label.pack(pady=10)
    
    def _login(self):
        """Handle login."""
        username = self.username_field.get().strip()
        password = self.password_field.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        success, session, message = self.auth_service.login(username, password)
        
        if success:
            self.current_session = session
            self._create_control_panel()
        else:
            messagebox.showerror("Login Failed", message)
    
    def _create_control_panel(self):
        """Create control panel after login."""
        # Clear window
        for widget in self.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = tk.Frame(self, bg=COLORS['primary'])
        header_frame.pack(fill=tk.X)
        
        header_label = tk.Label(
            header_frame,
            text=f"Admin Panel - {self.current_session.username}",
            font=FONTS['title'],
            bg=COLORS['primary'],
            fg='white',
            padx=20,
            pady=10
        )
        header_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        logout_btn = StyledButton(
            header_frame,
            text="Logout",
            command=self._logout,
            style='danger',
            width=10
        )
        logout_btn.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Main content
        main_frame = tk.Frame(self, bg=COLORS['light'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left sidebar - Department selection
        sidebar = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=1)
        sidebar.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        dept_label = tk.Label(
            sidebar,
            text="Select Counter",
            font=FONTS['subtitle'],
            bg=COLORS['secondary'],
            fg='white',
            pady=10
        )
        dept_label.pack(fill=tk.X)
        
        self.dept_frame = tk.Frame(sidebar, bg='white')
        self.dept_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._load_departments()
        
        # Right side - Controls
        control_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=1)
        control_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Current ticket display
        current_label = tk.Label(
            control_frame,
            text="Currently Serving",
            font=FONTS['subtitle'],
            bg=COLORS['warning'],
            fg='white',
            pady=10
        )
        current_label.pack(fill=tk.X)
        
        self.current_ticket_frame = tk.Frame(control_frame, bg='white')
        self.current_ticket_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Control buttons
        button_frame = tk.Frame(control_frame, bg='white')
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        call_next_btn = StyledButton(
            button_frame,
            text="Call Next",
            command=self._call_next,
            style='success',
            height=2
        )
        call_next_btn.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        
        skip_btn = StyledButton(
            button_frame,
            text="Skip",
            command=self._skip_ticket,
            style='warning',
            height=2
        )
        skip_btn.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        
        recall_btn = StyledButton(
            button_frame,
            text="Recall",
            command=self._recall_ticket,
            style='info',
            height=2
        )
        recall_btn.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        
        complete_btn = StyledButton(
            button_frame,
            text="Complete",
            command=self._complete_ticket,
            style='success',
            height=2
        )
        complete_btn.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        
        # Queue info
        queue_info_label = tk.Label(
            control_frame,
            text="Queue Information",
            font=FONTS['subtitle'],
            bg=COLORS['secondary'],
            fg='white',
            pady=10
        )
        queue_info_label.pack(fill=tk.X)
        
        self.queue_info_frame = tk.Frame(control_frame, bg='white')
        self.queue_info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Update display
        self._update_display()
        self.after(1000, self._update_display)
    
    def _load_departments(self):
        """Load department buttons."""
        for widget in self.dept_frame.winfo_children():
            widget.destroy()
        
        queues = self.queue_service.get_all_queues_status()
        
        if not queues:
            from app.services.queue_service import QueueService
            qs = QueueService(self.db)
            for dept in DEPARTMENTS:
                qs.enqueue_ticket(dept, "Sample", 5)
                queue = self.db.get_queue_by_department(dept)
                if queue:
                    self.db.delete_queue(queue.queue_id)
            queues = self.queue_service.get_all_queues_status()
        
        for queue_status in queues:
            btn = tk.Button(
                self.dept_frame,
                text=f"{queue_status['department']}\n({queue_status['waiting_count']} waiting)",
                font=FONTS['normal'],
                bg=COLORS['secondary'],
                fg='white',
                pady=10,
                cursor='hand2',
                command=lambda q=queue_status: self._select_queue(q)
            )
            btn.pack(fill=tk.X, pady=5)
    
    def _select_queue(self, queue_status):
        """Select a queue."""
        self.selected_queue_id = queue_status['queue_id']
        self._update_display()
    
    def _update_display(self):
        """Update display."""
        if not self.selected_queue_id:
            return
        
        # Update current ticket
        for widget in self.current_ticket_frame.winfo_children():
            widget.destroy()
        
        status = self.queue_service.get_queue_status(self.selected_queue_id)
        current = status.get('current_ticket')
        
        if current:
            card = TicketCard(
                self.current_ticket_frame,
                {
                    'ticket_number': current['ticket_number'],
                    'customer_name': current['customer_name'],
                    'department': current['department'],
                    'status': current['status']
                }
            )
            card.pack(fill=tk.BOTH, expand=True)
        else:
            no_ticket = tk.Label(
                self.current_ticket_frame,
                text="No ticket being served",
                font=FONTS['subtitle'],
                bg='white',
                fg=COLORS['text']
            )
            no_ticket.pack(pady=20)
        
        # Update queue info
        for widget in self.queue_info_frame.winfo_children():
            widget.destroy()
        
        info_text = f"""
Waiting: {status['waiting_count']}
Total: {status['total_tickets']}
Department: {status['department']}
        """
        
        info_label = tk.Label(
            self.queue_info_frame,
            text=info_text.strip(),
            font=FONTS['normal'],
            bg='white',
            justify=tk.LEFT
        )
        info_label.pack(anchor='w', padx=10, pady=10)
        
        self.after(1000, self._update_display)
    
    def _call_next(self):
        """Call next ticket."""
        if not self.selected_queue_id:
            messagebox.showwarning("Warning", "Please select a counter")
            return
        
        ticket = self.queue_service.call_next_ticket(self.selected_queue_id)
        if ticket:
            messagebox.showinfo("Success", f"Calling ticket {ticket.ticket_number}")
        else:
            messagebox.showinfo("Info", "No more tickets in queue")
    
    def _skip_ticket(self):
        """Skip current ticket."""
        if not self.selected_queue_id:
            messagebox.showwarning("Warning", "Please select a counter")
            return
        
        status = self.queue_service.get_queue_status(self.selected_queue_id)
        current = status.get('current_ticket')
        
        if current:
            self.queue_service.skip_ticket(self.selected_queue_id, current['ticket_id'])
            messagebox.showinfo("Success", "Ticket skipped")
        else:
            messagebox.showwarning("Warning", "No ticket is being served")
    
    def _recall_ticket(self):
        """Recall ticket."""
        if not self.selected_queue_id:
            messagebox.showwarning("Warning", "Please select a counter")
            return
        
        status = self.queue_service.get_queue_status(self.selected_queue_id)
        current = status.get('current_ticket')
        
        if current:
            self.queue_service.recall_ticket(self.selected_queue_id, current['ticket_id'])
            messagebox.showinfo("Success", "Ticket recalled")
        else:
            messagebox.showwarning("Warning", "No ticket is being served")
    
    def _complete_ticket(self):
        """Complete ticket."""
        if not self.selected_queue_id:
            messagebox.showwarning("Warning", "Please select a counter")
            return
        
        status = self.queue_service.get_queue_status(self.selected_queue_id)
        current = status.get('current_ticket')
        
        if current:
            self.queue_service.complete_ticket(self.selected_queue_id, current['ticket_id'])
            messagebox.showinfo("Success", "Ticket completed")
        else:
            messagebox.showwarning("Warning", "No ticket is being served")
    
    def _logout(self):
        """Logout."""
        if self.current_session:
            self.auth_service.logout(self.current_session.session_id)
        self._create_login_window()
