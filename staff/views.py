from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from issues.models import Issue, UserProfile, Category, MonetaryReward
from django.contrib.auth.models import User
from django.utils import timezone
import json

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.userprofile.role in ['Staff', 'Admin']:
                login(request, user)
                return redirect('staff_dashboard')
            else:
                messages.error(request, 'Invalid credentials for Staff login.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'staff/login.html')

@login_required
def staff_dashboard(request):
    if request.user.userprofile.role not in ['Staff', 'Admin']:
        return redirect('citizen_dashboard')
    category_filter = request.GET.get('category')
    status_filter = request.GET.get('status')
    issues = Issue.objects.all()
    if category_filter:
        issues = issues.filter(category__name=category_filter)
    if status_filter:
        issues = issues.filter(status=status_filter)
    categories = Category.objects.all()

    # Analytics data
    total_issues = Issue.objects.count()
    pending_count = Issue.objects.filter(status='Pending').count()
    in_progress_count = Issue.objects.filter(status='In Progress').count()
    resolved_count = Issue.objects.filter(status='Resolved').count()

    category_counts = {}
    for cat in categories:
        category_counts[cat.name] = Issue.objects.filter(category=cat).count()

    return render(request, 'staff/dashboard.html', {
        'issues': issues,
        'categories': categories,
        'total_issues': total_issues,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'resolved_count': resolved_count,
        'category_counts': category_counts,
        'status_data': json.dumps([pending_count, in_progress_count, resolved_count]),
        'category_labels': json.dumps(list(category_counts.keys())),
        'category_data': json.dumps(list(category_counts.values())),
    })

@login_required
def update_status(request, issue_id):
    if request.user.userprofile.role not in ['Staff', 'Admin']:
        return redirect('citizen_dashboard')
    issue = get_object_or_404(Issue, id=issue_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'In Progress', 'Resolved']:
            issue.status = new_status
            if new_status == 'Resolved':
                issue.resolved_by = request.user
            issue.save()
            messages.success(request, 'Status updated successfully!')
    return redirect('staff_dashboard')

@login_required
def publish_issue(request, issue_id):
    if request.user.userprofile.role not in ['Staff', 'Admin']:
        return redirect('citizen_dashboard')
    issue = get_object_or_404(Issue, id=issue_id)
    if request.method == 'POST':
        bounty_amount = request.POST.get('bounty_amount', 0)
        issue.published = True
        issue.bounty_amount = bounty_amount
        issue.save()
        if float(bounty_amount) > 0:
            messages.success(request, f'Issue published to public with ₹{bounty_amount} bounty!')
        else:
            messages.success(request, 'Issue published to public!')
    return redirect('staff_dashboard')

@login_required
def manage_rewards(request):
    if request.user.userprofile.role not in ['Staff', 'Admin']:
        return redirect('citizen_dashboard')

    rewards = MonetaryReward.objects.all().order_by('-allotted_at')
    users = User.objects.filter(userprofile__role='Citizen')
    issues = Issue.objects.all()

    # Calculate statistics
    total_reward_value = sum(reward.amount for reward in rewards)
    average_reward = total_reward_value / len(rewards) if rewards else 0

    return render(request, 'staff/manage_rewards.html', {
        'rewards': rewards,
        'users': users,
        'issues': issues,
        'total_reward_value': total_reward_value,
        'average_reward': round(average_reward, 2),
    })

@login_required
def allot_reward(request):
    if request.user.userprofile.role not in ['Staff', 'Admin']:
        return redirect('citizen_dashboard')

    if request.method == 'POST':
        user_id = request.POST.get('user')
        issue_id = request.POST.get('issue')
        amount = request.POST.get('amount')
        reason = request.POST.get('reason')

        try:
            user = User.objects.get(id=user_id)
            issue = Issue.objects.get(id=issue_id) if issue_id else None

            reward = MonetaryReward.objects.create(
                user=user,
                issue=issue,
                amount=amount,
                reason=reason,
                allotted_by=request.user,
                status='Approved'  # Auto-approve for simplicity
            )

            messages.success(request, f'₹{amount} reward allotted to {user.username} successfully!')
            return redirect('manage_rewards')

        except Exception as e:
            messages.error(request, f'Error allotting reward: {str(e)}')

    return redirect('manage_rewards')

@login_required
def update_reward_status(request, reward_id):
    if request.user.userprofile.role not in ['Staff', 'Admin']:
        return redirect('citizen_dashboard')

    reward = get_object_or_404(MonetaryReward, id=reward_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Approved', 'Paid', 'Rejected']:
            reward.status = new_status
            if new_status == 'Paid':
                reward.paid_at = timezone.now()
                reward.payment_reference = request.POST.get('payment_reference', '')
            reward.save()
            messages.success(request, f'Reward status updated to {new_status}!')

    return redirect('manage_rewards')
