"""
Views for the carbon emission tracking application.
Dashboard, Activity, History, and Goals sections.
"""

import json
from datetime import date, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Sum, Count, Avg
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme

from .models import ActivityType, EmissionRecord, EmissionGoal


# AUTH VIEWS
def login_view(request):
    """Authenticates a user and redirects to the intended page or dashboard."""

    if request.user.is_authenticated:
        return redirect('dashboard')  # Prevents authenticated users from seeing the login form again

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            next_url = request.GET.get('next', '')
            # Validate `next` before redirecting — open redirect vulnerability if skipped
            if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)

            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            # Intentionally vague error — avoids confirming whether the username exists

    return render(request, 'emission_app/login.html')


def logout_view(request):
    """Clears the session and redirects to the login page."""
    logout(request)
    return redirect('login')


# DASHBOARD
@login_required
def dashboard(request):
    """Computes and renders emission summary stats and chart data for the dashboard."""

    # `or 0.0` guards against None when no records exist yet (aggregate returns None on empty sets)
    total_emissions = EmissionRecord.objects.aggregate(
        total=Sum('emission_amount')
    )['total'] or 0.0

    total_records = EmissionRecord.objects.count()

    avg_emission = EmissionRecord.objects.aggregate(
        avg=Avg('emission_amount')
    )['avg'] or 0.0

    # Limit to top 5 so the chart stays readable without crowding the legend
    top_activities = (
        EmissionRecord.objects
        .values('activity__activity_name')
        .annotate(total=Sum('emission_amount'), count=Count('id'))
        .order_by('-total')[:5]
    )
    act_labels = [row['activity__activity_name'] for row in top_activities]
    act_totals = [round(row['total'], 2) for row in top_activities]

    # `select_related` avoids N+1 queries when accessing activity name in the template
    recent_records = EmissionRecord.objects.select_related('activity') \
        .order_by('-date', '-created_at')[:5]

    # Build per-day totals for the last 7 days; fills 0.0 for days with no records
    # so the chart always renders a complete 7-point line without gaps
    today = date.today()
    daily_data = []

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        total = EmissionRecord.objects.filter(date=day).aggregate(
            total=Sum('emission_amount')
        )['total'] or 0.0

        daily_data.append({
            'date': day.strftime('%b %d'),
            'total': round(total, 2)
        })

    # Chart.js requires JSON arrays, so serialise here rather than in the template
    context = {
        'total_emissions': round(total_emissions, 2),
        'total_records': total_records,
        'avg_emission': round(avg_emission, 2),
        'top_activities': top_activities,
        'recent_records': recent_records,
        'daily_data': daily_data,
        'daily_labels_json': json.dumps([d['date'] for d in daily_data]),
        'daily_totals_json': json.dumps([d['total'] for d in daily_data]),
        'act_labels_json': json.dumps(act_labels),
        'act_totals_json': json.dumps(act_totals),
    }

    return render(request, 'emission_app/dashboard.html', context)



# ACTIVITY
@login_required
def activity(request):
    """Handles two POST actions on one view: logging a record and adding an activity type."""

    if request.method == 'POST':
        # Single endpoint handles both forms; `action` field distinguishes which was submitted
        action = request.POST.get('action')

        if action == 'add_record':
            activity_id = request.POST.get('activity_id')
            quantity = request.POST.get('quantity')
            record_date = request.POST.get('date')
            description = request.POST.get('description', '')

            try:
                activity_type = get_object_or_404(ActivityType, pk=activity_id)
                qty = float(quantity)

                if qty <= 0:
                    raise ValueError("Quantity must be positive")  # Negative CO2 is physically meaningless

                # `emission_amount` is intentionally omitted — EmissionRecord.save() auto-calculates it
                EmissionRecord.objects.create(
                    activity=activity_type,
                    quantity=qty,
                    date=record_date or date.today(),  # Falls back to today if the user left the field empty
                    description=description,
                )

                messages.success(request, 'Emission record added successfully!')

            except (ValueError, TypeError) as e:
                messages.error(request, f'Invalid input: {e}')

            return redirect('activity')  # PRG pattern — prevents duplicate submissions on browser refresh

        elif action == 'add_activity':
            name = request.POST.get('activity_name', '').strip()
            factor = request.POST.get('emission_factor')
            unit = request.POST.get('unit', '').strip()

            try:
                # Both are required — an activity without a name or unit can't be meaningfully logged
                if not name or not unit:
                    raise ValueError("Name and unit are required")

                ActivityType.objects.create(
                    activity_name=name,
                    emission_factor=float(factor),
                    unit=unit,
                )

                messages.success(request, f'Activity type "{name}" added successfully!')

            except (ValueError, TypeError) as e:
                messages.error(request, f'Invalid input: {e}')

            return redirect('activity')  # PRG pattern — same reason as above

    # Annotate with usage stats so the catalog table can show record counts without extra queries
    activity_types = ActivityType.objects.annotate(
        record_count=Count('emissionrecord'),
        total_emissions=Sum('emissionrecord__emission_amount'),
    ).order_by('activity_name')

    context = {
        'activity_types': activity_types,
        'today': date.today(),  # Passed so the date input defaults to today in the template
    }

    return render(request, 'emission_app/activity.html', context)



# HISTORY
 

@login_required
def history(request):
    """Returns emission history with optional filters; builds chart data from the filtered set."""

    # Start with all records; filters are applied progressively below
    records = EmissionRecord.objects.select_related('activity') \
        .order_by('-date', '-created_at')

    activity_filter = request.GET.get('activity')
    if activity_filter:
        records = records.filter(activity__id=activity_filter)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Both filters are optional and independent — applied only when the param is non-empty
    if start_date:
        records = records.filter(date__gte=start_date)
    if end_date:
        records = records.filter(date__lte=end_date)

    # Compute total after filtering so the summary reflects exactly what's on screen
    total_filtered = records.aggregate(
        total=Sum('emission_amount')
    )['total'] or 0.0

    activity_types = ActivityType.objects.order_by('activity_name')

    # Group by day so the trend chart shows one bar per date, not one per record
    daily_agg = (
        records.values('date')
        .annotate(total=Sum('emission_amount'))
        .order_by('date')  # Ascending — chart reads left-to-right chronologically
    )

    chart_dates = [str(row['date']) for row in daily_agg]
    chart_totals = [round(row['total'], 2) for row in daily_agg]

    # Separate breakdown by activity type for the donut chart
    by_activity = (
        records.values('activity__activity_name')
        .annotate(total=Sum('emission_amount'))
        .order_by('-total')  # Highest emitting activities appear first in the legend
    )

    act_labels = [row['activity__activity_name'] for row in by_activity]
    act_totals = [round(row['total'], 2) for row in by_activity]

    context = {
        'records': records,
        'total_filtered': round(total_filtered, 2),
        'activity_types': activity_types,
        'activity_filter': activity_filter,
        'start_date': start_date,
        'end_date': end_date,
        'chart_dates': chart_dates,
        'chart_dates_json': json.dumps(chart_dates),
        'chart_totals_json': json.dumps(chart_totals),
        'act_labels_json': json.dumps(act_labels),
        'act_totals_json': json.dumps(act_totals),
    }

    return render(request, 'emission_app/history.html', context)


# DELETE RECORD

@login_required
def delete_record(request, record_id):
    """Deletes a single emission record. POST-only to block accidental deletions via GET."""
    if request.method == 'POST':
        record = get_object_or_404(EmissionRecord, pk=record_id)
        record.delete()
        messages.success(request, 'Record deleted successfully.')

    # Always redirect — GET requests silently fall through without deleting anything
    return redirect('history')



# GOALS
@login_required
def goals(request):
    """Manages goals and computes live progress by summing records within each goal's period window."""

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add_goal':
            title = request.POST.get('title', '').strip()
            target = request.POST.get('target_emission')
            period = request.POST.get('period', 'monthly')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date') or None  # Empty string → None so the DB stores NULL, not ""
            notes = request.POST.get('notes', '').strip()

            try:
                if not title:
                    raise ValueError("Title is required")

                EmissionGoal.objects.create(
                    title=title,
                    target_emission=float(target),
                    period=period,
                    start_date=start_date or date.today(),
                    end_date=end_date,
                    notes=notes,
                )

                messages.success(request, f'Goal "{title}" added successfully!')

            except (ValueError, TypeError) as e:
                messages.error(request, f'Invalid input: {e}')

            return redirect('goals')

        elif action == 'delete_goal':
            goal_id = request.POST.get('goal_id')
            goal = get_object_or_404(EmissionGoal, pk=goal_id)
            goal.delete()
            messages.success(request, 'Goal deleted successfully.')

            return redirect('goals')

    all_goals = EmissionGoal.objects.all()
    today = date.today()

    goals_with_progress = []

    for goal in all_goals:
        # Determine the date range to query based on the goal's recurrence period
        if goal.period == 'daily':
            start = end = today  # Daily goals only count today's records
        elif goal.period == 'weekly':
            start = today - timedelta(days=today.weekday())  # Monday of the current week
            end = start + timedelta(days=6)                  # Sunday of the current week
        else:
            start = today.replace(day=1)  # First day of the current month
            if today.month == 12:
                end = today.replace(month=12, day=31)
            else:
                # First day of next month minus one day — handles variable month lengths
                end = today.replace(month=today.month + 1, day=1) - timedelta(days=1)

        actual = EmissionRecord.objects.filter(
            date__gte=start,
            date__lte=end
        ).aggregate(total=Sum('emission_amount'))['total'] or 0.0

        actual = round(actual, 2)

        # Cap at 200% so a severely exceeded goal doesn't break the progress bar layout
        pct = min(
            round((actual / goal.target_emission) * 100, 1),
            200
        ) if goal.target_emission else 0  # Guard against division by zero if target is 0

        goals_with_progress.append({
            'goal': goal,
            'actual': actual,
            'pct': pct,
            'over_target': actual > goal.target_emission,  # Drives the red/green indicator in the template
        })

    # Extract parallel arrays for the target-vs-actual comparison chart
    goal_labels = [g['goal'].title for g in goals_with_progress]
    goal_targets = [g['goal'].target_emission for g in goals_with_progress]
    goal_actuals = [g['actual'] for g in goals_with_progress]

    context = {
        'goals_with_progress': goals_with_progress,
        'today': today,
        'period_choices': EmissionGoal.PERIOD_CHOICES,
        'goal_labels_json': json.dumps(goal_labels),
        'goal_targets_json': json.dumps(goal_targets),
        'goal_actuals_json': json.dumps(goal_actuals),
    }

    return render(request, 'emission_app/goals.html', context)