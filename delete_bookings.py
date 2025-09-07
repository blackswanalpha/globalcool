#!/usr/bin/env python
"""
Delete all bookings from Global Cool-Light E.A LTD database
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.leads.models import Booking, Inquiry

def delete_all_bookings():
    """Delete all bookings from the database"""
    
    # Count existing bookings
    booking_count = Booking.objects.count()
    inquiry_count = Inquiry.objects.count()
    
    print(f"📊 Current database status:")
    print(f"   • {booking_count} bookings")
    print(f"   • {inquiry_count} inquiries")
    print()
    
    if booking_count == 0 and inquiry_count == 0:
        print("✅ No bookings or inquiries to delete!")
        return
    
    # Confirm deletion
    print("⚠️  WARNING: This will permanently delete ALL bookings and inquiries!")
    print("   This action cannot be undone.")
    print()
    
    # For safety, require explicit confirmation
    confirmation = input("Type 'DELETE ALL' to confirm: ")
    
    if confirmation != 'DELETE ALL':
        print("❌ Deletion cancelled. No data was deleted.")
        return
    
    print("\n🗑️  Deleting all bookings and inquiries...")
    
    # Delete all bookings
    if booking_count > 0:
        deleted_bookings = Booking.objects.all().delete()
        print(f"✅ Deleted {deleted_bookings[0]} bookings")
    
    # Delete all inquiries
    if inquiry_count > 0:
        deleted_inquiries = Inquiry.objects.all().delete()
        print(f"✅ Deleted {deleted_inquiries[0]} inquiries")
    
    print("\n🎉 All bookings and inquiries have been successfully deleted!")
    print("\n📊 Database is now clean:")
    print(f"   • {Booking.objects.count()} bookings remaining")
    print(f"   • {Inquiry.objects.count()} inquiries remaining")
    print()
    print("💡 You can now:")
    print("   • Create fresh bookings at: http://127.0.0.1:8000/booking/")
    print("   • Repopulate with sample data: python simple_populate_data.py")

def main():
    """Main function"""
    print("🗑️  Global Cool-Light E.A LTD - Delete All Bookings")
    print("=" * 50)
    delete_all_bookings()

if __name__ == '__main__':
    main()
