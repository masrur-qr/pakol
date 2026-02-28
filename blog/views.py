from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from blog.models import Post, Comment, CommentForm
# from blog.forms import  CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from django.shortcuts import redirect
# from django.conf import settings
from django.contrib.auth.decorators import login_required

from tours.models import Tour
from home.models import SEO_Optimiser

# Create your views here.

# def blog_index(request):
#     return render(request, 'blog/blog_index.html')

def blog_list(request):
    template = 'blog/blog_index.html'
    posts = Post.objects.filter(status='published')
    common_tags = Post.tags.most_common()[:4]
     

    recent_posts = Post.objects.filter(status='published').order_by("-Created")[:3]
    #Paginator
    paginator = Paginator(posts, 6) # Show n posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    # categories = Category.objects.all()
    SEO = SEO_Optimiser.objects.get(id=1)
    tags = Post.tags.all()
    
    args = {
        'posts': posts,
        'common_tags':common_tags,
        'recent_posts': recent_posts,
        'SEO': SEO,
        'tags':tags,
    }
    return render(request, template, args)

# @login_required
def details(request, Slug):
    # categories = Category.objects.all()
    recent_posts = Post.objects.filter(status='published').order_by("-Created")[:3]
    post=Post.objects.get(Slug=Slug)
    # post=Post.objects.get(id=id)
    
    post_related = post.tags.similar_objects()[:3]
    # post_related = Tour.tags.similar_objects()[:3]

    posttags = post.tags.all()
    # tours_related = Tour.objects.filter(Available=True).filter(tags__in=posttags)[:3]
    tags = Post.tags.all()
    context = {
        'post' : post,
        'recent_posts':recent_posts,
        # 'form': form,
        'post_related': post_related,
        # 'tours_related': tours_related,
        'tags': tags,
        # 'obj': obj 
    }
    return render(request, 'blog/blog_details.html',context)

def detail_view(request, slug):
    post = get_object_or_404(Post, Slug=slug)
    context = {
        'post':post,
        'recent_posts': recent_posts,
    }
    return render(request, 'blog/blog_details.html', context)

def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name  
    posts = Post.objects.filter(tags=tag)
    context = {
        'tag':tag,
        'posts':posts,
    }
    return render(request, 'blog/blog_index.html', context)

def add_comment_to_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:details',  Slug=post.Slug) #id=post.id,
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, id):
    comment = get_object_or_404(Comment, id=id)
    comment.approve()
    return redirect('blog:details',  Slug=comment.post.Slug) #id=comment.post.id,

@login_required
def comment_remove(request, id):
    comment = get_object_or_404(Comment, id=id)
    comment.delete()
    return redirect('blog:details',  Slug=comment.post.Slug) #id=comment.post.id,


def approved_comments(self):
    return self.comments.filter(approved_comment=True)

