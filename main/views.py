from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from datetime import datetime
from main.models import Receipt
from django.conf import settings
from main.forms import ReceiptForm


def index(request):
    promo_start = settings.PROMO_START
    promo_end = settings.PROMO_END
    if isinstance(promo_start, str):
        promo_start = datetime.strptime(promo_start, "%Y-%m-%d").date()
    if isinstance(promo_end, str):
        promo_end = datetime.strptime(promo_end, "%Y-%m-%d").date()

    return render(request, "main/index.html", {
        "promo_start": promo_start,
        "promo_end": promo_end,
    })

@login_required
def receipt_create(request):
    if request.method == 'POST':
        form = ReceiptForm(request.POST)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.user = request.user
            receipt.status = Receipt.Status.ON_REVIEW
            receipt.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Чек успешно загружен и отправлен на проверку!'
                })
            return redirect('main:receipts')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
    else:
        form = ReceiptForm()

    return render(request, 'main/receipt_create.html', {'form': form})

def profile(request):
    return render(request, 'profile.html')


@login_required
def receipts(request):
    receipts_list = Receipt.objects.filter(user=request.user).order_by("-purchased_at")

    paginator = Paginator(receipts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/receipts.html', {
        "receipts": page_obj,
        "total_count": receipts_list.count()
    })

def rules(request):
    return render(request, 'rules.html' )

@login_required
def api_receipts(request):
    receipts = Receipt.objects.filter(user=request.user).values(
        'id', 'fn', 'fd', 'fp', 'purchased_at', 'amount', 'status', 'reject_reason', 'created_at'
    )
    return JsonResponse(list(receipts), safe=False)