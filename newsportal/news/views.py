from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect

from django.core.cache import cache

from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import *
from .forms import NewsForm
from .filters import PostFilter
from .utils import MyMixin


class HomeNewsView(ListView):
    model = Post
    template_name = 'news/index.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


class NewsByCategory(ListView):
    model = Post
    template_name = 'news/category.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return Post.objects.filter(category_id=self.kwargs['category_id'])


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/view_news.html'
    context_object_name = 'post'
    pk_url_kwarg = 'news_id'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f"product-{self.kwargs['news_id']}", None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f"post-{self.kwargs['news_id']}", obj)
            return obj


class ArticleView(ListView):
    model = Post
    template_name = 'news/articles.html'
    context_object_name = 'articles'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статьи'
        return context

    def get_queryset(self):
        return Post.objects.filter(type_category='AR')


class NewsView(ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новости'
        return context

    def get_queryset(self):
        return Post.objects.filter(type_category='NW')


# {% if perms.news.add_post %} в _nav.html
class CreateNews(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('home')
    # login_url = '/admin/'


class UpdateNews(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    model = Post
    form_class = NewsForm
    template_name = 'news/add_news.html'


class DeleteNews(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post', )
    model = Post
    template_name = 'news/delete_news.html'
    success_url = reverse_lazy('home')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(user=request.user, category=category).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user, category=OuterRef('pk')
            )
        )
    ).order_by('name')
    return render(request, 'subscriptions.html', {'categories': categories_with_subscriptions})


# class SearchPost(ListView):
#     model = Post
#     template_name = 'search.html'
#     context_object_name = 'search'
#     paginate_by = 5
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         self.filterset = PostFilter(self.request.GET, queryset)
#
#         return self.filterset.qs
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['filterset'] = self.filterset
#         return context


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})


