from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render

from .forms import ProfileForm, RegisterForm
from .models import Profile


def register(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	form = RegisterForm(request.POST or None, initial={'role': request.GET.get('role', Profile.CANDIDATE)})
	if form.is_valid():
		user = form.save()
		login(request, user)
		return redirect('dashboard')
	return render(request, 'users/register.html', {'form': form})


def login_view(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	form = AuthenticationForm(request, data=request.POST or None)
	if form.is_valid():
		login(request, form.get_user())
		return redirect(request.GET.get('next') or 'dashboard')
	return render(request, 'users/login.html', {'form': form})


def logout_view(request):
	if request.method == 'POST':
		logout(request)
	return redirect('login')


@login_required
def profile(request):
	user_profile, _ = Profile.objects.get_or_create(user=request.user)
	form = ProfileForm(request.POST or None, request.FILES or None, instance=user_profile)
	if form.is_valid():
		form.save()
		messages.success(request, 'Profile updated.')
		return redirect('profile')
	return render(request, 'users/profile.html', {'form': form, 'profile': user_profile})


def candidate_directory(request):
	if not request.user.is_authenticated:
		return redirect(f'/users/login/?next={request.path}')
	if not hasattr(request.user, 'profile') or request.user.profile.role != Profile.EMPLOYER:
		raise PermissionDenied('Only employers can browse candidate profiles.')
	query = request.GET.get('q', '').strip()
	candidates = Profile.objects.filter(role=Profile.CANDIDATE).select_related('user')
	if query:
		candidates = candidates.filter(
			Q(user__username__icontains=query)
			| Q(user__first_name__icontains=query)
			| Q(user__last_name__icontains=query)
			| Q(bio__icontains=query)
		)
	return render(request, 'users/candidates.html', {'candidates': candidates, 'query': query})


def candidate_detail(request, pk):
	if not request.user.is_authenticated:
		return redirect(f'/users/login/?next={request.path}')
	if not hasattr(request.user, 'profile') or request.user.profile.role != Profile.EMPLOYER:
		raise PermissionDenied('Only employers can view candidate profiles.')
	candidate = get_object_or_404(
		Profile.objects.select_related('user'), pk=pk, role=Profile.CANDIDATE
	)
	return render(request, 'users/candidate_detail.html', {'candidate': candidate})
