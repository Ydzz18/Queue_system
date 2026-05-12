# Reusable UI widgets (cards, buttons)
import tkinter as tk
from tkinter import ttk
from app.utils.constants import COLORS, FONTS

class StyledButton(tk.Button):
    """Custom styled button widget."""
    
    def __init__(self, parent, text, command=None, style='primary', width=15, height=2, **kwargs):
        """Initialize styled button."""
        color = COLORS.get(style, COLORS['primary'])
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=color,
            fg='white',
            font=FONTS['normal'],
            padx=10,
            pady=5,
            border=0,
            cursor='hand2',
            activebackground=self._darken_color(color),
            width=width,
            height=height,
            **kwargs
        )
    
    @staticmethod
    def _darken_color(hex_color):
        """Darken a hex color for hover effect."""
        return hex_color

class TicketCard(tk.Frame):
    """Card displaying ticket information."""
    
    def __init__(self, parent, ticket_data, **kwargs):
        """Initialize ticket card."""
        super().__init__(parent, bg='white', relief=tk.RAISED, bd=2, **kwargs)
        
        self.ticket_data = ticket_data
        self._create_widgets()
    
    def _create_widgets(self):
        """Create card widgets."""
        # Ticket number
        ticket_label = tk.Label(
            self,
            text=self.ticket_data.get('ticket_number', 'N/A'),
            font=FONTS['ticket_large'],
            fg=COLORS['primary'],
            bg='white'
        )
        ticket_label.pack(pady=10)
        
        # Customer name
        name_label = tk.Label(
            self,
            text=f"Customer: {self.ticket_data.get('customer_name', 'N/A')}",
            font=FONTS['subtitle'],
            bg='white'
        )
        name_label.pack(pady=5)
        
        # Department
        dept_label = tk.Label(
            self,
            text=f"Department: {self.ticket_data.get('department', 'N/A')}",
            font=FONTS['normal'],
            bg='white'
        )
        dept_label.pack(pady=5)
        
        # Status
        status = self.ticket_data.get('status', 'waiting')
        status_color = {
            'waiting': COLORS['info'],
            'called': COLORS['warning'],
            'completed': COLORS['success'],
            'skipped': COLORS['danger'],
            'expired': COLORS['danger']
        }.get(status, COLORS['info'])
        
        status_label = tk.Label(
            self,
            text=f"Status: {status.upper()}",
            font=FONTS['subtitle'],
            fg='white',
            bg=status_color,
            padx=10,
            pady=5
        )
        status_label.pack(pady=5, fill=tk.X)

class InfoCard(tk.Frame):
    """Card for displaying information."""
    
    def __init__(self, parent, title, value, icon=None, **kwargs):
        """Initialize info card."""
        super().__init__(parent, bg='white', relief=tk.RAISED, bd=1, **kwargs)
        
        self.title = title
        self.value = value
        self.icon = icon
        self._create_widgets()
    
    def _create_widgets(self):
        """Create card widgets."""
        # Title
        title_label = tk.Label(
            self,
            text=self.title,
            font=FONTS['normal'],
            bg='white',
            fg=COLORS['text']
        )
        title_label.pack(pady=5)
        
        # Value
        value_label = tk.Label(
            self,
            text=str(self.value),
            font=FONTS['header'],
            bg='white',
            fg=COLORS['primary']
        )
        value_label.pack(pady=10)

class InputField(tk.Frame):
    """Custom input field with label."""
    
    def __init__(self, parent, label, placeholder="", input_type="text", **kwargs):
        """Initialize input field."""
        super().__init__(parent, bg='white', **kwargs)
        
        self.label_text = label
        self.placeholder = placeholder
        self.input_type = input_type
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create field widgets."""
        # Label
        label = tk.Label(
            self,
            text=self.label_text,
            font=FONTS['normal'],
            bg='white',
            fg=COLORS['text']
        )
        label.pack(anchor='w', padx=5, pady=(5, 0))
        
        # Input
        if self.input_type == 'password':
            self.entry = tk.Entry(
                self,
                show='*',
                font=FONTS['normal'],
                border=1,
                relief=tk.FLAT
            )
        else:
            self.entry = tk.Entry(
                self,
                font=FONTS['normal'],
                border=1,
                relief=tk.FLAT
            )
        
        self.entry.pack(fill=tk.X, padx=5, pady=5)
        
        # Placeholder
        if self.placeholder:
            self.entry.insert(0, self.placeholder)
            self.entry.bind('<FocusIn>', self._on_focus_in)
            self.entry.bind('<FocusOut>', self._on_focus_out)
    
    def _on_focus_in(self, event):
        """Handle focus in event."""
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg='black')
    
    def _on_focus_out(self, event):
        """Handle focus out event."""
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg='gray')
    
    def get(self):
        """Get input value."""
        value = self.entry.get()
        if value == self.placeholder:
            return ""
        return value
    
    def set(self, value):
        """Set input value."""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)

class StatusBadge(tk.Label):
    """Badge for displaying status."""
    
    def __init__(self, parent, status, **kwargs):
        """Initialize status badge."""
        color_map = {
            'waiting': COLORS['info'],
            'called': COLORS['warning'],
            'completed': COLORS['success'],
            'skipped': COLORS['danger'],
            'expired': COLORS['danger'],
            'active': COLORS['success'],
            'inactive': COLORS['danger']
        }
        
        color = color_map.get(status, COLORS['info'])
        
        super().__init__(
            parent,
            text=status.upper(),
            font=FONTS['normal'],
            fg='white',
            bg=color,
            padx=10,
            pady=5,
            **kwargs
        )
