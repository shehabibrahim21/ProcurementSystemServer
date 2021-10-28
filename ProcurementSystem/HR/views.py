from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question
from HR.forms import SearchForm
from HR.models import RetrieveData
import InputCleaning as  ic
import GetCategoryCode as gcc
import RetrieveSpecifications as  rs
import GetDetails as gd

def index(request):
    form = SearchForm(request.POST)
    print(RetrieveData.list)
    specifications = rs.get_specifics()
    if form.is_valid():
        raw_data = form.cleaned_data['name']

        clean_data= ic.lookup(raw_data)
        clean_data = ' '.join(clean_data)

        tup = gd.get_details(clean_data,RetrieveData.list )
        try:
            context = {
                "raw_data":raw_data,
                "clean_data":clean_data,
                "lst_items": RetrieveData.list,
                "form": form,
                 "specifications": specifications,
                'successful_submit': True,
                'tup': tup,
                'itc' : tup[0],
                 'gnrc': tup[1],
                 'unt': tup[2],
                 'prc' : tup[3],
                  'acc':tup[4]

            }
        except:
            context = {
                "raw_data": raw_data,
                "clean_data": clean_data,
                "lst_items": RetrieveData.list,
                "form": form,
                "specifications": specifications,
                'successful_submit': True,
                'tup': tup,

            }

        return render(request, 'HR/index.html', context)

    else:
        form = SearchForm()
        context = {
            "lst_items": RetrieveData.list,
            "form": form,
            "specifications": specifications,
            'successful_submit': False
        }

        return render(request, 'HR/index.html', context)


class IndexView(generic.ListView):
    template_name = 'HR/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'HR/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'HR/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'HR/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('HR:results', args=(question.id,)))



def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def get_queryset(self):
    """
    Return the last five published questions (not including those set to be
    published in the future).
    """
    return Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]