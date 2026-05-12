#!/usr/bin/env python3
"""
School Cashier Queue Management System
Main entry point for the application
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.ui.dashboard import Dashboard

def main():
    """Main entry point."""
    print("Starting School Cashier Queue System...")
    app = Dashboard()
    app.mainloop()

if __name__ == "__main__":
    main()
