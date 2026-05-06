"""
Models for the emission tracking application.
"""

from django.db import models


class ActivityType(models.Model):
    """Represents a type of emission-generating activity with its CO2 conversion factor."""

    # Human-readable name for the activity (e.g., "Car Travel", "Electricity Use")
    activity_name = models.CharField(max_length=100, unique=True)

    # Amount of CO2 (in kg) produced per one unit of this activity
    emission_factor = models.FloatField(help_text="kg CO2 per unit")

    # The unit of measurement for this activity (e.g., "km", "kWh", "kg")
    unit = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.activity_name} ({self.emission_factor} kg CO2/{self.unit})"


class EmissionRecord(models.Model):
    """Logs a single emission event tied to a specific activity and date."""

    # Links to the activity type that determines the emission factor used
    activity = models.ForeignKey(ActivityType, on_delete=models.CASCADE)

    # User-inputted amount of the activity performed (e.g., 50 km driven)
    quantity = models.FloatField()

    # Calculated CO2 emission — auto-computed from quantity × emission_factor on save
    emission_amount = models.FloatField(help_text="kg CO2")

    # The date on which the activity occurred
    date = models.DateField()

    # Optional user notes about this specific record
    description = models.TextField(blank=True, default="")

    # Timestamp set automatically when the record is first created
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-calculate CO2 emission before persisting to avoid manual entry errors
        self.emission_amount = self.quantity * self.activity.emission_factor
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.activity.activity_name} - {self.emission_amount:.2f} kg CO2 on {self.date}"

    class Meta:
        # Most recent entries appear first in queries and the dashboard
        ordering = ['-date', '-created_at']


class EmissionGoal(models.Model):
    """Defines a user-set CO2 reduction target for a given time period."""

    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    # Short descriptive name for the goal (e.g., "Reduce commute emissions")
    title = models.CharField(max_length=100)

    # The maximum CO2 (in kg) the user aims not to exceed within the period
    target_emission = models.FloatField(help_text="Target kg CO2 per period")

    # Recurrence window over which the target is measured
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='monthly')

    # The date from which progress tracking begins
    start_date = models.DateField()

    # Optional end date — if blank, the goal is treated as ongoing
    end_date = models.DateField(null=True, blank=True)

    # Any additional context or motivation the user wants to record
    notes = models.TextField(blank=True, default="")

    # Timestamp set automatically when the goal is created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.target_emission} kg CO2/{self.period})"

    class Meta:
        # Newest goals appear first in lists and the dashboard
        ordering = ['-created_at']