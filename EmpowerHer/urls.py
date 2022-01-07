"""EmpowerHer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from EmpowerHerApp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('resume_screening/',resume_screening,name="resume_screening"),
    path('index/',index,name="index"),
    path('',index1,name="index1"),
    path('interview/',interview,name="interview"),
    path('home/',home,name="home"),
    path('opportunity/',opportunity,name="opportunity"),
    path('book_slots/',book_slots,name="book_slots"),
    path('post_opportunity/',post_opportunity,name="post_opportunity"),
    path('join_panel/',join_panel,name="join_panel"),
    # path('support_our_cause/',support_our_cause,name="support_our_cause"),
    path('match_with_jd/',match_with_jd,name="match_with_jd"),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)