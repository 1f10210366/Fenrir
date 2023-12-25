from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import TemplateView



class TopView(TemplateView):
    template_name = "fenrir/seach_input.html"


class SearchResultsView(TemplateView):
    template_name = "fenrir/seach_input.html"