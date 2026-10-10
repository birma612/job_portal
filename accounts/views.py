
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UserProfileForm
from .models import UserProfile


@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Your profile has been updated successfully.'
            )
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(
        request,
        'accounts/profile.html',
        {'form': form, 'profile': profile}
    )
