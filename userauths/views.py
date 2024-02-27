from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.core.paginator import Paginator
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views import View


from post.models import Post, Follow, Stream
from django.contrib.auth.models import User
from userauths.models import Profile
from .forms import EditProfileForm, UserRegisterForm
from django.urls import resolve
from comment.models import Comment


def userProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	url_name= resolve(request.path).url_name
	if url_name == 'profile':
		posts = Post.objects.filter(user=user).order_by('-posted')
	else:
		posts=profile.favourite.all()
	#track stats	
	post_count = Post.objects.filter(user=user).count()
	following_count = Follow.objects.filter(follower=user).count()
	followers_count = Follow.objects.filter(following=user).count()
	#follow stats
	follow_status = Follow.objects.filter(following=user,follower=request.user).exists()
    #paginate
	paginator = Paginator(posts,3)
	page_number = request.GET.get('page')
	posts_paginator = paginator.get_page(page_number)

	context = {
		'posts_paginator': posts_paginator,
		'profile': profile,
		'posts': posts,
		'url_name':url_name,
		'post_count':post_count,
		'followers_count':followers_count,
		'following_count':following_count,
		'follow_status':follow_status,

	}
	return render(request,'profile.html', context)	

def follow(request,username,option):
	user=request.user
	following= get_object_or_404(User,username=username)
	try:
		f,created = Follow.objects.get_or_create(follower=user,following=following)
		if int(option) == 0:
			f.delete()
			Stream.objects.filter(following=following,user=user).all().delete()
		else:
			posts = Post.objects.filter(user=following)[:10]

			with transaction.atomic():
				for post in posts:
					stream = Stream(post=post,user=user,date=post.posted,following=following)
					stream.save()
		return HttpResponseRedirect(reverse('profile', args=[username]))
	except User.DoesNotExist:
		return HttpResponseRedirect(reverse('profile', args=[username]))
def editProfile(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)

    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.image = form.cleaned_data.get('image')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.location = form.cleaned_data.get('location')
            profile.url = form.cleaned_data.get('url')
            profile.bio = form.cleaned_data.get('bio')
            profile.save()
            return redirect('profile',profile.user.username)
    else:
        form = EditProfileForm()

    context = {
        'form':form,
    }
    return render(request, 'edit-profile.html', context)

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # Profile.get_or_create(user=request.user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hurray your account was created!!')

            # Automatically Log In The User
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],)
            login(request, new_user)
            # return redirect('editprofile')
            return redirect('editprofile')
            


    elif request.user.is_authenticated:
        return redirect('index')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'sign-up.html', context)

class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
    	if request.user.is_authenticated:
    		logout(request)
    		#request.session.flush()  # Clear session data
    	return redirect('sign-in')
       

    """def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            if request.user.is_authenticated:
                logout(request)
                request.session.flush()  # Clear session data
            return redirect('sign-in')"""







