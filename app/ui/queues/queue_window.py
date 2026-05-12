# Ticket generation screen
import tkinter as tk
from tkinter import messagebox, ttk
from app.utils.constants import COLORS, FONTS, DEPARTMENTS
from app.ui.components.widgets import StyledButton, InputField, StatusBadge
from app.services.queue_service import QueueService
from app.services.ticket_service import TicketService
from app.database.db_manager import DatabaseManager

class TicketGenerationWindow(tk.Toplevel):
    """Window for generating new tickets."""
    
    def __init__(self, parent):
        """Initialize ticket generation window."""
        super().__init__(parent)
        
        self.title("Generate New Ticket")
        self.geometry("600x500")
        self.configure(bg=COLORS['light'])
        
        self.db = DatabaseManager()
        self.queue_service = QueueService(self.db)
        self.ticket_service = TicketService(self.db)
        
        self.generated_ticket = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create window widgets."""
        # Header
        header = tk.Label(
            self,
            text="Generate New Ticket",
            font=FONTS['title'],
            bg=COLORS['primary'],
            fg='white',
            pady=10
        )
        header.pack(fill=tk.X)
        
        # Form frame
        form_frame = tk.Frame(self, bg='white', padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Customer name
        self.name_field = InputField(
            form_frame,
            label="Customer Name:",
            placeholder="Enter customer name"
        )
        self.name_field.pack(fill=tk.X, pady=10)
        
        # Department selection
        dept_label = tk.Label(
            form_frame,
            text="Department/Counter:",
            font=FONTS['normal'],
            bg='white',
            fg=COLORS['text']
        )
        dept_label.pack(anchor='w', pady=(10, 0))
        
        self.dept_var = tk.StringVar(value=DEPARTMENTS[0])
        dept_dropdown = ttk.Combobox(
            form_frame,
            textvariable=self.dept_var,
            values=DEPARTMENTS,
            state='readonly',
            font=FONTS['normal'],
            width=40
        )
        dept_dropdown.pack(fill=tk.X, pady=5)
        
        # Priority selection
        priority_label = tk.Label(
            form_frame,
            text="Priority:",
            font=FONTS['normal'],
            bg='white',
            fg=COLORS['text']
        )
        priority_label.pack(anchor='w', pady=(10, 0))
        
        self.priority_var = tk.StringVar(value="5 - Normal")
        priority_options = [
            "1 - High Priority",
            "2 - Senior Citizen",
            "3 - PWD (Persons with Disability)",
            "4 - Pregnant",
            "5 - Normal"
        ]
        priority_dropdown = ttk.Combobox(
            form_frame,
            textvariable=self.priority_var,
            values=priority_options,
            state='readonly',
            font=FONTS['normal'],
            width=40
        )
        priority_dropdown.pack(fill=tk.X, pady=5)
        
        # Notes
        notes_label = tk.Label(
            form_frame,
            text="Notes (Optional):",
            font=FONTS['normal'],
            bg='white',
            fg=COLORS['text']
        )
        notes_label.pack(anchor='w', pady=(10, 0))
        
        self.notes_text = tk.Text(
            form_frame,
            height=3,
            font=FONTS['normal'],
            border=1,
            relief=tk.FLAT
        )
        self.notes_text.pack(fill=tk.X, pady=5)
        
        # Button frame
        button_frame = tk.Frame(form_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=20)
        
        generate_btn = StyledButton(
            button_frame,
            text="Generate Ticket",
            command=self._generate_ticket,
            style='success',
            width=15
        )
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = StyledButton(
            button_frame,
            text="Cancel",
            command=self.destroy,
            style='danger',
            width=15
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Result frame (hidden by default)
        self.result_frame = tk.Frame(form_frame, bg='white')
        
        self.result_label = tk.Label(
            self.result_frame,
            text="Ticket Generated Successfully!",
            font=FONTS['subtitle'],
            bg='white',
            fg=COLORS['success']
        )
        self.result_label.pack(pady=10)
        
        self.ticket_number_label = tk.Label(
            self.result_frame,
            text="",
            font=FONTS['ticket_large'],
            bg='white',
            fg=COLORS['primary']
        )
        self.ticket_number_label.pack(pady=10)
        
        self.ticket_info_label = tk.Label(
            self.result_frame,
            text="",
            font=FONTS['normal'],
            bg='white'
        )
        self.ticket_info_label.pack(pady=10)
        
        # Print button in result frame
        self.print_btn = StyledButton(
            self.result_frame,
            text="Print Ticket",
            command=self._print_ticket,
            style='info'
        )
        self.print_btn.pack(pady=5)
    
    def _generate_ticket(self):
        """Generate new ticket."""
        # Validate input
        customer_name = self.name_field.get().strip()
        if not customer_name:
            messagebox.showerror("Error", "Please enter customer name")
            return
        
        department = self.dept_var.get()
        priority = int(self.priority_var.get().split()[0])
        notes = self.notes_text.get("1.0", tk.END).strip()
        
        # Generate ticket
        self.generated_ticket = self.queue_service.enqueue_ticket(
            department, customer_name, priority, notes
        )
        
        if self.generated_ticket:
            # Hide form and show result
            self.result_frame.pack(fill=tk.BOTH, expand=True, pady=20)
            
            self.ticket_number_label.config(
                text=self.generated_ticket.ticket_number
            )
            
            self.ticket_info_label.config(
                text=f"Name: {customer_name}\nDepartment: {department}\nPriority: {self._get_priority_label(priority)}"
            )
            
            messagebox.showinfo("Success", f"Ticket {self.generated_ticket.ticket_number} generated successfully!")
        else:
            messagebox.showerror("Error", "Failed to generate ticket")
    
    def _print_ticket(self):
        """Print/save ticket."""
        if self.generated_ticket:
            output_path = self.ticket_service.save_ticket_to_file(self.generated_ticket)
            if output_path:
                messagebox.showinfo("Success", f"Ticket saved to:\n{output_path}")
            else:
                messagebox.showerror("Error", "Failed to save ticket")
    
    @staticmethod
    def _get_priority_label(priority: int) -> str:
        """Get priority label."""
        labels = {1: "High Priority", 2: "Senior Citizen", 3: "PWD", 4: "Pregnant", 5: "Normal"}
        return labels.get(priority, "Normal")
