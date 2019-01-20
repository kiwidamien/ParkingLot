from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView
from django.utils import timezone
from django.utils.text import slugify
from .forms import NewQuestionForm, PostForm, FindLotForm
from .models import Lot, Question, Post


def home_page(request):
    if request.method == 'POST':
        form = FindLotForm(request.POST)
        if form.is_valid():
            the_slug = slugify(form.cleaned_data.get('lot_slug'))
            lot = get_object_or_404(Lot, slug=the_slug)
            return redirect('list_questions', lot_id=lot.slug)
    else:
        form = FindLotForm()
    return render(request, 'homepage.html', {'form': form})


class LotListView(ListView):
    model = Lot
    context_object_name = 'lots'
    template_name = 'list_lots.html'


def new_question(request, lot_id):
    lot = get_object_or_404(Lot, slug=lot_id)
    if request.method == 'POST':
        form = NewQuestionForm(request.POST)
        user = User.objects.first()

        if form.is_valid():
            question = form.save(commit=False)
            question.lot = lot
            question.starter = user
            question.save()

            Post.objects.create(
                message=form.cleaned_data.get('message'),
                question=question,
                created_by=user
            )

            return redirect('list_questions', lot_id=lot.slug)
    else:
        form = NewQuestionForm()
    return render(request, 'new_question.html', {'lot': lot, 'form': form})


class QuestionListView(ListView):
    """
    This is the class-based view, which is performs the same function
    as the function-based view questions_in_lot(...) below
    """
    model = Question
    context_object_name = 'questions'
    template_name = 'list_of_questions_in_lot.html'

    def get_context_data(self, **kwargs):
        kwargs['lot'] = self.lot
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.lot = get_object_or_404(Lot, slug=self.kwargs.get('lot_id'))
        questions = (
            self.lot.questions
            .order_by('-last_updated')
            .annotate(replies=Count('posts') - 1)
        )
        return questions


def questions_in_lot(request, lot_id):
    """
    This function implements the same view as QuestionListView does
    """
    lot = get_object_or_404(Lot, slug=lot_id)
    questions = (
        lot.questions.order_by('-last_updated')
        .annotate(replies=Count('posts') - 1)
    )
    return render(request, 'list_of_questions_in_lot.html', 
                  {'lot': lot, 'questions': questions})


class PostListView(ListView):
    """
    This CBV implements the same functionality as the FBV 'question_comments'
    """
    model = Post
    context_object_name = 'posts'
    template_name = 'comments_on_question.html'

    def get_context_data(self, **kwargs):
        session_key = f'viewed_question_{self.question.pk}'
        if not self.request.session.get(session_key, False):
            self.question.views += 1
            self.question.save()
            self.request.session[session_key] = True

        kwargs['question'] = self.question
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.question = get_object_or_404(Question,
                                          lot__slug=self.kwargs.get('lot_id'),
                                          pk=self.kwargs.get('question_pk'))
        queryset = self.question.posts.order_by('created_at')
        return queryset


def question_comments(request, lot_id, question_pk):
    """
    This FBV implements the same view as the CBV PostListView
    """
    question = get_object_or_404(Question, lot__slug=lot_id, pk=question_pk)
    question.views += 1
    question.save()
    return render(request, 'comments_on_question.html', {'question': question})


def post_comment(request, lot_id, question_pk):
    question = get_object_or_404(Question, lot__slug=lot_id, pk=question_pk)
    user = User.objects.first()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.question = question
            post.created_by = user
            post.save()

            question.last_updated = timezone.now()
            question.save()
            return redirect('question_comments', lot_id=lot_id,
                            question_pk=question_pk)
    else:
        form = PostForm()
    return render(request, 'post_comment.html', {'question': question, 'form':
                                                 form})


class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_comment.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('question_comments', lot_id=post.question.lot.slug,
                        question_pk=post.question.pk)
