from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True)  # For category icons

    def __str__(self):
        return self.name

class Issue(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)  # Made compulsory
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    image = models.ImageField(upload_to='issues/', blank=True, null=True)  # Keep optional in model, make required in form
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)  # For public board
    bounty_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)  # Reward for solving
    accepted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='accepted_issues')
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_issues')
    ai_category = models.CharField(max_length=100, blank=True)  # AI suggested category
    predicted_resolution_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Citizen', 'Citizen'),
        ('Staff', 'Staff'),
        ('Admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Citizen')
    points = models.IntegerField(default=0)
    total_rewards = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Total monetary rewards
    badges = models.JSONField(default=list)  # List of badge names

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Reward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    points_earned = models.IntegerField()
    earned_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} earned {self.points_earned} points"

class MonetaryReward(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Paid', 'Paid'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    allotted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='allotted_rewards')
    allotted_at = models.DateTimeField(default=timezone.now)
    paid_at = models.DateTimeField(null=True, blank=True)
    payment_reference = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"₹{self.amount} reward for {self.user.username}"

    def save(self, *args, **kwargs):
        # Update user's total rewards when approved
        try:
            if self.status == 'Approved' and (not hasattr(self, '_original_status') or self._original_status != 'Approved'):
                # Ensure userprofile exists
                if not hasattr(self.user, 'userprofile'):
                    from .models import UserProfile
                    UserProfile.objects.get_or_create(user=self.user)
                # Ensure amount is Decimal
                amount_decimal = self.amount if isinstance(self.amount, Decimal) else Decimal(str(self.amount))
                self.user.userprofile.total_rewards += amount_decimal
                self.user.userprofile.save()
            elif self.status == 'Rejected' and hasattr(self, '_original_status') and self._original_status == 'Approved':
                if hasattr(self.user, 'userprofile'):
                    # Ensure amount is Decimal
                    amount_decimal = self.amount if isinstance(self.amount, Decimal) else Decimal(str(self.amount))
                    self.user.userprofile.total_rewards -= amount_decimal
                    self.user.userprofile.save()
        except Exception as e:
            # Log the error but don't break the save
            import logging
            logging.error(f"Error updating total_rewards for user {self.user.username}: {e}")

        super().save(*args, **kwargs)
        self._original_status = self.status
