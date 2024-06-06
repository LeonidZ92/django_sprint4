from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from blogicum.settings import PAGINATOR

from .forms import ProfileEditForm, PostForm, CommentForm

from blog.models import Category
from blog.models import Comment
from blog.models import Post
from blog.models import User


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


def get_posts(post):
    return post.filter(is_published=True,
                       pub_date__lte=timezone.now(),
                       category__is_published=True,
                       ).select_related('author',
                                        'category',
                                        'location',)


class BlogListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    queryset = Post.objects.select_related('author').annotate(
        comment_count=Count('comments')).filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True)
    ordering = '-pub_date'
    paginate_by = PAGINATOR


class CategoryListView(ListView):
    model = Category
    paginate_by = PAGINATOR
    template_name = 'blog/category.html'

    def get_object(self):
        return get_object_or_404(Category,
                                 slug=self.kwargs['category_slug'],
                                 is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_object()
        return context

    def get_queryset(self):
        page_obj = Post.objects.filter(
            category=self.get_object(),
            is_published=True,
            pub_date__lte=timezone.now()
        )
        return page_obj


def get_profile(request, username):
    profile = get_object_or_404(User, username=username)
    user_posts = profile.posts.select_related('author').annotate(
        comment_count=Count('comments')).order_by('-pub_date')
    if not request.user.is_authenticated:
        user_posts = profile.posts.select_related('author').filter(
            pub_date__lte=timezone.now(),
            is_published=True).order_by('-pub_date')

    paginator = Paginator(user_posts, PAGINATOR)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile': profile,
        'page_obj': page_obj,
    }
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:index')
    else:
        form = ProfileEditForm(instance=request.user)
        return render(request, 'blog/user.html', {'form': form})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', post_id=post_id)
    else:
        form = CommentForm()

    return render(request, 'blog/detail.html', {'form': form, 'post': post})


class CommentUpdateView(OnlyAuthorMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'
    success_url = reverse_lazy('blog:index')


class CommentDeleteView(LoginRequiredMixin, OnlyAuthorMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    success_url = reverse_lazy('blog:post_detail')
    pk_url_kwarg = 'comment_id'
    success_url = reverse_lazy('blog:index')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        post = get_object_or_404(
            self.model, id=self.kwargs[self.pk_url_kwarg]
        )
        if post.author == self.request.user:
            return post
        return get_object_or_404(
            Post.custom_manager, id=self.kwargs[self.pk_url_kwarg]
        )

    def get_context_data(self, **kwargs):
        comment_form = CommentForm()
        comments = self.object.comments.select_related('author')

        return {
            **super().get_context_data(**kwargs),
            'form': comment_form,
            'comments': comments,
        }


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save(commit=False)
        post.pub_date = timezone.now()
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user.username
        return reverse('blog:profile', kwargs={'username': user})


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def handle_no_permission(self):
        return redirect(
            'blog:post_detail',
            post_id=self.kwargs[self.pk_url_kwarg]
        )

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs[self.pk_url_kwarg]}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context


class PostDeleteView(LoginRequiredMixin, OnlyAuthorMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.request.user.username})
