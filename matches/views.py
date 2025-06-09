from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Match
from .forms import MatchCreateForm
from django.db.models import Q


@login_required
def create_match(request):
    if request.user.user_type != 'player':
        messages.error(request, 'Only players can create matches.')
        return redirect('home')
    
    if request.method == 'POST':
        form = MatchCreateForm(request.POST, current_user=request.user)
        if form.is_valid():
            match = form.save(commit=False)
            match.challenger = request.user
            match.save()
            messages.success(request, 'Match request sent! Waiting for opponent confirmation.')
            return redirect('matches:my_matches')
    else:
        form = MatchCreateForm(current_user=request.user)
    
    return render(request, 'matches/create_match.html', {'form': form})

@login_required
def my_matches(request):
    if request.user.user_type != 'player':
        messages.error(request, 'Only players can view matches.')
        return redirect('home')
    

    matches = Match.objects.filter(
        Q(challenger=request.user) | Q(opponent=request.user)
    ).select_related('challenger', 'opponent', 'venue')

    return render(request, 'matches/my_matches.html', {'matches': matches})

@require_POST
@login_required
def confirm_match(request, match_id):
    match = get_object_or_404(Match, id=match_id, opponent=request.user)
    
    if match.status == 'pending':
        match.status = 'confirmed'
        match.save()
        return JsonResponse({'success': True, 'message': 'Match confirmed!'})
    
    return JsonResponse({'success': False, 'message': 'Match cannot be confirmed.'})

@require_POST
@login_required
def cancel_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    

    if request.user in [match.challenger, match.opponent]:
        match.status = 'cancelled'
        match.save()
        return JsonResponse({'success': True, 'message': 'Match cancelled.'})
    
    return JsonResponse({'success': False, 'message': 'You cannot cancel this match.'})
