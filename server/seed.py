
# Seed script to populate database with test data


from app import app, db
from models import User, Room, Tenant, Occupancy, MonthlyCharge, Payment, Notification
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def clear_database():
    # Clear all tables
    print("🗑️  Clearing database...")
    db.drop_all()
    db.create_all()
    print("✅ Database cleared and tables created")

def seed_users():
    # Create test users
    print("\n👥 Creating users...")
    
    users = [
        User(
            username="Admin1",
            email="admin1@oksms.com",
            # phone="254712345678",
            password_hash=generate_password_hash("admin123"),
            role="admin"
            # is_active=True
        ),
        User(
            username="Admin2",
            email="admin2@oksms.com",
            # phone="254712345679",
            password_hash=generate_password_hash("admin234"),
            role="admin"
            # is_active=False
        ),
        User(
            username="MaryMG",
            email="marymanager@oksms.com",
            # phone="254712345680",
            password_hash=generate_password_hash("manager123"),
            role="manager"
            # is_active=True
        ),
        User(
            username="AliceMG",
            email="alicemanager@oksms.com",
            # phone="254712345681",
            password_hash=generate_password_hash("manager234"),
            role="manager"
            # is_active=True
        ),
        User(
            username="BobMG",
            email="bobmanager@oksms.com",
            # phone="254712345682",
            password_hash=generate_password_hash("manager345"),
            role="manager"
            # is_active=True
        ),
        User(
            username="CharlieMG",
            email="charliemanager@oksms.com",
            # phone="254712345683",
            password_hash=generate_password_hash("manager456"),
            role="manager"
            # is_active=False
        ),
    ]
    
    db.session.add_all(users)
    db.session.commit()
    print(f"✅ Created {len(users)} users")
    return users

def seed_rooms(users):
    """Create test rooms"""
    print("\n🏠 Creating rooms...")
    
    rooms = [
        Room(
            room_number="101",
            # floor=1,
            capacity=1,
            default_rent=5000.00,
            status="occupied",
            # created_by_user_id=users[0].id  # Admin
        ),
        Room(
            room_number="102",
            # floor=1,
            capacity=2,
            default_rent=7500.00,
            status="available",
            # created_by_user_id=users[0].id  # Admin
        ),
        Room(
            room_number="103",
            # floor=1,
            capacity=1,
            default_rent=5000.00,
            status="occupied",
            # created_by_user_id=users[0].id
        ),
        Room(
            room_number="201",
            # floor=2,
            capacity=2,
            default_rent=8000.00,
            status="available",
            # created_by_user_id=users[0].id
        ),
        Room(
            room_number="202",
            # floor=2,
            capacity=2,
            default_rent=8000.00,
            status="occupied",
            # created_by_user_id=users[0].id
        ),
        Room(
            room_number="203",
            # floor=2,
            capacity=1,
            default_rent=5500.00,
            status="available",
            # created_by_user_id=users[0].id
        ),
    ]
    
    db.session.add_all(rooms)
    db.session.commit()
    print(f"✅ Created {len(rooms)} rooms")
    return rooms

def seed_tenants(users):
    """Create test tenants"""
    print("\n👤 Creating tenants...")
    
    tenants = [
        Tenant(
            name="Maxwell",
            email="maxwell@gmail.com",
            national_id="12345678",
            phone="0712999111",
            # emergency_contact_name="Sarah",
            # occupation="Engineer"
        ),
        Tenant(
            name="Alonso",
            email="alonso@gmail.com",
            national_id="87654321",
            phone="0712999222",
            # emergency_contact_name="Maria",
            # occupation="Teacher"
        ),
        Tenant(
            name="Lewis",
            email="lewis@gmail.com",
            national_id="11223344",
            phone="0712999333",
            # emergency_contact_name="John",
            # occupation="Doctor"
        ),
    ]
    
    db.session.add_all(tenants)
    db.session.commit()
    print(f"✅ Created {len(tenants)} tenants")
    return tenants

def seed_occupancies(tenants, rooms, users):
    """Create test occupancies"""
    print("\n📋 Creating occupancies...")
    
    now = datetime.utcnow()
    
    occupancies = [
        Occupancy(
            tenant_id=tenants[0].id,  # Maxwell
            room_id=rooms[2].id,  # Room 103
            check_in_date=now - timedelta(days=90),
            check_out_date=None,
            agreed_rent=5000.00,
            status="active",
            # created_by_user_id=users[1].id  # Manager
        ),
        Occupancy(
            tenant_id=tenants[1].id,  # Alonso
            room_id=rooms[4].id,  # Room 202
            check_in_date=now - timedelta(days=60),
            check_out_date=None,
            agreed_rent=8000.00,
            status="active",
            # created_by_user_id=users[1].id
        ),
        Occupancy(
            tenant_id=tenants[2].id,  # Lewis
            room_id=rooms[0].id,  # Room 101
            check_in_date=now - timedelta(days=30),
            check_out_date=None,
            agreed_rent=5000.00,
            status="active",
            # created_by_user_id=users[1].id
        ),
    ]
    
    db.session.add_all(occupancies)
    db.session.commit()
    print(f"✅ Created {len(occupancies)} occupancies")
    return occupancies

def seed_monthly_charges(occupancies):
    """Create test monthly charges"""
    print("\n💰 Creating monthly charges...")
    
    now = datetime.utcnow()
    current_month = now.month
    current_year = now.year
    
    monthly_charges = []
    
    # Create charges for the last 3 months for each occupancy
    for occupancy in occupancies:
        for month_offset in range(3):
            month = current_month - month_offset
            year = current_year
            
            if month <= 0:
                month += 12
                year -= 1
            
            charge = MonthlyCharge(
                occupancy_id=occupancy.id,
                month=month,
                year=year,
                rent_amount=occupancy.monthly_rent,
                water_bill=500.00 if month_offset < 2 else 0,
                damages_or_dues=0,
                total_due=occupancy.monthly_rent + (500.00 if month_offset < 2 else 0)
            )
            monthly_charges.append(charge)
    
    db.session.add_all(monthly_charges)
    db.session.commit()
    print(f"✅ Created {len(monthly_charges)} monthly charges")
    return monthly_charges

def seed_payments(occupancies, users):
    """Create test payments"""
    print("\n💳 Creating payments...")
    
    now = datetime.utcnow()
    
    payments = [
        Payment(
            occupancy_id=occupancies[0].id,  # Alice
            amount=5000.00,
            payment_method="mpesa",
            transaction_id="MPM0001",
            paid_by_user_id=occupancies[0].tenant.user_id,
            paid_date=now - timedelta(days=45),
            status="completed"
        ),
        Payment(
            occupancy_id=occupancies[0].id,  # Alice
            amount=5500.00,
            payment_method="bank_transfer",
            transaction_id="BANK0001",
            paid_by_user_id=occupancies[0].tenant.user_id,
            paid_date=now - timedelta(days=15),
            status="completed"
        ),
        Payment(
            occupancy_id=occupancies[1].id,  # Bob
            amount=8000.00,
            payment_method="mpesa",
            transaction_id="MPM0002",
            paid_by_user_id=occupancies[1].tenant.user_id,
            paid_date=now - timedelta(days=30),
            status="completed"
        ),
        Payment(
            occupancy_id=occupancies[2].id,  # Charlie
            amount=5000.00,
            payment_method="cash",
            transaction_id="CASH0001",
            paid_by_user_id=occupancies[2].tenant.user_id,
            paid_date=now - timedelta(days=5),
            status="completed"
        ),
    ]
    
    db.session.add_all(payments)
    db.session.commit()
    print(f"✅ Created {len(payments)} payments")
    return payments

def seed_notifications(users, occupancies):
    """Create test notifications"""
    print("\n🔔 Creating notifications...")
    
    now = datetime.utcnow()
    
    notifications = [
        Notification(
            user_id=users[3].id,  # Alice (tenant)
            title="Rent Due",
            message="Your rent of KES 5,000 is due on the 25th",
            notification_type="payment_reminder",
            is_read=False,
            created_at=now - timedelta(days=5)
        ),
        Notification(
            user_id=users[1].id,  # Manager
            title="New Tenant Check-in",
            message="Charlie has checked into Room 101",
            notification_type="checkin",
            is_read=True,
            created_at=now - timedelta(days=30)
        ),
        Notification(
            user_id=users[0].id,  # Admin
            title="Room Maintenance Completed",
            message="Room 203 maintenance has been completed",
            notification_type="maintenance",
            is_read=True,
            created_at=now - timedelta(days=7)
        ),
        Notification(
            user_id=users[4].id,  # Bob (tenant)
            title="Payment Received",
            message="Your payment of KES 8,000 has been received",
            notification_type="payment_confirmation",
            is_read=True,
            created_at=now - timedelta(days=30)
        ),
    ]
    
    db.session.add_all(notifications)
    db.session.commit()
    print(f"✅ Created {len(notifications)} notifications")
    return notifications

def main():
    """Run all seed functions"""
    with app.app_context():
        try:
            print("🌱 Starting database seeding...\n")
            
            clear_database()
            users = seed_users()
            rooms = seed_rooms(users)
            tenants = seed_tenants(users)
            occupancies = seed_occupancies(tenants, rooms, users)
            monthly_charges = seed_monthly_charges(occupancies)
            payments = seed_payments(occupancies, users)
            notifications = seed_notifications(users, occupancies)
            
            print("\n" + "="*50)
            print("✅ Database seeding completed successfully!")
            print("="*50)
            print("\n📊 Summary:")
            print(f"  • Users: {len(users)}")
            print(f"  • Rooms: {len(rooms)}")
            print(f"  • Tenants: {len(tenants)}")
            print(f"  • Occupancies: {len(occupancies)}")
            print(f"  • Monthly Charges: {len(monthly_charges)}")
            print(f"  • Payments: {len(payments)}")
            print(f"  • Notifications: {len(notifications)}")
            print("\n🔐 Test Login Credentials:")
            print("  Admin:    admin@oksms.com / admin123")
            print("  Manager:  manager@oksms.com / manager123")
            print("  Tenant:   alice@example.com / tenant123")
            
        except Exception as e:
            print(f"\n❌ Error during seeding: {str(e)}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    main()