from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Post, Comment
from .forms import PostForm, CommentForm

# ------------------------
# Post CRUD
# ------------------------

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# ------------------------
# Comment CRUD
# ------------------------

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
        return redirect('post-detail', pk=post.pk)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        form = CommentForm(instance=comment)
        return render(request, 'blog/comment_form.html', {'form': form, 'comment': comment})

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post-detail', pk=comment.post.pk)
        return render(request, 'blog/comment_form.html', {'form': form, 'comment': comment})

    def test_func(self):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        return self.request.user == comment.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        post_pk = comment.post.pk
        comment.delete()
        return redirect('post-detail', pk=post_pk)

    def test_func(self):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        return self.request.user == comment.author

# ------------------------
# Tag Filtering
# ------------------------

class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        return Post.objects.filter(tags__slug=tag_slug)

# ------------------------
# Search
# ------------------------

def search_posts(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    return render(request, 'blog/search_results.html', {'results': results, 'query': query})
