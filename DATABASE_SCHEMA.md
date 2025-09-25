# Database Schema

## Overview
The Rental Management System uses a PostgreSQL database hosted on Supabase with two main tables: `tenants` and `payments`.

## Tables

### Tenants Table
Stores information about rental tenants.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique identifier |
| name | VARCHAR(200) | NOT NULL | Tenant's full name |
| phone | VARCHAR(20) | NOT NULL | International phone number (e.g., +254712345678) |
| apartment_number | VARCHAR(50) | NOT NULL | Apartment identifier |
| rent_amount | DECIMAL(10,2) | NOT NULL | Monthly rent amount (in KSh) |
| rent_status | VARCHAR(10) | CHECK (rent_status IN ('Paid', 'Unpaid')), DEFAULT 'Unpaid' | Payment status |
| created_at | TIMESTAMP WITH TIME ZONE | DEFAULT NOW() | Record creation timestamp |
| updated_at | TIMESTAMP WITH TIME ZONE | DEFAULT NOW() | Last update timestamp |

### Payments Table
Stores payment records linked to tenants.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique identifier |
| tenant_id | UUID | FOREIGN KEY REFERENCES tenants(id) ON DELETE CASCADE | Reference to tenant |
| amount | DECIMAL(10,2) | NOT NULL | Payment amount (in KSh) |
| date | TIMESTAMP WITH TIME ZONE | DEFAULT NOW() | Payment date |
| status | VARCHAR(10) | CHECK (status IN ('Paid', 'Pending')), DEFAULT 'Paid' | Payment status |

## Indexes
- `idx_tenants_rent_status` on `tenants(rent_status)` - For filtering by payment status
- `idx_payments_date` on `payments(date)` - For sorting payments by date
- `idx_payments_tenant_id` on `payments(tenant_id)` - For joining with tenants table

## Relationships
- **One-to-Many**: One tenant can have multiple payments
- **Cascade Delete**: When a tenant is deleted, all their payments are also deleted

## Sample Data

### Tenants
```sql
INSERT INTO tenants (name, phone, apartment_number, rent_amount, rent_status) VALUES
('John Doe', '+254712345678', 'A101', 50000.00, 'Unpaid'),
('Jane Smith', '+254798765432', 'B202', 75000.00, 'Paid'),
('Mike Johnson', '+254723456789', 'C303', 60000.00, 'Unpaid');
```

### Payments
```sql
INSERT INTO payments (tenant_id, amount, status) VALUES
((SELECT id FROM tenants WHERE name = 'Jane Smith'), 75000.00, 'Paid'),
((SELECT id FROM tenants WHERE name = 'John Doe'), 50000.00, 'Pending');
```

## Django Models
The Django models in `rental_app/models.py` correspond to these database tables with additional features:
- Automatic UUID generation
- String representations for admin interface
- Ordering by creation/update dates
- Related name for reverse lookups
