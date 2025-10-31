"""
User models for eSafety platform
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRole(models.TextChoices):
    """User role enumeration"""
    SUPER_ADMIN = 'super_admin', _('Super Admin')
    SYSTEM_ADMIN = 'system_admin', _('System Administrator')
    TMC_OPERATOR = 'tmc_operator', _('Traffic Management Center Operator')
    DISPATCHER = 'dispatcher', _('KeNHA Dispatcher')
    FIELD_INSPECTOR = 'field_inspector', _('KeNHA Field Inspector')
    MAINTENANCE_CREW = 'maintenance_crew', _('KeNHA Maintenance Crew')
    POLICE = 'police', _('Police Services')
    EMS = 'ems', _('Emergency Medical Services')
    FIRE_RESCUE = 'fire_rescue', _('Fire & Rescue Services')
    TOWING = 'towing', _('Towing & Recovery Services')
    ANALYST = 'analyst', _('Data Analyst')
    POLICY_ANALYST = 'policy_analyst', _('Policy Analyst')
    SUPPORT = 'support', _('Customer Support')
    QA_REVIEWER = 'qa_reviewer', _('Quality Assurance Reviewer')
    ROAD_USER_REGISTERED = 'road_user_registered', _('Registered Road User')
    ROAD_USER_ANONYMOUS = 'road_user_anonymous', _('Anonymous Road User')


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    """
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone number'), max_length=20, unique=True, null=True, blank=True)
    role = models.CharField(_('role'), max_length=30, choices=UserRole.choices, default=UserRole.ROAD_USER_ANONYMOUS)
    
    # Verification & Security
    is_verified = models.BooleanField(_('verified'), default=False)
    phone_verified = models.BooleanField(_('phone verified'), default=False)
    email_verified = models.BooleanField(_('email verified'), default=False)
    mfa_enabled = models.BooleanField(_('MFA enabled'), default=False)
    mfa_secret = models.CharField(_('MFA secret'), max_length=32, null=True, blank=True)
    
    # Reputation & Engagement
    reputation_score = models.DecimalField(_('reputation score'), max_digits=5, decimal_places=2, default=50.0)
    last_reputation_update = models.DateTimeField(_('last reputation update'), null=True, blank=True)
    
    # Blockchain (optional for registered users)
    blockchain_wallet_address = models.CharField(_('blockchain wallet'), max_length=42, null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone']
    
    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"


class UserProfile(models.Model):
    """
    Extended user profile information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(_('profile picture'), upload_to='profiles/', null=True, blank=True)
    
    # Organizational information
    department = models.CharField(_('department'), max_length=100, null=True, blank=True)
    organization = models.CharField(_('organization'), max_length=100, null=True, blank=True)
    badge_number = models.CharField(_('badge number'), max_length=50, null=True, blank=True)
    equipment_assigned = models.JSONField(_('equipment assigned'), default=dict, blank=True)
    
    # Preferences
    language = models.CharField(_('language'), max_length=10, default='en', choices=[('en', 'English'), ('sw', 'Swahili')])
    notification_preferences = models.JSONField(_('notification preferences'), default=dict, blank=True)
    location_preferences = models.JSONField(_('location preferences'), default=dict, blank=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
    
    def __str__(self):
        return f"{self.user.email} - Profile"


class UserReputation(models.Model):
    """
    User reputation tracking for citizen reporters
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reputation')
    
    # Reputation metrics
    accuracy_score = models.DecimalField(_('accuracy score'), max_digits=5, decimal_places=2, default=0.0)
    report_count = models.IntegerField(_('total reports'), default=0)
    verified_reports = models.IntegerField(_('verified reports'), default=0)
    false_reports = models.IntegerField(_('false reports'), default=0)
    spam_count = models.IntegerField(_('spam count'), default=0)
    
    # Blockchain reference
    blockchain_hash_reference = models.CharField(_('blockchain hash'), max_length=66, null=True, blank=True)
    
    # Metadata
    last_reputation_update = models.DateTimeField(_('last update'), auto_now=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        db_table = 'user_reputations'
        verbose_name = _('user reputation')
        verbose_name_plural = _('user reputations')
    
    def __str__(self):
        return f"{self.user.email} - Reputation: {self.accuracy_score}"

