from django.contrib import admin
from accounts.models import PasswordReset, User

admin.site.register(User)
admin.site.register(PasswordReset)