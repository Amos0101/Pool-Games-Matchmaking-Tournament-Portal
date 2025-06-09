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

- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, JavaScript 
- **Styling**: Bootstrap
- **Database**: SQLite (development), MySQL (production ready)
- **Authentication**: Django Auth System
- **File Handling**: Django Media & FileField for image uploads
- **AJAX**: JavaScript Fetch API for dynamic interactions

## Security Features

- CSRF protection on all forms
- User authentication required for sensitive actions
- File upload validation for images
- SQL injection protection via Django ORM
- XSS protection through template escaping



## Future Enhancements

- **Payment Integration**: Handle bid money through payment gateways
- **Match Results**: Record and display match outcomes
- **Rating System**: Player ratings based on match results
- **Chat System**: Real-time messaging between players
- **Tournament Brackets**: Advanced tournament management
- **Notifications**: Email/SMS notifications for match updates
- **Geolocation**: Find nearby players and venues
- **Mobile App**: Native mobile application


