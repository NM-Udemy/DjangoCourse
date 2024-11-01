from django.db import models
from django.contrib.auth.models import User
import uuid

# パスワード再発行→メールアドレスに再発行のURLが届く→URLをクリックし再発行画面
class PasswordResetToken(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='password_reset_token',
    )
    token = models.UUIDField(default=uuid.uuid4, db_index=True)
    used = models.BooleanField(default=False)