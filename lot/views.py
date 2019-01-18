from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView
from .models import Lot

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
        subject = request.POST['subject']
        message = request.POST['message']

        user = User.objects.first()

        question = Question.objects.create(
            subject=subject, lot=lot, starter=user
        )

        post = Post.objects.create(
            message=message,
            lot=lot,
            created_by=user
        )

        return redirect('list_questions', pk=lot.pk)
    return render(request, 'new_question.html', {'lot': lot})


def questions_in_lot(request, lot_id):
    lot = get_object_or_404(Lot, slug=lot_id)
    return render(request, 'list_of_questions_in_lot.html', {'lot': lot})
