# Custom Admin Dashboard

A modern, TailAdmin-inspired dashboard for the EduCollege Django project.

## Features

- **Modern UI Design**: Clean, professional interface with gradient colors and smooth animations
- **Statistics Overview**: Real-time statistics cards showing:
  - Total Students/Placements
  - Faculty Members
  - Departments
  - Placement Rate
- **Recent Activities**: 
  - Recent student applications
  - Upcoming events
  - Latest news
  - Recent placements
- **Sidebar Navigation**: Easy access to all admin sections
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Access the Dashboard

### Method 1: Direct URL
Visit: `http://localhost:8000/admin-dashboard/`

**Note**: You must be logged in as a staff member to access the dashboard.

### Method 2: From Django Admin
1. Go to: `http://localhost:8000/admin/`
2. Login with your admin credentials
3. Click the **"Open Custom Dashboard"** button at the top of the page

## Files Created

1. **Template**: `templates/admin/dashboard.html` - Main dashboard template
2. **CSS**: `static/css/admin-dashboard.css` - Dashboard styling
3. **View**: `cwebapp/views.py` - Added `admin_dashboard` view
4. **URL**: `cweb/urls.py` - Added route for `/admin-dashboard/`

## Dashboard Sections

### Statistics Cards
- **Students**: Total placement records count
- **Faculty**: Total faculty members
- **Departments**: Total departments
- **Placement Rate**: Average placement percentage

### Recent Applications
Shows the 5 most recent student applications with their status.

### Upcoming Events
Displays the next 4 upcoming events with dates and venues.

### Recent News
Lists the 4 most recent news items.

### Recent Placements
Shows the 5 most recent successful placements.

## Customization

### Colors
Edit `static/css/admin-dashboard.css` and modify the CSS variables:
```css
:root {
    --primary-color: #4F46E5;
    --success-color: #10B981;
    --warning-color: #F59E0B;
    --info-color: #3B82F6;
}
```

### Statistics
Modify the `admin_dashboard` view in `cwebapp/views.py` to add or change statistics.

## Security

The dashboard is protected by the `@staff_member_required` decorator, ensuring only staff users can access it.

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Mobile Support

The dashboard is fully responsive and includes:
- Collapsible sidebar on mobile devices
- Responsive grid layouts
- Touch-friendly navigation
