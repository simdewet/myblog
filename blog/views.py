from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Images, Comment
from .forms import PostForm, CommentForm
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Display posts on home page
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(posts, 10) # Show 10 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    #return render(request, 'blog/post_list.html', {'posts': posts})
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})

# About page
def about(request):
    return render(request, 'blog/about.html')

# List posts by month
def post_list_month(request, year, month):
    posts = Post.objects.filter(published_date__year=year, published_date__month=month).order_by('-published_date')
    return render(request, 'blog/post_list_month.html', {'posts': posts})

# Display post detail
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post_images = Images.objects.filter(post__pk=pk)
    comments = post.comments.order_by('created_date')
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        commentform = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'post_images': post_images, 'comments': comments, 'commentform': commentform})

# New post form; once fields have been filled correctly, information is saved to database
@login_required
def post_new(request):

    if request.method == "POST":
        postform = PostForm(request.POST)
        if postform.is_valid():
            post = postform.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            # save images to database
            for file in request.FILES.getlist('images'):
                print(file.name)
                instance = Images(post=Post.objects.get(id=post.pk),image=file)
                instance.save()
                
 
            return redirect('post_detail', pk=post.pk)

    else:
        postform = PostForm()

    return render(request, 'blog/post_edit.html', {'form': postform})

# Edit an existing post
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post_images = Images.objects.filter(post__pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            # save images to database
            for file in request.FILES.getlist('images'):
                print(file.name)
                instance = Images(post=Post.objects.get(id=post.pk),image=file)
                instance.save()


            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'post_images': post_images})

# Publish post not yet published
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

# Remove post from database
@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

# Approve comment
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

# Remove comment
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

# Remove image associated with post from database
@login_required
def image_remove(request, pk):
    image = get_object_or_404(Images, pk=pk)
    image.delete()
    return redirect('post_edit', pk=image.post.pk)


