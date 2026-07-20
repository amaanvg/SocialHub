from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm


@login_required(login_url='login')
def home(request):

    if request.method == 'POST':

        form = PostForm(request.POST)

        if form.is_valid():

            post = form.save(commit=False)
            post.user = request.user
            post.save()

            return redirect('home')

    else:

        form = PostForm()

    posts = Post.objects.all().order_by('-created_at')

    comment_form = CommentForm()

    context = {
    'form': form,
    'comment_form': comment_form,
    'posts': posts
}

    return render(request, 'home.html', context)

@login_required(login_url='login')
def delete_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        user=request.user
    )

    if request.method == "POST":
        post.delete()

    return redirect('home')

@login_required(login_url='login')
def like_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('home')

@login_required(login_url='login')
def add_comment(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()

    return redirect('home')