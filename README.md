# EcoLogic - Environmental Issue Reporting System

A Django-based web application for citizens to report environmental issues and for staff to manage and resolve them. The system includes a gamification element with points, rewards, and leaderboards to encourage community participation.

## Features

### For Citizens
- Report environmental issues with photos and location data
- View public issue board with bounty rewards
- Accept and resolve issues for monetary rewards
- Track personal points and rewards
- View leaderboard rankings

### For Staff
- Manage reported issues (pending, in progress, resolved)
- Publish issues to public board with bounties
- Monitor analytics and category statistics
- Manage monetary rewards for citizens
- Access staff dashboard with comprehensive issue overview

### For Admins
- Full administrative access to all system data
- User management and system configuration
- Advanced analytics and reporting

## Project Structure

```
ecologic/
├── citizens/          # Citizen-facing functionality
├── staff/            # Staff management interface
├── issues/           # Core issue reporting system
├── templates/        # Global templates
├── static/           # Static files (CSS, JS, images)
├── media/            # User-uploaded files
└── db.sqlite3        # SQLite database
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Django 4.2 or higher
- Git

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mzaid212005/eco.git
   cd eco
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install django
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create staff accounts:**
   ```bash
   python create_staff_logins.py
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/
   - Staff login: http://127.0.0.1:8000/staff/login/

## Default Staff Accounts

After running `create_staff_logins.py`, you can log in with these credentials:

- **Staff 1:**
  - Username: `staff1`
  - Password: `password123`

- **Staff 2:**
  - Username: `staff2`
  - Password: `password123`

## Usage

### Reporting Issues
1. Citizens can register/login at the main site
2. Fill out the issue reporting form with:
   - Issue title and description
   - Category selection
   - Location information
   - Photo upload (required)
3. Submit the issue for staff review

### Staff Workflow
1. Log in using staff credentials
2. View all reported issues on the dashboard
3. Update issue status (Pending → In Progress → Resolved)
4. Publish issues to public board with bounties
5. Manage citizen rewards and payments

### Public Board
- Citizens can browse issues with bounties
- Accept issues to work on them
- Earn rewards upon successful resolution
- Track progress and earnings

## Key Models

### User Types
- **Citizen**: Can report and resolve issues
- **Staff**: Can manage issues and rewards
- **Admin**: Full system access

### Core Entities
- **Issue**: Environmental problem reports
- **Category**: Issue classification (e.g., Pollution, Waste, Wildlife)
- **UserProfile**: Extended user information with points and rewards
- **MonetaryReward**: Financial incentives for issue resolution
- **Reward**: Point-based rewards system

## API Endpoints

### Main Routes
- `/` - Home page and issue reporting
- `/citizens/` - Citizen registration and dashboard
- `/staff/` - Staff login and management
- `/public-board/` - Public issue board with bounties
- `/leaderboard/` - User rankings and statistics

### Staff Routes
- `/staff/dashboard/` - Issue management dashboard
- `/staff/manage-rewards/` - Reward administration

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Static Files
```bash
python manage.py collectstatic
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Technologies Used

- **Backend**: Django 4.2
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Django's built-in auth system
- **File Storage**: Local filesystem with Django's media handling

## Future Enhancements

- [ ] Mobile app development
- [ ] Advanced analytics dashboard
- [ ] Integration with mapping services
- [ ] Automated issue categorization using AI
- [ ] Notification system for issue updates
- [ ] Social features for community engagement