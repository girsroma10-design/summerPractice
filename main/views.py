# views.py
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Post, Comment, Profile, Settings, Category
from .forms import PostForm, CommentForm, ProfileForm, SettingsForm, CategoryForm

from django.shortcuts import render
from .models import Post, Category


def is_admin(user):
    return user.is_staff or user.is_superuser


def home(request):
    featured_posts = Post.objects.filter(is_published=True).exclude(image__exact='').order_by('-published_date')[:3]
    latest_posts = Post.objects.filter(is_published=True).order_by('-published_date')[:5]
    categories = Category.objects.all()

    if request.user.is_authenticated:
        settings_obj, _ = Settings.objects.get_or_create(user=request.user)
        user_theme = settings_obj.theme
    else:
        user_theme = 'light'

    context = {
        'featured_posts': featured_posts,
        'latest_posts': latest_posts,
        'categories': categories,
        'user_theme': user_theme,
    }
    return render(request, 'blog/home.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        raise PermissionDenied("Вы не автор этого поста")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_form.html', {
        'form': form,
        'is_edit': True,
        'post': post,
    })


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        raise PermissionDenied("Вы не автор этого поста")

    if request.method == 'POST':
        post.delete()
        return redirect('home')

    return redirect('post_detail', pk=pk)


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'blog/profile.html', {'form': form})


@login_required
def user_settings(request):
    settings, created = Settings.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = SettingsForm(instance=settings)
    return render(request, 'blog/settings.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                remember_me = request.POST.get('remember_me')
                if remember_me:
                    request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
                else:
                    request.session.set_expiry(0)  # Browser session
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


def category_list(request):
    categories = Category.objects.all()
    selected_category_id = request.GET.get('category')
    selected_category = None

    if selected_category_id:
        try:
            selected_category = categories.get(id=selected_category_id)
            posts = Post.objects.filter(category=selected_category)
        except Category.DoesNotExist:
            selected_category = None
            posts = Post.objects.all()
    else:
        posts = Post.objects.all()

    context = {
        'categories': categories,
        'selected_category': selected_category,
        'posts': posts,
    }
    return render(request, 'blog/category_list.html', context)


@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CategoryForm()
    return render(request, 'blog/create_category.html', {'form': form, 'submit_text': 'Создать',})


@login_required
@user_passes_test(is_admin)
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'blog/create_category.html', {'form': form, 'category': category, 'submit_text': 'Сохранить'})


@login_required
@user_passes_test(is_admin)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'blog/delete_category.html', {'category': category})


@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-published_date')
    return render(request, 'blog/my_posts.html', {'posts': posts})
