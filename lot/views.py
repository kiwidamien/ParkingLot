from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView
from .forms import NewQuestionForm
from .models import Lot, Post

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
    return render(request, 'list_of_questions_in_lot.html', {'lot': lot})
