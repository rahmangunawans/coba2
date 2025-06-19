# AniFlix - Premium Anime & Movie Streaming Platform

## Overview

AniFlix is a Flask-based streaming platform for anime series and movies with subscription-based access control. The application provides a Netflix-like experience with user authentication, content management, and tiered subscription plans.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with responsive design
- **CSS Framework**: TailwindCSS for modern styling
- **JavaScript**: Minimal client-side logic for UI interactions
- **Icons**: Font Awesome for consistent iconography
- **Responsive Design**: Mobile-first approach with grid layouts

### Backend Architecture
- **Framework**: Flask web framework
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy extension
- **Authentication**: Flask-Login for session management
- **Form Handling**: Flask-WTF with WTForms for secure form processing
- **Password Security**: Werkzeug for password hashing
- **WSGI Server**: Gunicorn for production deployment

### Database Schema
- **Users**: Authentication, subscription management, watch history
- **Content Structure**: Hierarchical anime (series → seasons → episodes) and standalone movies
- **Subscription System**: Free, regular, and VIP tiers with usage tracking
- **Watch History**: User viewing patterns and progress tracking

## Key Components

### User Management
- Registration and login system with email validation
- Subscription tiers: Free (limited), Regular, and VIP
- Admin role system for content management
- Session-based authentication with secure password hashing

### Content Management
- **Anime Series**: Multi-season structure with episode organization
- **Movies**: Standalone content with preview limitations for free users
- **Torrent Integration**: Links to external streaming sources
- **Metadata**: Titles, descriptions, genres, ratings, and thumbnails

### Subscription System
- **Free Tier**: 5 episodes per day, 10-minute movie previews
- **Regular Tier**: Unlimited anime, full movies, 1 device
- **VIP Tier**: All Regular features plus 2 concurrent devices
- Pricing structure with multi-month discounts

### Admin Panel
- Content addition and management interface
- User statistics and subscription tracking
- Hierarchical content creation (anime → seasons → episodes)

## Data Flow

1. **User Authentication**: Login/registration → session creation → role-based access
2. **Content Discovery**: Browse/search → filtering by genre/type → content selection
3. **Streaming Access**: Subscription validation → usage limit checks → torrent link provision
4. **Watch History**: Stream initiation → progress tracking → recommendation data
5. **Admin Operations**: Admin authentication → content CRUD operations → metadata management

## External Dependencies

### Python Packages
- **Flask**: Core web framework
- **Flask-SQLAlchemy**: Database ORM integration
- **Flask-Login**: User session management
- **Flask-WTF**: Secure form handling
- **Gunicorn**: Production WSGI server
- **Psycopg2**: PostgreSQL database adapter
- **Email-validator**: Email format validation

### Frontend Libraries
- **TailwindCSS**: Utility-first CSS framework (CDN)
- **Font Awesome**: Icon library (CDN)
- **Google Fonts**: Poppins font family

### Infrastructure
- **PostgreSQL**: Primary database (configurable)
- **SQLite**: Development database fallback

## Deployment Strategy

### Production Configuration
- **Runtime**: Python 3.11 with Nix package management
- **Web Server**: Gunicorn with auto-scaling deployment
- **Database**: PostgreSQL with connection pooling
- **Port Configuration**: 5000 with proper port forwarding
- **Security**: ProxyFix middleware for reverse proxy support

### Environment Variables
- `SESSION_SECRET`: Flask session encryption key
- `DATABASE_URL`: Database connection string
- Development defaults provided for local testing

### Deployment Features
- Auto-scaling deployment target
- Reuse-port configuration for zero-downtime deployments
- Health check via port waiting
- Automatic database table creation on startup

## Recent Changes
- June 19, 2025: Initial platform setup with authentication and subscription system
- June 19, 2025: Added trailer support for both anime and movies
- June 19, 2025: Implemented movie parts system for multi-part streaming
- June 19, 2025: Enhanced admin panel with detailed content management
- June 19, 2025: Fixed template errors and improved content display
- June 19, 2025: Added sample data with working torrent links and trailers

## User Preferences

Preferred communication style: Simple, everyday language.