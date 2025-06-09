# Pool Games Matchmaking and Event Portal

A Django-based web platform that connects pool game enthusiasts, enabling them to register, find opponents, organize matches, and stay updated with events and tournaments.

## Features

### User Management
- **Dual Registration**: Users can register as Players or Referees
- **Player Profiles**: Full name, username, email, location, profile photos, bio, skill levels
- **Referee Profiles**: Basic information for match officiating
- **Secure Authentication**: Django's built-in authentication system

### Player Directory
- Browse all registered players
- View player cards with photos, skill levels, and bios
- Challenge players directly from their profiles

### Match System
- **Match Creation**: Players can create match requests
- **Match Details**: Opponent selection, venue, date, time, bid amount
- **Confirmation System**: Opponents must confirm match requests
- **Match Management**: View, confirm, or cancel matches
- **AJAX Integration**: Real-time match actions without page reload

### Event Management
- **Admin Event Creation**: Admins can create and manage events
- **Event Posters**: Upload and display event images
- **Homepage Features**: Selected events displayed on homepage
- **Dedicated Events Page**: Complete list of upcoming events
- **Auto-cleanup**: Past events are automatically filtered out

### Admin Features
- **Venue Management**: Only admins can add pool venues
- **Event Management**: Create, edit, and delete events
- **User Management**: Full admin control over users and profiles

## Technology Stack

- **Backend**: Django 4.2.7 (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Bootstrap 5.1.3
- **Database**: SQLite (development), MySQL (production ready)
- **Authentication**: Django Auth System
- **File Handling**: Django Media & FileField for image uploads
- **AJAX**: JavaScript Fetch API for dynamic interactions

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Quick Start

1. **Clone or download the project files**

2. **Install dependencies**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Run database migrations**
   \`\`\`bash
   python manage.py makemigrations
   python manage.py migrate
   \`\`\`

4. **Create sample data (optional but recommended)**
   \`\`\`bash
   python scripts/setup_database.py
   \`\`\`

5. **Create a superuser (if not using sample data)**
   \`\`\`bash
   python manage.py createsuperuser
   \`\`\`

6. **Run the development server**
   \`\`\`bash
   python manage.py runserver
   \`\`\`

7. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

### Sample Data

The setup script creates:
- **Admin user**: username `admin`, password `admin123`
- **4 sample players** with different skill levels
- **2 sample referees**
- **4 pool venues** in different locations
- **4 upcoming events** including tournaments and workshops

All sample players use password: `password123`

## Usage Guide

### For Players
1. **Register** as a Player with your details
2. **Complete your profile** with bio and skill level
3. **Browse the player directory** to find opponents
4. **Create match requests** with venue, time, and bid details
5. **Manage your matches** - confirm incoming requests or cancel if needed
6. **Stay updated** with events and tournaments

### For Referees
1. **Register** as a Referee
2. **Update your profile** with experience and certifications
3. **View upcoming matches** that may need officiating

### For Admins
1. **Access the admin panel** at `/admin/`
2. **Add venues** where matches can be played
3. **Create events** and upload promotional posters
4. **Manage users** and their profiles
5. **Monitor match activities**

## Project Structure

\`\`\`
pool_portal/
├── pool_portal/          # Main project settings
├── accounts/             # User management and profiles
├── matches/              # Match creation and management
├── events/               # Event and tournament management
├── templates/            # HTML templates
├── static/               # CSS, JS, and static assets
├── media/                # User uploaded files
└── scripts/              # Database setup and utilities
\`\`\`

## Key Models

- **User**: Custom user model with Player/Referee roles
- **PlayerProfile**: Extended profile for players
- **RefereeProfile**: Basic profile for referees
- **Venue**: Pool halls and playing locations
- **Match**: Match requests and confirmations
- **Event**: Tournaments and special events

## Security Features

- CSRF protection on all forms
- User authentication required for sensitive actions
- File upload validation for images
- SQL injection protection via Django ORM
- XSS protection through template escaping

## Responsive Design

- Mobile-first Bootstrap implementation
- Responsive navigation and layouts
- Touch-friendly buttons and interactions
- Optimized for all device sizes

## Future Enhancements

- **Payment Integration**: Handle bid money through payment gateways
- **Match Results**: Record and display match outcomes
- **Rating System**: Player ratings based on match results
- **Chat System**: Real-time messaging between players
- **Tournament Brackets**: Advanced tournament management
- **Notifications**: Email/SMS notifications for match updates
- **Geolocation**: Find nearby players and venues
- **Mobile App**: Native mobile application

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please create an issue in the project repository or contact the development team.
