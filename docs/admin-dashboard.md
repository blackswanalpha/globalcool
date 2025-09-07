# Admin Dashboard Documentation

## Overview

The Global Cool-Light E.A LTD admin dashboard provides a comprehensive management interface for the HVAC business operations. Built using Django and Bootstrap 5, it offers a modern, responsive interface for managing bookings, services, customers, and business analytics.

## Features

### Authentication System
- **Admin Login**: Secure login system for staff members
- **Admin Signup**: Registration system for new admin users
- **Session Management**: Remember me functionality and secure session handling
- **Password Validation**: Strong password requirements

### Dashboard Features
- **Statistics Overview**: Key business metrics at a glance
  - Today's bookings count
  - Active services count
  - Total customers count
  - Monthly revenue tracking

- **Recent Activity**: Quick view of recent bookings and their status
- **Quick Actions**: Fast access to common tasks
  - Create new bookings
  - Generate quotations
  - Add services
  - Manage users

### Navigation Structure
- **Dashboard**: Main overview page
- **Bookings**: Manage all service bookings
  - All bookings
  - Pending bookings
  - Completed bookings
- **Services**: Service management
  - All services
  - Add new services
  - Service categories
- **Portfolio**: Project showcase management
- **Quotations**: Quote management system
- **Customers**: Customer relationship management
- **Reports**: Business analytics and reporting
  - Revenue reports
  - Booking analytics
  - Customer reports
- **Settings**: System configuration
  - General settings
  - User management
  - Email templates

## URLs

### Authentication URLs
- `/users/admin/login/` - Admin login page
- `/users/admin/signup/` - Admin registration page
- `/users/admin/logout/` - Admin logout
- `/users/admin/forgot-password/` - Password reset (placeholder)

### Dashboard URLs
- `/users/admin/dashboard/` - Main admin dashboard

## Installation & Setup

### 1. Static Files
The admin dashboard uses Bootstrap 5 and custom styling. Static files are automatically copied from the admin-template directory:

```bash
# Static files are located in:
static/admin-css/     # Bootstrap and custom CSS
static/admin-js/      # JavaScript files
static/admin-lib/     # Third-party libraries
static/admin-img/     # Images and assets
```

### 2. Create Admin User
Use the custom management command to create admin users:

```bash
# Interactive mode
python manage.py create_admin

# Command line mode
python manage.py create_admin --email admin@example.com --password YourPassword123! --first-name John --last-name Doe
```

### 3. Access the Dashboard
1. Start the Django development server
2. Navigate to `http://localhost:8000/users/admin/login/`
3. Login with your admin credentials
4. Access the dashboard at `http://localhost:8000/users/admin/dashboard/`

## Design System

### Color Scheme
- **Primary**: Blue (#004AAD) - Global Cool-Light brand color
- **Secondary**: Light Blue (#00AEEF)
- **Accent**: Orange (#FFB800) for highlights
- **Neutral**: Gray tones for backgrounds and text

### Typography
- **Headings**: Poppins Bold
- **Body Text**: Roboto Regular
- **Icons**: Font Awesome 5 and Bootstrap Icons

### Layout
- **Sidebar Navigation**: Collapsible sidebar with main navigation
- **Top Bar**: Search, notifications, and user profile
- **Content Area**: Main dashboard content with cards and widgets
- **Responsive Design**: Mobile-first approach with Bootstrap grid

## Security Features

### Authentication
- Email-based login system
- Strong password validation
- Session management with remember me option
- Staff-only access control

### Authorization
- User role checking (is_staff required)
- Login required decorators
- Permission-based access control

### Session Security
- Configurable session expiry
- Secure session handling
- CSRF protection on all forms

## Customization

### Adding New Admin Pages
1. Create new views in `apps/users/views.py`
2. Add URL patterns in `apps/users/urls.py`
3. Create templates in `templates/admin/`
4. Update navigation in `templates/admin/dashboard.html`

### Styling Customization
- Modify `static/admin-css/style.css` for custom styles
- Update Bootstrap variables in `static/admin-css/bootstrap.min.css`
- Add custom JavaScript in `static/admin-js/main.js`

## Integration with Main Website

### Navigation Link
The main website header includes an "Admin" link in the top bar that directs to the admin login page.

### Shared Components
- Uses the same favicon and branding elements
- Consistent with the main website's color scheme
- Responsive design matches the main site

## Future Enhancements

### Planned Features
1. **Real Data Integration**: Connect with actual booking and service models
2. **Advanced Analytics**: Charts and graphs for business insights
3. **Email System**: Automated email notifications and templates
4. **File Management**: Upload and manage service images and documents
5. **API Integration**: RESTful API for mobile app integration
6. **Advanced Permissions**: Role-based access control with custom permissions
7. **Audit Logging**: Track all admin actions and changes
8. **Backup System**: Automated database and media backups

### Technical Improvements
1. **AJAX Integration**: Dynamic content loading without page refresh
2. **Real-time Notifications**: WebSocket integration for live updates
3. **Advanced Search**: Full-text search across all entities
4. **Export Features**: PDF and Excel export for reports
5. **Multi-language Support**: Internationalization for different languages

## Troubleshooting

### Common Issues

1. **Static Files Not Loading**
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Permission Denied**
   - Ensure user has `is_staff=True`
   - Check user permissions in Django admin

3. **Template Not Found**
   - Verify template paths in `templates/admin/`
   - Check `TEMPLATES` setting in Django settings

4. **CSS/JS Not Working**
   - Check static file paths in templates
   - Ensure `DEBUG=True` for development
   - Run `collectstatic` command

## Support

For technical support or feature requests, contact the development team or refer to the main project documentation.

---

**Last Updated**: September 2025  
**Version**: 1.0  
**Author**: Global Cool-Light Development Team
