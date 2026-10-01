from django.conf import settings
from django.db import models

class Receipt(models.Model):
    class Status(models.TextChoices):
        ON_REVIEW = "on_review", "На проверке"
        ACCEPTED = "accepted", "Принят"
        REJECTED = "rejected", "Отклонён"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "receipts",
        verbose_name = "Пользователь",
    )
    fn = models.CharField("ФН", max_length=20)
    fd = models.CharField("ФД", max_length=20)
    fp = models.CharField("ФП", max_length=20)
    purchased_at = models.DateTimeField("Дата и время покупки")
    amount = models.DecimalField("Сумма", max_digits=10, decimal_places=2)
    status = models.CharField(
        'Статус',
        max_length = 20,
        choices = Status.choices,
        default = Status.ON_REVIEW,
    )

    reject_reason = models.TextField("Причина отказа", blank=True)
    created_at = models.DateTimeField("Дата регистрации", auto_now_add=True)

    class Meta:
        verbose_name = "Чек"
        verbose_name_plural = "Чеки"
        ordering = ["-purchased_at"]
        constraints = [
            models.UniqueConstraint(
                fields=['fn', 'fd', 'fp'],
                name="unique_receipt_fn_fd_fp",
            )
        ]

    def __str__(self):
        return f"Чек {self.fn}-{self.fd}-{self.fp} ({self.get_status_display()})"

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    def __str__(self):
        return f"Профиль {self.user.username}"