from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


# django.contrib.auth wymaga aby byl folder registration
# mozna od razu podac strone dla http://localhost:8000/account/login/?next=/account/logout
urlpatterns = [
    # post views
    url(r'^sql_execute/(?P<sqlid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<uid>[0-9A-Za-z_\-]+)$', views.sql_execute,name='sql_execute'),
    url(r'^sqlcommand/$', views.create_sqlcommand,name='sqlcommand'),
    url(r'^edit/$', views.edit,name='edit'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    url(r'^register/$', views.register,name='register'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^logout-then-login/$', 'django.contrib.auth.views.logout_then_login', name='logout_then_login'),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^password-change/$','django.contrib.auth.views.password_change',name='password_change'),
    url(r'^password-change/done/$','django.contrib.auth.views.password_change_done',name='password_change'),
    url(r'^password-reset/$','django.contrib.auth.views.password_reset',name='password_reset'),
    url(r'^password-reset/done/$','django.contrib.auth.views.password_reset_done',name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$','django.contrib.auth.views.password_reset_confirm',name='password_reset_confirm'),
    url(r'^password-reset/complete/$','django.contrib.auth.views.password_reset_complete',name='password_reset_complete'),
]


