# OKS Hostel Management System - Missing Features & Implementation Checklist

## Priority Level: CRITICAL (Security & Data Integrity)

- [ ] **Fix Numeric Type Handling**
  - Replace `int()` casts with `float()` or `Decimal` for financial data
  - Files: rooms.py, billings.py, payments.py
  - Impact: Prevents loss of cents in rent calculations

- [ ] **Fix Occupancy State Bug**
  - Replace `occupancy.tenant_id = []` with proper end_date update
  - File: occupancies.py, line 192
  - Impact: Prevents crashes when ending occupancies

- [ ] **Implement Consistent Authorization**
  - Authorization check BEFORE data access in all endpoints
  - Return 403 Forbidden immediately if unauthorized
  - Files: All routes/\*.py

- [ ] **Add Database Transaction Safety**
  - Implement savepoints for complex operations
  - Handle IntegrityError for duplicate prevention
  - Implement rollback on failure

- [ ] **Add Request Validation**
  - Validate all input fields (email, phone, amounts)
  - Reject negative amounts
  - Validate date ranges

---

## Priority Level: HIGH (Core Functionality)

### Payment Management

- [ ] **Implement Payment Reconciliation Endpoint**
  - Endpoint: `POST /api/payments/reconcile`
  - Match M-Pesa deposits to tenant accounts
  - Auto-allocate payments to oldest arrears first
  - Return reconciliation report

- [ ] **Track Payment Methods**
  - Distinguish between M-Pesa, Cash, Bank transfers
  - Add receipt numbers for all methods
  - Create method-specific reporting

- [ ] **Implement Payment Reversal**
  - Endpoint: `POST /api/payments/{id}/reverse`
  - Handle refunds properly
  - Update tenant balance
  - Create audit log

- [ ] **Auto-Payment Allocation**
  - When payment received, automatically allocate to:
    1. Oldest unpaid month
    2. Then damages/dues
    3. Then advance payment
  - Logic: Create automatic allocation algorithm

### Occupancy Management

- [ ] **Complete TenantLedger Endpoint**
  - Show all charges, payments, and balance for tenant
  - Endpoint: `GET /api/tenants/{id}/ledger`
  - Return structure:
    ```json
    {
      "tenant": {...},
      "summary": {
        "total_charged": 0,
        "total_paid": 0,
        "current_balance": 0,
        "arrears": 0
      },
      "transactions": [
        {
          "date": "2026-05-13",
          "type": "billing|payment",
          "description": "",
          "amount": 0,
          "balance": 0
        }
      ]
    }
    ```

- [ ] **Implement Mid-Occupancy Rent Changes**
  - New endpoint: `POST /api/occupancies/{id}/change-rent`
  - Prorate charges for partial months
  - Keep change history
  - Update future billings

- [ ] **Damage & Dues Recording**
  - Endpoint: `POST /api/occupancies/{id}/record-damage`
  - Add damages to next billing
  - Track reason and date
  - Can be disputed/removed

- [ ] **Room Maintenance Tracking**
  - Add room status: "maintenance" (in addition to "available", "occupied")
  - Endpoint: `POST /api/rooms/{id}/maintenance`
  - Track maintenance dates
  - No billings during maintenance periods

### Billing Management

- [ ] **Implement Arrears Detection**
  - Flag tenants who haven't paid for current month
  - Endpoint: `GET /api/tenants/{id}/status` returns arrears info
  - Send alerts (via future SMS/Email)

- [ ] **Prorated Billing**
  - When tenant moves mid-month, calculate prorated charge
  - Formula: (daily_rate) × (days_occupied)
  - Apply to both end of old room, start of new room

- [ ] **Bulk Billing Operations**
  - Endpoint: `POST /api/billings/bulk-generate` with room selection
  - Generate for specific rooms only
  - Skip already billed rooms

- [ ] **Credit System**
  - Handle overpayments
  - Track credit balance per tenant
  - Allow credit to be applied to future months
  - Export credit report

### Reporting

- [ ] **Comprehensive Arrears Report**
  - Group by: amount owed, months overdue, room number
  - Export to CSV/PDF
  - Include payment history for each tenant

- [ ] **Income Report**
  - Monthly income by payment method (M-Pesa, Cash, Bank)
  - Outstanding vs. collected
  - Projected income vs. actual
  - Trends over 3, 6, 12 months

- [ ] **Occupancy Report**
  - Occupancy rate over time
  - Turnover statistics
  - Vacancy periods
  - Average stay duration

- [ ] **Room Utilization Report**
  - Revenue per room per month
  - Room with highest/lowest occupancy
  - Maintenance impact on revenue

- [ ] **Tenant Payment History Report**
  - Payments received by date
  - Payment methods breakdown
  - Average collection period
  - Bad debt analysis

- [ ] **End-of-Month Financial Summary**
  - Total rent charged
  - Total water bills charged
  - Total damages
  - Total collected
  - Outstanding balance
  - Cash flow analysis

---

## Priority Level: MEDIUM (Performance & UX)

### Backend Improvements

- [ ] **Implement Pagination**
  - Add `limit`, `offset` parameters to all list endpoints
  - Return `total_count` in response
  - Default limit: 50, max limit: 500

- [ ] **Add Query Filtering**

  ```
  GET /api/tenants?status=active|inactive&room_number=101&search=john
  GET /api/payments?status=pending&month=5&year=2026&method=mpesa
  GET /api/rooms?status=available|occupied|maintenance
  ```

- [ ] **Implement Sorting**
  - Allow sorting by any field: `?sort=name&order=asc`
  - Support multi-field sort: `?sort=room_number,name&order=asc,desc`

- [ ] **Add Database Indexes**
  - Index foreign keys (tenant_id, room_id, occupancy_id)
  - Index frequently filtered fields (status, month, year)
  - Index date ranges (created_at, start_date, end_date)

- [ ] **Optimize N+1 Queries**
  - Use `joinedload()` for related data
  - Create optimized list endpoints with minimal queries

- [ ] **Add Caching**
  - Cache room list (changes infrequently)
  - Cache user info (valid for session)
  - Cache reports (recompute at set intervals)

- [ ] **Implement Audit Logging**
  - Log all Create, Update, Delete operations
  - Store: who, what, when, before/after values
  - Table: `audit_logs`

### Frontend Improvements

- [ ] **Add Form Validation UI**
  - Real-time validation feedback
  - Visual indicators for required fields
  - Error messages below inputs

- [ ] **Implement Modal Dialogs**
  - Create/Edit tenant modal
  - Create/Edit room modal
  - Record payment modal
  - Confirm delete dialogs

- [ ] **Add Loading States**
  - Skeleton loaders on tables
  - Button loading spinners
  - Page transition animations

- [ ] **Implement Search/Filter UI**
  - Search box on all list pages
  - Filter dropdowns (status, room, payment method)
  - Applied filters display

- [ ] **Add Date Range Filters**
  - From/To date pickers
  - Common ranges: "This Month", "Last 3 Months", "This Year"
  - Custom range option

- [ ] **Implement Real-time Notifications**
  - Toast notifications for success/error
  - Alert for low/no occupancy
  - Payment received alerts

- [ ] **Add Print & Export**
  - Print button on all reports
  - Export to CSV
  - Export to PDF (future)
  - Email reports option

---

## Priority Level: LOW (Nice-to-Have)

- [ ] **Implement SMS Alerts**
  - Send payment reminders 3 days before due date
  - Send arrears notices
  - Send move-in/move-out confirmations

- [ ] **Add Email Notifications**
  - Send payment receipts
  - Send monthly statements
  - Send arrears notices

- [ ] **Multi-tenant Support**
  - Allow managing multiple hostels
  - Each hostel separate data
  - Global admin role

- [ ] **Advanced User Roles**
  - "Accountant" - only sees financials
  - "Receptionist" - only handles check-in/out
  - Custom role builder

- [ ] **Implement Two-Factor Authentication**
  - OTP via SMS or Email
  - TOTP app support

- [ ] **Dashboard Charts & Analytics**
  - Revenue trend chart
  - Occupancy rate chart
  - Payment method pie chart
  - Arrears breakdown

- [ ] **Mobile App**
  - React Native version
  - Offline mode with sync
  - Mobile-optimized UI

- [ ] **Calendar View**
  - Occupancy calendar
  - Payment calendar
  - Maintenance calendar

- [ ] **Tenant Portal**
  - View own ledger
  - View rent due
  - Request maintenance
  - View room details

---

## Implementation Roadmap

### Week 1-2: Critical Fixes

- Data integrity fixes (numeric types, state bugs)
- Authorization fixes
- Request validation

### Week 3-4: Core Functionality

- Payment reconciliation
- Tenant ledger completion
- Damage recording

### Week 5-6: Reporting

- Implement all reports
- Export functionality
- Report generation optimization

### Week 7-8: Performance

- Add pagination/filtering
- Database optimization
- Caching implementation

### Week 9+: Polish & Extras

- Frontend UX improvements
- SMS/Email notifications
- Mobile optimization
- Additional features per priority

---

## Testing Checklist

- [ ] Unit tests for all models
- [ ] Unit tests for authorization decorators
- [ ] Integration tests for API endpoints
- [ ] Test concurrent billing generation (race condition)
- [ ] Test payment allocation algorithm
- [ ] Test occupancy state transitions
- [ ] Test all numeric calculations
- [ ] Load test with 1000+ tenants
- [ ] Test data export/import
- [ ] Test permission checks on all endpoints

---

## Deployment Checklist

- [ ] Set all environment variables in production
- [ ] Run database migrations
- [ ] Load seed data (test rooms, test users)
- [ ] Configure CORS for frontend domain
- [ ] Set up backup schedule
- [ ] Configure SSL/TLS
- [ ] Set up monitoring & logging
- [ ] Create admin super-user
- [ ] Document API endpoints
- [ ] Create user documentation
- [ ] Create admin documentation
- [ ] Test full workflow end-to-end

---

## Success Criteria

Your system will be production-ready when:

✅ All critical bugs are fixed
✅ All core CRUD operations work
✅ Payment flow is complete (record → reconcile → allocate)
✅ All reports generate correctly
✅ Pagination works on all lists
✅ Authorization is enforced everywhere
✅ No data loss on concurrent operations
✅ Numeric data maintains precision
✅ Frontend is responsive on mobile
✅ API documentation is complete
✅ Users can manage full hostel lifecycle
✅ Financial integrity is guaranteed
