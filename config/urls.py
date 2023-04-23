from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

THIRD_PARTY_URLS = [
    path("accounts/", include("allauth.urls")),
    path('__debug__/', include('debug_toolbar.urls')),
]

LOCAL_URLS = [
    path("accounts/", include("apps.accounts.urls")),
    path("products/", include("apps.products.urls")),
    path("message/", include("apps.message.urls")),
    path("", include("apps.customer.urls")),
    path("blog/", include("apps.blog.urls")),
    path("forum/", include("apps.forum.urls")),

    path("vote/", include("apps.vote.urls")),
    path("comment/", include("apps.comment.urls")),
]

urlpatterns = [
    path('admin/', admin.site.urls),

    *THIRD_PARTY_URLS,
    *LOCAL_URLS,


]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

handler404 = 'apps.customer.views.handler404'
handler500 = 'apps.customer.views.handler500'