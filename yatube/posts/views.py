from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, Group, User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import PostForm


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Отдаем в словаре контекста
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list_user = user.posts.all().filter(author__username=username)
    paginator = Paginator(post_list_user, 10)
    page_number = request.GET.get('page')
    post_count = post_list_user.count()
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'post_count': post_count,
        'author': user,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post_count = Post.objects.filter(author_id=post.author.id).count()
    context = {
        'post_count': post_count,
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)
   

@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if not form.is_valid():
        context = {'form': form}
        return render(request, 'posts/post_create.html', context)
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('posts:profile', post.author)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if not form.is_valid():
        return render(request, 'posts/post_create.html', {
            'form': form,
            'post': post,
            'post_id': post_id,
            'is_edit': True
        })
    form.save()
    return redirect('posts:post_detail', post_id=post_id)
