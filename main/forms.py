# main/forms.py
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import Receipt


class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ["fn", "fd", "fp", "purchased_at", "amount"]
        widgets = {
            "purchased_at": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "fn": forms.TextInput(attrs={"placeholder": "Введите ФН", "class": "form-control"}),
            "fd": forms.TextInput(attrs={"placeholder": "Введите номер чека (ФД)", "class": "form-control"}),
            "fp": forms.TextInput(attrs={"placeholder": "Введите ФП", "class": "form-control"}),
            "amount": forms.NumberInput(attrs={"placeholder": "0.00 ₽", "class": "form-control", "step": "0.01"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["purchased_at"].input_formats = ["%Y-%m-%dT%H:%M"]

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount is not None and amount < 1000:
            raise ValidationError("Минимальная стоимость чека должна составлять 1 000 ₽.")
        return amount

    def clean_purchased_at(self):
        purchased_at = self.cleaned_data.get("purchased_at")
        if not purchased_at:
            return purchased_at

        promo_start = settings.PROMO_START
        promo_end = settings.PROMO_END
        if isinstance(promo_start, str):
            promo_start = datetime.strptime(promo_start, "%Y-%m-%d").date()
        if isinstance(promo_end, str):
            promo_end = datetime.strptime(promo_end, "%Y-%m-%d").date()

        if purchased_at.date() < promo_start or purchased_at.date() > promo_end:
            raise ValidationError(
                f"Дата покупки должна входить в период акции: "
                f"{promo_start.strftime('%d.%m.%Y')} — {promo_end.strftime('%d.%m.%Y')}"
            )
        return purchased_at

    def clean(self):
        cleaned_data = super().clean()
        fn = cleaned_data.get("fn")
        fd = cleaned_data.get("fd")
        fp = cleaned_data.get("fp")

        if fn and fd and fp:
            if Receipt.objects.filter(fn=fn, fd=fd, fp=fp).exists():
                raise ValidationError(
                    "Чек с такими реквизитами (ФН+ФД+ФП) уже был зарегистрирован."
                )
        return cleaned_data