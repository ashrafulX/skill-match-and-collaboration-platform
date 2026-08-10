# from django.contrib import admin
# from django.urls import path, include
# from . import views

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('filter-jobs', views.filter_jobs, name='filter_jobs'),
#     path('find-job', views.find_job, name='find_job'),
#     path('', views.home, name='homepage'),
#     path('aboutUs/', views.about, name='aboutpage'),
#     path('', include('loginpage.urls')),
#     path('', include('jobPost.urls')),
#     path('', include('Categories.urls')),
# ]

# # Static files (if required)
# from django.conf import settings
# from django.conf.urls.static import static
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# if settings.DEBUG:
#     urlpatterns += static(
#         settings.MEDIA_URL,
#         document_root=settings.MEDIA_ROOT
#     )

#     urlpatterns = [
#         *urlpatterns,
#     ] + debug_toolbar_urls()
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('filter-jobs', views.filter_jobs, name='filter_jobs'),
    path('find-job', views.find_job, name='find_job'),
    path('', views.home, name='homepage'),
    path('aboutUs/', views.about, name='aboutpage'),
    path('', include('loginpage.urls')),
    path('', include('jobPost.urls')),
    path('', include('Categories.urls')),
]


if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )