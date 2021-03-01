from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from . forms import *
from . models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


def posts_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Post/posts_list.html', context={'posts': page_obj.object_list, 'paginator': paginator, 'page_number': page_number, 'page_obj': page_obj})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments_posts = post.comments_posts.all()
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()
    
    return render(request, 'Post/post_detail.html', locals())

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            photo = form.instance
            return redirect('posts_list')
    else:
        form = PostForm()
    return render(request, 'Post/post_create.html', locals())




class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'Post/post_create.html'
    context_object_name = 'post'
    form_class = PostForm


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST" and post.author == request.user:
        post.delete()
        return redirect('posts_list')
    return render(request, 'Post/post_delete.html', locals())
    
@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = get_object_or_404(Post, pk=comment.post.pk)
    if request.method == "POST" and post.author == request.user:
        comment.delete()
        return redirect(post.get_absolute_url())
    return render(request, 'Post/comment_delete.html', locals())


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'Post/tags_list.html', locals())


def tag_detail(request, slug):
    tag = Tag.objects.get(slug__iexact=slug)
    return render(request, 'Post/tag_detail.html', locals())