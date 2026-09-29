from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, DeleteView, DetailView, ListView

from main.models import Receipt


def index(request):
    return render(request, 'main/index.html')

def receipt_create(request):
    return render(request, 'receipt_create.html')

def profile(request):
    return render(request, 'profile.html')

def receipts(request):
    receipts = Receipt.objects.filter(user=request.user).order_by("-purchased_at")
    return render(request, 'receipts.html', {"receipts": receipts} )

def rules(request):
    return render(request, 'rules.html' )
