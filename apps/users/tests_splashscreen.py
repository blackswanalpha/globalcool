"""
Tests for the admin portal splashscreen functionality.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminSplashscreenTestCase(TestCase):
    """Test cases for admin splashscreen functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create a regular user
        self.regular_user = User.objects.create_user(
            username='regular_user',
            email='user@example.com',
            password='testpass123'
        )
        
        # Create an admin user
        self.admin_user = User.objects.create_user(
            username='admin_user',
            email='admin@example.com',
            password='adminpass123',
            is_staff=True
        )
        
        # URLs
        self.splashscreen_url = reverse('users:admin_splashscreen')
        self.login_url = reverse('users:admin_login')
        self.dashboard_url = reverse('users:admin_dashboard')
    
    def test_splashscreen_url_exists(self):
        """Test that the splashscreen URL exists and returns 200"""
        response = self.client.get(self.splashscreen_url)
        self.assertEqual(response.status_code, 200)
    
    def test_splashscreen_uses_correct_template(self):
        """Test that the splashscreen uses the correct template"""
        response = self.client.get(self.splashscreen_url)
        self.assertTemplateUsed(response, 'admin/splashscreen.html')
    
    def test_splashscreen_contains_branding(self):
        """Test that the splashscreen contains company branding elements"""
        response = self.client.get(self.splashscreen_url)
        self.assertContains(response, 'Global Cool-Light E.A LTD')
        self.assertContains(response, 'Your Trusted HVAC Partner')
        self.assertContains(response, 'Admin Portal')
        self.assertContains(response, 'fas fa-snowflake')
    
    def test_splashscreen_contains_skip_button(self):
        """Test that the splashscreen contains a skip button"""
        response = self.client.get(self.splashscreen_url)
        self.assertContains(response, 'Skip')
        self.assertContains(response, 'skipSplash()')
    
    def test_splashscreen_contains_loading_elements(self):
        """Test that the splashscreen contains loading elements"""
        response = self.client.get(self.splashscreen_url)
        self.assertContains(response, 'loading-spinner')
        self.assertContains(response, 'progress-bar')
        self.assertContains(response, 'Initializing system...')
    
    def test_splashscreen_redirects_authenticated_admin(self):
        """Test that authenticated admin users are redirected to dashboard"""
        # Login as admin
        self.client.login(username='admin_user', password='adminpass123')
        
        # Access splashscreen
        response = self.client.get(self.splashscreen_url)
        
        # Should redirect to dashboard
        self.assertRedirects(response, self.dashboard_url)
    
    def test_splashscreen_shows_for_unauthenticated_users(self):
        """Test that unauthenticated users see the splashscreen"""
        response = self.client.get(self.splashscreen_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'admin-splashscreen')
    
    def test_splashscreen_shows_for_regular_users(self):
        """Test that regular (non-admin) users see the splashscreen"""
        # Login as regular user
        self.client.login(username='regular_user', password='testpass123')
        
        # Access splashscreen
        response = self.client.get(self.splashscreen_url)
        
        # Should show splashscreen (not redirect)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'admin-splashscreen')
    
    def test_splashscreen_javascript_functionality(self):
        """Test that the splashscreen contains necessary JavaScript"""
        response = self.client.get(self.splashscreen_url)
        self.assertContains(response, 'skipSplash()')
        self.assertContains(response, 'redirectToLogin()')
        self.assertContains(response, 'setTimeout')
        self.assertContains(response, 'users:admin_login')
    
    def test_splashscreen_css_animations(self):
        """Test that the splashscreen contains CSS animations"""
        response = self.client.get(self.splashscreen_url)
        self.assertContains(response, '@keyframes')
        self.assertContains(response, 'logoFloat')
        self.assertContains(response, 'fadeInUp')
        self.assertContains(response, 'progressFill')
    
    def test_splashscreen_responsive_design(self):
        """Test that the splashscreen contains responsive CSS"""
        response = self.client.get(self.splashscreen_url)
        self.assertContains(response, '@media')
        self.assertContains(response, 'max-width: 768px')
        self.assertContains(response, 'max-width: 480px')
    
    def test_admin_link_points_to_splashscreen(self):
        """Test that the main admin link points to splashscreen"""
        # This would require testing the header template
        # For now, we'll just verify the URL name exists
        from django.urls import reverse
        try:
            url = reverse('users:admin_splashscreen')
            self.assertTrue(url.startswith('/users/admin/'))
        except:
            self.fail("admin_splashscreen URL name not found")


class AdminSplashscreenIntegrationTestCase(TestCase):
    """Integration tests for admin splashscreen with the overall system"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin_user',
            email='admin@example.com',
            password='adminpass123',
            is_staff=True
        )
    
    def test_full_admin_flow_with_splashscreen(self):
        """Test the complete admin flow: splashscreen -> login -> dashboard"""
        # Step 1: Access splashscreen
        response = self.client.get(reverse('users:admin_splashscreen'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Global Cool-Light E.A LTD')
        
        # Step 2: Navigate to login (simulating redirect or skip)
        response = self.client.get(reverse('users:admin_login'))
        self.assertEqual(response.status_code, 200)
        
        # Step 3: Login
        response = self.client.post(reverse('users:admin_login'), {
            'email': 'admin@example.com',
            'password': 'adminpass123'
        })
        self.assertRedirects(response, reverse('users:admin_dashboard'))
        
        # Step 4: Verify dashboard access
        response = self.client.get(reverse('users:admin_dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_splashscreen_bypass_for_authenticated_admin(self):
        """Test that authenticated admins bypass splashscreen"""
        # Login first
        self.client.login(username='admin_user', password='adminpass123')
        
        # Try to access splashscreen
        response = self.client.get(reverse('users:admin_splashscreen'))
        
        # Should redirect directly to dashboard
        self.assertRedirects(response, reverse('users:admin_dashboard'))


if __name__ == '__main__':
    import django
    from django.conf import settings
    from django.test.utils import get_runner
    
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["apps.users.tests_splashscreen"])
