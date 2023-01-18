from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
#from django.template import loader
from .models import Question, Answer
from django.views import generic
from django.utils import timezone
from .form import QuestionsForm

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'mc_and_datasheet/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now() # publication date less than or equal to
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'mc_and_datasheet/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'mc_and_datasheet/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    form = QuestionsForm(instance=question)

    context= {
            'question': question,
            'error_message' : " you did not select a choice. ", 
    }

    try:
        selected_answer = question.answer_set.get(pk=request.POST['answer'])
    except (KeyError, Answer.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'mc_and_datasheet/detail.html', context)


    else:
        selected_answer.votes += 1
        selected_answer.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('mc_and_datasheet:results', args=(question.id,)))