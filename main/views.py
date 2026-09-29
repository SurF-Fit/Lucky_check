from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, DeleteView, DetailView, ListView

def index(request):
    return render(request, 'main/index.html')

def receipt_create(request):
    return render(request, 'receipt_create.html')

def profile(request):
    return render(request, 'profile.html')

def receipts(request):
    return render(request, 'receipts.html' )

def rules(request):
    return render(request, 'rules.html' )
