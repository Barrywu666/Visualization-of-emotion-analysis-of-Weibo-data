"""BigData URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path

from BigApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('page2/', views.demo_ajax),
    path('test/', views.demo_ajax2),
    path('test2/<recordid>/', views.demo_test2),
    path('demo_search/', views.demo_search),
    path('demo_graph/', views.demo_graph),
    path('demo_test/', views.demo_test),
    path('word/', views.word),
    path('searchresults/', views.search),
    re_path(r'^$', views.change),
]
