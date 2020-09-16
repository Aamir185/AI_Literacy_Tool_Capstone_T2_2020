"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from AI_Literacy_App import views
from django.conf.urls.static import static
from core import settings
from django.conf.urls import include, url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('examples/', views.examples),
    path('examples/age_gender/', views.age_gender),
    path('examples/age_gender/image_upload/', views.image_upload_view),
    path('examples/age_gender/run_module/', views.run_module),
    path('examples/sentiment_analysis/', views.sentiment_analysis),
    path('examples/sentiment_analysis/run_sentiment/', views.run_sentiment),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)