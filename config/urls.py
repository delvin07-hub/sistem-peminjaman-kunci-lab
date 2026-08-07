from django.urls import path, include

urlpatterns = [
    path('', include('apps.authentication.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('master/', include('apps.master_data.urls')),
    path('transaksi/', include('apps.transaction.urls')),
    path('laporan/', include('apps.report.urls')),
    path('api/', include('apps.notifications.urls')),
    path(
        'notifikasi-log/',
        include('apps.notifications.web_urls'),
    ),
]
