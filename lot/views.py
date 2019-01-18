from django.shortcuts import render
from django.views.generic import CreateView, ListView
from .models import Lot
# Create your views here.
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


class QuestionListView(ListView):
    pass

