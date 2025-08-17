from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View
from .models import Post, Comment
from .forms import CommentForm



# Add comment to a post
class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
        return redirect('post-detail', pk=post.pk)

# Edit a comment
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

# Delete a comment
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        post_pk = comment.post.pk
        comment.delete()
        return redirect('post-detail', pk=post_pk)

    def test_func(self):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        return self.request.user == comment.author
