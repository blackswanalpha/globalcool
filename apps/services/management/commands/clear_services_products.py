"""
Django management command to safely delete all services and products data.
This command provides options to delete specific data types or all data.
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from apps.services.models import (
    Service, ServiceCategory, ServiceImage,
    Product, ProductCategory, ProductImage
)


class Command(BaseCommand):
    help = 'Delete services and products data from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--services-only',
            action='store_true',
            help='Delete only services and related data (keep products)',
        )
        parser.add_argument(
            '--products-only',
            action='store_true',
            help='Delete only products and related data (keep services)',
        )
        parser.add_argument(
            '--categories-only',
            action='store_true',
            help='Delete only categories (this will cascade delete all related data)',
        )
        parser.add_argument(
            '--images-only',
            action='store_true',
            help='Delete only images (keep services and products)',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Delete all services and products data',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Skip confirmation prompt',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        # Validate arguments
        exclusive_options = [
            options['services_only'],
            options['products_only'], 
            options['categories_only'],
            options['images_only'],
            options['all']
        ]
        
        if sum(exclusive_options) == 0:
            raise CommandError(
                "You must specify one of: --services-only, --products-only, "
                "--categories-only, --images-only, or --all"
            )
        
        if sum(exclusive_options) > 1:
            raise CommandError(
                "You can only specify one deletion option at a time"
            )

        # Show current data counts
        self.show_current_data()

        # Determine what to delete
        if options['services_only']:
            self.delete_services_data(options)
        elif options['products_only']:
            self.delete_products_data(options)
        elif options['categories_only']:
            self.delete_categories_data(options)
        elif options['images_only']:
            self.delete_images_data(options)
        elif options['all']:
            self.delete_all_data(options)

    def show_current_data(self):
        """Display current data counts"""
        self.stdout.write(self.style.HTTP_INFO("=== Current Database Counts ==="))
        self.stdout.write(f"Service Categories: {ServiceCategory.objects.count()}")
        self.stdout.write(f"Services: {Service.objects.count()}")
        self.stdout.write(f"Service Images: {ServiceImage.objects.count()}")
        self.stdout.write(f"Product Categories: {ProductCategory.objects.count()}")
        self.stdout.write(f"Products: {Product.objects.count()}")
        self.stdout.write(f"Product Images: {ProductImage.objects.count()}")
        self.stdout.write("")

    def confirm_deletion(self, message, force=False):
        """Ask for user confirmation unless force is True"""
        if force:
            return True
        
        self.stdout.write(self.style.WARNING(message))
        response = input("Are you sure you want to proceed? (yes/no): ")
        return response.lower() in ['yes', 'y']

    def delete_services_data(self, options):
        """Delete all services and related data"""
        service_count = Service.objects.count()
        service_image_count = ServiceImage.objects.count()
        
        if service_count == 0 and service_image_count == 0:
            self.stdout.write(self.style.SUCCESS("No services data to delete."))
            return

        message = f"This will delete {service_count} services and {service_image_count} service images."
        
        if options['dry_run']:
            self.stdout.write(self.style.WARNING(f"DRY RUN: {message}"))
            return

        if not self.confirm_deletion(message, options['force']):
            self.stdout.write("Operation cancelled.")
            return

        try:
            with transaction.atomic():
                # Delete service images first (though CASCADE should handle this)
                deleted_images = ServiceImage.objects.all().delete()
                # Delete services
                deleted_services = Service.objects.all().delete()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully deleted {deleted_services[0]} services "
                        f"and {deleted_images[0]} service images."
                    )
                )
        except Exception as e:
            raise CommandError(f"Error deleting services data: {e}")

    def delete_products_data(self, options):
        """Delete all products and related data"""
        product_count = Product.objects.count()
        product_image_count = ProductImage.objects.count()
        
        if product_count == 0 and product_image_count == 0:
            self.stdout.write(self.style.SUCCESS("No products data to delete."))
            return

        message = f"This will delete {product_count} products and {product_image_count} product images."
        
        if options['dry_run']:
            self.stdout.write(self.style.WARNING(f"DRY RUN: {message}"))
            return

        if not self.confirm_deletion(message, options['force']):
            self.stdout.write("Operation cancelled.")
            return

        try:
            with transaction.atomic():
                # Delete product images first (though CASCADE should handle this)
                deleted_images = ProductImage.objects.all().delete()
                # Delete products
                deleted_products = Product.objects.all().delete()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully deleted {deleted_products[0]} products "
                        f"and {deleted_images[0]} product images."
                    )
                )
        except Exception as e:
            raise CommandError(f"Error deleting products data: {e}")

    def delete_categories_data(self, options):
        """Delete all categories (this will cascade delete all related data)"""
        service_cat_count = ServiceCategory.objects.count()
        product_cat_count = ProductCategory.objects.count()
        service_count = Service.objects.count()
        product_count = Product.objects.count()
        
        if service_cat_count == 0 and product_cat_count == 0:
            self.stdout.write(self.style.SUCCESS("No categories to delete."))
            return

        message = (
            f"This will delete {service_cat_count} service categories and "
            f"{product_cat_count} product categories, which will also delete "
            f"{service_count} services and {product_count} products due to CASCADE."
        )
        
        if options['dry_run']:
            self.stdout.write(self.style.WARNING(f"DRY RUN: {message}"))
            return

        if not self.confirm_deletion(message, options['force']):
            self.stdout.write("Operation cancelled.")
            return

        try:
            with transaction.atomic():
                # Delete categories (CASCADE will handle related data)
                deleted_service_cats = ServiceCategory.objects.all().delete()
                deleted_product_cats = ProductCategory.objects.all().delete()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully deleted {deleted_service_cats[0]} service categories "
                        f"and {deleted_product_cats[0]} product categories "
                        f"(and all related data)."
                    )
                )
        except Exception as e:
            raise CommandError(f"Error deleting categories: {e}")

    def delete_images_data(self, options):
        """Delete only images"""
        service_image_count = ServiceImage.objects.count()
        product_image_count = ProductImage.objects.count()
        
        if service_image_count == 0 and product_image_count == 0:
            self.stdout.write(self.style.SUCCESS("No images to delete."))
            return

        message = f"This will delete {service_image_count} service images and {product_image_count} product images."
        
        if options['dry_run']:
            self.stdout.write(self.style.WARNING(f"DRY RUN: {message}"))
            return

        if not self.confirm_deletion(message, options['force']):
            self.stdout.write("Operation cancelled.")
            return

        try:
            with transaction.atomic():
                deleted_service_images = ServiceImage.objects.all().delete()
                deleted_product_images = ProductImage.objects.all().delete()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully deleted {deleted_service_images[0]} service images "
                        f"and {deleted_product_images[0]} product images."
                    )
                )
        except Exception as e:
            raise CommandError(f"Error deleting images: {e}")

    def delete_all_data(self, options):
        """Delete all services and products data"""
        service_cat_count = ServiceCategory.objects.count()
        product_cat_count = ProductCategory.objects.count()
        service_count = Service.objects.count()
        product_count = Product.objects.count()
        service_image_count = ServiceImage.objects.count()
        product_image_count = ProductImage.objects.count()
        
        total_items = (service_cat_count + product_cat_count + service_count + 
                      product_count + service_image_count + product_image_count)
        
        if total_items == 0:
            self.stdout.write(self.style.SUCCESS("No data to delete."))
            return

        message = (
            f"This will delete ALL services and products data:\n"
            f"- {service_cat_count} service categories\n"
            f"- {product_cat_count} product categories\n"
            f"- {service_count} services\n"
            f"- {product_count} products\n"
            f"- {service_image_count} service images\n"
            f"- {product_image_count} product images\n"
            f"Total: {total_items} items"
        )
        
        if options['dry_run']:
            self.stdout.write(self.style.WARNING(f"DRY RUN: {message}"))
            return

        if not self.confirm_deletion(message, options['force']):
            self.stdout.write("Operation cancelled.")
            return

        try:
            with transaction.atomic():
                # Delete in order to avoid foreign key constraints
                deleted_service_images = ServiceImage.objects.all().delete()
                deleted_product_images = ProductImage.objects.all().delete()
                deleted_services = Service.objects.all().delete()
                deleted_products = Product.objects.all().delete()
                deleted_service_cats = ServiceCategory.objects.all().delete()
                deleted_product_cats = ProductCategory.objects.all().delete()
                
                total_deleted = (
                    deleted_service_images[0] + deleted_product_images[0] +
                    deleted_services[0] + deleted_products[0] +
                    deleted_service_cats[0] + deleted_product_cats[0]
                )
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully deleted all services and products data "
                        f"({total_deleted} total items)."
                    )
                )
        except Exception as e:
            raise CommandError(f"Error deleting all data: {e}")
