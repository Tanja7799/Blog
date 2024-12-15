from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages #меседжі користувачу
from taggit.models import Tag
from django.shortcuts import redirect#перенаправлення
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def post_list(request, tag_slug=None):
    posts = Post.objects.filter(status='published')
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])



    paginator = Paginator(posts, 3)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)



    return render(request, 'blog/post/list.html',{'posts': posts, 'page': page,
                                                                         'tag': tag})


def post_detail(request, year, month, day, slug_post):
    post = get_object_or_404(Post, status='published',
                                   slug=slug_post,
                                   publish__year = year,
                                   publish__month = month ,
                                   publish__day = day)

    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()


    context = {'post': post,
               'comments': comments,
                'comment_form': comment_form}
    return render(request, 'blog/post/detail.html', context=context)



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Створено акаунт {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user) ##instance=request.user візьмуться поточні дані з профілю
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context=context)

def logout_confirm(request):
    return render(request, 'users/logout_confirm.html')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'body', 'slug']

    def form_valid(self, form):
        form.instance.author = self.request.user #поєднує автора з новим постом
        return super().form_valid(form) # зветраємось у батьківський клас

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'body', 'slug']

    def form_valid(self, form):
        form.instance.author = self.request.user  # поєднує автора з новим постом
        return super().form_valid(form)  # зветраємось у батьківський клас

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDelateView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    #перевіряємо чи є він автором
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False















