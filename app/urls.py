from django.conf.urls.defaults import *


urlpatterns = patterns('expenses.app.views',
    # (r'^expenses/', include('expenses.foo.urls')),
    (r'^expenses/$', 'expenses'),
    (r'^expenses/show/(?P<eid>\d+)/$', 'expense_show'),
    (r'^expenses/add/$', 'expense_add') 
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
