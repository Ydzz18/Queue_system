# School Cashier Queue Management System

A comprehensive queue management system built with Python and Tkinter for managing student queues in school cashier operations.

## Features

### 1. **Ticket Generation**
   - Generate tickets with customer name, department/counter selection
   - Priority levels: High Priority, Senior Citizen, PWD, Pregnant, Normal
   - Optional notes for special requests
   - Automatic ticket numbering

### 2. **Queue Management Dashboard**
   - Real-time display of current and next tickets for all counters
   - Queue status showing number of waiting customers
   - Live updates (1-second refresh rate)
   - Multiple department/counter support

### 3. **Admin Panel**
   - Secure login system with username/password authentication
   - Call next ticket functionality
   - Skip ticket option
   - Recall ticket feature
   - Complete ticket marking
   - Queue statistics and information display

### 4. **Data Management**
   - JSON-based database for data persistence
   - Complete ticket history tracking
   - User management with role-based access (admin, manager, cashier)
   - Session management with automatic expiry

### 5. **Ticket Printing**
   - Save tickets as text files
   - PDF generation support (optional)
   - Print-friendly ticket format

## Project Structure

```
Queue-System/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── app/
│   ├── ui/
│   │   ├── dashboard.py          # Main queue display
│   │   ├── queues/
│   │   │   ├── queue_window.py   # Ticket generation
│   │   │   └── admin_panel.py    # Admin controls
│   │   └── components/
│   │       └── widgets.py        # Reusable UI components
│   ├── services/
│   │   ├── queue_service.py      # Queue operations
│   │   ├── ticket_service.py     # Ticket management
│   │   └── auth_service.py       # Authentication
│   ├── models/
│   │   ├── queue.py              # Queue data structures
│   │   └── user.py               # User data structures
│   ├── database/
│   │   └── db_manager.py         # JSON database CRUD
│   └── utils/
│       ├── constants.py          # Configuration
│       ├── validators.py         # Input validation
│       └── helpers.py            # Utility functions
└── data/
    └── queue_data.json          # Database file (auto-created)
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone or download the project**
   ```bash
   cd Queue-System
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## Usage

### Starting the Application

```bash
python main.py
```

The dashboard will open showing the queue status for all counters.

### Generating a Ticket

1. Click "Generate New Ticket" button
2. Enter customer name
3. Select department/counter
4. Choose priority level
5. Add optional notes
6. Click "Generate Ticket"
7. Optionally print the ticket

### Admin Operations

1. Click "Admin Panel" on dashboard
2. Login with credentials:
   - Default Username: `admin`
   - Default Password: `admin123`
3. Select a counter from the list
4. Use control buttons:
   - **Call Next**: Call the next waiting ticket
   - **Skip**: Skip current ticket
   - **Recall**: Move ticket back to waiting queue
   - **Complete**: Mark ticket as completed

## Configuration

Edit `app/utils/constants.py` to customize:
- Colors and fonts
- Window dimensions
- Queue settings
- Department/counter names
- Admin credentials

## Database

The system uses JSON files for data storage:
- Location: `data/queue_data.json`
- Auto-creates on first run
- Stores: Queues, Tickets, Users, Sessions, History

## Demo Credentials

- **Username**: `admin`
- **Password**: `admin123`

## Features Overview

### Ticket Status Lifecycle
- **Waiting**: Newly generated ticket
- **Called**: Currently being served
- **Completed**: Transaction finished
- **Skipped**: Ticket skipped for priority
- **Expired**: Ticket validity expired

### Priority Levels
- **1 - High Priority**: Emergency cases
- **2 - Senior Citizen**: Elderly customers
- **3 - PWD**: Persons with Disability
- **4 - Pregnant**: Pregnant customers
- **5 - Normal**: Regular customers

### User Roles
- **Admin**: Full system access
- **Manager**: Queue management
- **Cashier**: Basic operations

## Security Features

- Password hashing using SHA-256
- Session management with 24-hour expiry
- User authentication and authorization
- Audit trail of all operations

## Tips & Best Practices

1. **Ticket Expiry**: Tickets automatically expire after 2 hours
2. **Backup**: Regularly backup `queue_data.json`
3. **Performance**: System supports up to 200 tickets per queue
4. **Monitoring**: Check Admin Panel for real-time queue status
5. **Priority**: Always serve priority customers first

## Troubleshooting

### Application Won't Start
- Ensure Python 3.8+ is installed
- Install all dependencies: `pip install -r requirements.txt`
- Check for port conflicts

### No Data Saving
- Check `data/` directory permissions
- Ensure `queue_data.json` is writable
- Clear corrupted JSON and restart

### Login Issues
- Reset password using command: `python -c "from app.services.auth_service import AuthService; from app.database.db_manager import DatabaseManager; a = AuthService(DatabaseManager()); a.reset_password('<user_id>', 'newpassword')"`
- Default admin can't be deleted

## Future Enhancements

- SMS/Email notifications
- Mobile app integration
- Multi-location support
- Advanced analytics and reporting
- Voice/Audio queue announcements
- Integration with payment systems
- Customer satisfaction surveys
- Real-time queue predictions

## Support

For issues or feature requests, refer to the code documentation or contact system administrator.

## License

This project is provided as-is for educational purposes.

## Version

Version 1.0.0 - Initial Release
