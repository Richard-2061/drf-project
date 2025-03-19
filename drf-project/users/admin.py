# -*- coding: utf-8 -*-
# @Author: Richard
# @File: admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email',)
    ordering = ('-date_joined',)
