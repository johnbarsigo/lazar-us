# OKS Hostel Management System - Frontend

A modern, responsive React.js frontend for the hostel management system with light/dark mode support.

## Features

- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Light/Dark Mode**: Toggle between light and dark themes
- **Role-based Access Control**: Different dashboards for Admin and Manager roles
- **Real-time Data**: Integration with REST API for live data updates
- **User-friendly UI**: Clean and intuitive interface designed for non-technical users
- **Authentication**: Secure login and signup with JWT tokens

## Pages

- **Login/Signup**: User authentication
- **Dashboard**: Overview with key metrics and quick actions
- **Tenants**: Manage tenant information and occupancy history
- **Rooms**: View room status and management
- **Billings**: Monthly charges and billing management
- **Payments**: Record and track payments
- **Reports**: Arrears and income reports with export functionality

## Tech Stack

- React 18 with TypeScript
- Tailwind CSS for styling
- React Router for navigation
- Axios for API calls
- Zustand for state management
- Vite as build tool

## Getting Started

### Prerequisites

- Node.js 16+ and npm

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

The app will open at `http://localhost:3000`

### Build

```bash
npm run build
```

## Environment Variables

Create a `.env.local` file:

```
VITE_API_URL=http://localhost:5555/api
```

## Project Structure

```
src/
├── api/          # API client and endpoints
├── components/   # Reusable components (Header, Sidebar, Layout)
├── pages/        # Page components
├── store/        # Zustand stores (Auth, UI)
├── types/        # TypeScript interfaces
└── index.css     # Global styles with Tailwind
```

## Usage Notes

- The app assumes the backend API is running on `http://localhost:5555`
- JWT tokens are stored in localStorage
- Dark mode preference is persisted across sessions
- Mobile-first responsive design approach

## Future Enhancements

- Add form validation UI feedback
- Implement modals for create/edit operations
- Add real-time notifications
- Implement advanced filtering and sorting
- Add print functionality for reports
- Implement data export to Excel
