from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Issue, Category, UserProfile

def home(request):
    total_issues = Issue.objects.count()
    resolved_issues = Issue.objects.filter(status='Resolved').count()
    active_users = UserProfile.objects.count()
    return render(request, 'issues/home.html', {
        'total_issues': total_issues,
        'resolved_issues': resolved_issues,
        'active_users': active_users
    })

def public_board(request):
    issues = Issue.objects.filter(published=True, status__in=['Pending', 'In Progress'])
    return render(request, 'issues/public_board.html', {'issues': issues})

def accept_issue(request, issue_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to accept issues.')
        return redirect('citizen_login')

    issue = get_object_or_404(Issue, id=issue_id, published=True)
    if issue.status == 'Pending':
        issue.status = 'In Progress'
        issue.accepted_by = request.user
        issue.save()
        if issue.bounty_amount > 0:
            messages.success(request, f'Issue accepted! You can earn ₹{issue.bounty_amount} by solving it.')
        else:
            messages.success(request, 'Issue accepted!')
    return redirect('public_board')

def resolve_issue(request, issue_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to resolve issues.')
        return redirect('citizen_login')

    issue = get_object_or_404(Issue, id=issue_id, published=True)

    # Check if the user accepted this issue
    if issue.accepted_by != request.user:
        messages.error(request, 'You can only resolve issues you have accepted.')
        return redirect('public_board')

    if request.method == 'POST':
        proof = request.FILES.get('proof')
        if proof:
            issue.image = proof
            issue.status = 'Resolved'
            issue.resolved_by = request.user
            issue.save()

            # Award points
            profile = request.user.userprofile
            profile.points += 10
            profile.save()

            # Auto-allot bounty reward if set
            reward_message = 'Issue resolved! You earned 10 points.'
            if issue.bounty_amount > 0:
                # Create automatic reward
                from .models import MonetaryReward
                reward = MonetaryReward.objects.create(
                    user=request.user,
                    issue=issue,
                    amount=issue.bounty_amount,
                    reason=f'Automatically awarded for resolving issue: {issue.title}',
                    allotted_by=None,  # System auto-allot
                    status='Approved'  # Auto-approve bounty rewards
                )
                reward_message += f' and ₹{issue.bounty_amount} bounty reward!'

            messages.success(request, reward_message)
    return redirect('public_board')

def leaderboard(request):
    top_users = UserProfile.objects.order_by('-points')[:10]
    return render(request, 'issues/leaderboard.html', {'top_users': top_users})
