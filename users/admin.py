from django.contrib import admin
from django.contrib.auth.models import Group
from .models import UserAccount


admin.site.register(UserAccount)

# not using groups
admin.site.unregister(Group)