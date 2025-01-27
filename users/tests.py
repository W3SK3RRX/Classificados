from django.test import TestCase
from django.utils.timezone import now
from users.models import User, Subscription, Plan, create_subscription

class UserModelTests(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test",
            "lastname": "User",
        }

    def test_create_user(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.check_password(self.user_data["password"]))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(**self.user_data)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_user_string_representation(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), user.email)

class SubscriptionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="subscriber@example.com",
            password="testpass123",
            name="Subscriber",
            lastname="User",
        )
        self.plan = Plan.objects.create(name="Basic Plan", price=100.00, duration_in_days=30)

    def test_create_subscription(self):
        create_subscription(self.user, self.plan)
        subscription = Subscription.objects.get(user=self.user)
        self.assertEqual(subscription.user, self.user)
        self.assertTrue(subscription.active)
        self.assertGreater(subscription.end_date, now())

class PlanModelTests(TestCase):
    def test_create_plan(self):
        plan = Plan.objects.create(name="Premium Plan", price=200.00, duration_in_days=60)
        self.assertEqual(str(plan), "Premium Plan")
        self.assertEqual(plan.price, 200.00)
