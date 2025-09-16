-- Old Kachesa Suites Management System Schema
-- Run: mysql -u <user> -p <database> <schema.sql


-- Users (system accounts)

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    role ENUM('admin', 'staff') DEFAULT 'staff',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- Tenants
CREATE TABLE tenants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(150),
    national_id VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- Rooms

CREATE TABLE rooms (
  id INT AUTO_INCREMENT PRIMARY KEY,
  room_number VARCHAR(50) UNIQUE NOT NULL,
  block VARCHAR(50),
  capacity INT DEFAULT 1,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- Occupancies (history of tenants in rooms)

CREATE TABLE occupancies (
  id INT AUTO_INCREMENT PRIMARY KEY,
  room_id INT NOT NULL,
  tenant_id INT NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NULL,              -- NULL = currently occupying
  rent_amount DECIMAL(10,2) NOT NULL,
  water_amount DECIMAL(10,2) DEFAULT 0,
  check_in_notes TEXT,
  check_out_notes TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (room_id) REFERENCES rooms(id),
  FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);


-- Payments (MPesa C2B and manual payments)

CREATE TABLE payments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  occupancy_id INT NULL,           -- which occupancy this payment applies to
  tenant_id INT NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  mpesa_transaction_id VARCHAR(50) UNIQUE,
  paybill VARCHAR(50),
  bill_ref_number VARCHAR(100),
  status ENUM('pending','confirmed','failed') DEFAULT 'pending',
  raw_callback JSON,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (occupancy_id) REFERENCES occupancies(id),
  FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);


-- Dues and Damages

CREATE TABLE adjustments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  occupancy_id INT,
  tenant_id INT NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  reason VARCHAR(255),
  resolved BOOLEAN DEFAULT FALSE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (occupancy_id) REFERENCES occupancies(id),
  FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);


-- Announcements

CREATE TABLE announcements (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255),
  body TEXT,
  scheduled_at DATETIME NULL,
  published BOOLEAN DEFAULT FALSE,
  created_by INT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (created_by) REFERENCES users(id)
);
