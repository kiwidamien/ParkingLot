from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView
from django.utils import timezone
from .forms import NewQuestionForm, PostForm
from .models import Lot, Question, Post

"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('/', views.home_page, name='home'),
    path('/trainings/', views.TrainingListView, name='list_trainings'),
    path('/trainings/<slug:training_id>/', views.QuestionListView,
         name='list_questions'),
]
"""


def home_page(request):
    return render(request, 'homepage.html')


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


def questions_in_lot(request, lot_id):
    lot = get_object_or_404(Lot, slug=lot_id)
    questions = (
        lot.questions.order_by('-last_updated')
        .annotate(replies=Count('posts') - 1)
    )
    return render(request, 'list_of_questions_in_lot.html', {'lot': lot,
                                                             'questions': questions})


def question_comments(request, lot_id, question_pk):
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
