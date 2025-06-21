#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# Time    : 2025/6/15 13:25
# File    : urls.py
# Software: PyCharm

from django.contrib import admin
from django.urls import path
from learning_log_app import views

app_name = 'learning_log_app'

urlpatterns = [
    # 测试
    path('base', views.base, name='base'),

    # 主页
    path('index/', views.index, name='index'),

    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),


    # 显示所有的主题
    path('topis', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('edit_topic/<int:topic_id>/', views.edit_topic, name='edit_topic'),


    # 用于添加新主题的网页
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # 用于编辑条目的页面
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),


    #管理主页
    path('manage_topics/', views.manage_topics, name='manage_topics'),  # 主题管理
    path('manage_user/', views.manage_user, name='manage_user'),  # 用户管理
    path('manage_notes/', views.manage_notes, name='manage_notes'),  # 用户管理

]

