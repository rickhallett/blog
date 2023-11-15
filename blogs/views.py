from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Post
from .forms import EmailPostForm
from django.core.mail import send_mail


def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 8)
    pg_num = request.GET.get('page', 1)
    try:
        posts = paginator.page(pg_num)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except InvalidPage:
        Http404('Can\'t find this post!')

    return render(request=request, template_name='blogs/post/list.html', context={'posts': posts})


class PostListView(ListView):
    queryset = Post.published.all()[:25]
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'blogs/post/list.html'


def post_detail(request, post_id):
    try:
        post = Post.published.get(id=post_id)
    except Post.DoesNotExist as ex:
        raise Http404(f'post {post_id} not found')

    return render(request, 'blogs/post/detail.html', {'post': post})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year, publish__month=month,
                             publish__day=day)

    return render(request, 'blogs/post/detail.html', {'post': post})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'rickjhallett@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blogs/post/share.html', {'post': post, 'form': form})
