from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.products.views.product import ProductListView

THIRD_PARTY_URLS = [
    path("accounts/", include("allauth.urls")),
    path('__debug__/', include('debug_toolbar.urls')),
]

LOCAL_URLS = [
    path("accounts/", include("apps.accounts.urls")),
    path("products/", include("apps.products.urls")),
    path("chats/", include("apps.chats.urls")),
    path("orders/", include("apps.orders.urls")),
    
    path("articles/", include("apps.articles.urls")),
    path("forums/", include("apps.forums.urls")),

    path("vote/", include("apps.votes.urls")),
    path("comments/", include("apps.comments.urls")),
]

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('admin/', admin.site.urls),

    *THIRD_PARTY_URLS,
    *LOCAL_URLS,


]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

handler404 = 'apps.orders.views.handler404'
handler500 = 'apps.orders.views.handler500'