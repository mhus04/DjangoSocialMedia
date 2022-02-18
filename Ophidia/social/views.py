from ast import Num
from dataclasses import fields
from multiprocessing import context
from re import template
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import Post, Comment, ThreadModel, UserProfile, MessageModel
from .forms import PostForm, CommentForm, ThreadForm, MessageForm
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.models import User
from django.db.models import Q

class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm()
        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'social/post_list.html', context)
    
    def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit = False)
            new_post.author = request.user
            new_post.save()

        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'social/post_list.html', context)
    
    

class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()

        comments = Comment.objects.filter(post = post).order_by('-created_on')

        context = {
            'post' : post,
            'form' : form,
            'comments' : comments,
        }

        return render(request, 'social/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk = pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit = False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        comments = Comment.objects.filter(post = post).order_by('-created_on')

        context = {
            'post' : post,
            'form' : form,
            'comments' : comments,
        }

        return render(request, 'social/post_detail.html', context)

class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['body']
    template_name = 'social/post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs = {'pk' : pk})
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'social/post_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'social/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail', kwargs = {'pk' : pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk = pk)
        user = profile.user
        posts = Post.objects.filter(author = user).order_by('-created_on')

        followers = profile.followers.all()
        number_of_followers = len(followers)

        if number_of_followers == 0:
            is_following = False

        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False

        context = {
            'user' : user,
            'profile' : profile,
            'posts' : posts,
            'number_of_followers' : number_of_followers,
            'is_following' : is_following,
        }

        return render(request, 'social/profile.html', context)

class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['name', 'bio', 'birth_date', 'location', 'picture']
    template_name = 'social/profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs = {'pk' : pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user

class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk = pk)
        profile.followers.add(request.user)

        return redirect('profile', pk = profile.pk)

class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk = pk)
        profile.followers.remove(request.user)

        return redirect('profile', pk = profile.pk)

class Like(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk = pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        
        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        
        if is_like:
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class Dislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk = pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        
        if is_like:
            post.likes.remove(request.user)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        
        if is_dislike:
            post.dislikes.remove(request.user)
        else:
            post.dislikes.add(request.user)
        
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        profile_list = UserProfile.objects.filter(
            Q(user__username__icontains = query)
        )

        context = {
            'profile_list' : profile_list,
            'query' : query,
        }

        return render(request, 'social/search.html', context)

class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user = request.user) | Q(receiver = request.user))

        context = {
            'threads' : threads
        }

        return render(request, 'social/inbox.html', context)

class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()

        context = {
            'form' : form
        }

        return render(request, 'social/create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        username = request.POST.get('username')

        try:
            receiver = User.objects.get(username = username)
            if ThreadModel.objects.filter(user = request.user, receiver = receiver).exists():
                thread = ThreadModel.objects.filter(user = request.user, receiver = receiver)[0]
                return redirect('thread', pk = thread.pk)
            elif ThreadModel.objects.filter(user = receiver, receiver = request.user).exists():
                thread = ThreadModel.objects.filter(user = receiver, receiver = request.user)[0]
                return redirect('thread', pk = thread.pk)
            
            if form.is_valid():
                thread = ThreadModel(
                    user = request.user,
                    receiver = receiver,
                )
                thread.save()
            
                return redirect('thread', pk = thread.pk)
        except:
            return redirect('create-thread')

class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk = pk)
        message_list = MessageModel.objects.filter(thread__pk__contains = pk)
        context = {
            'thread' : thread,
            'form' : form,
            'message_list' : message_list
        }

        return render(request, 'social/thread.html', context)

class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        thread = ThreadModel.objects.get(pk = pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver
        
        message = MessageModel(
            thread = thread,
            sender_user = request.user,
            receiver_user = receiver,
            body = request.POST.get('message')
        )

        message.save()
        return redirect('thread', pk = pk)