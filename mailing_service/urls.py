from django.urls import path
from .views import ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, \
    MailingListListView, MailingListCreateView, MailingListUpdateView, MailingListDeleteView, MailingListDetailView, LogListView

urlpatterns = [
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:client_id>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:client_id>/delete/', ClientDeleteView.as_view(), name='client_delete'),

    path('mailing-lists/', MailingListListView.as_view(), name='mailing_list_list'),
    path('mailing-lists/create/', MailingListCreateView.as_view(), name='mailing_list_create'),
    path('mailing-lists/<int:mailing_list_id>/', MailingListUpdateView.as_view(), name='mailing_list_detail'),
    path('mailing-lists/<int:mailing_list_id>/update/', MailingListUpdateView.as_view(), name='mailing_list_update'),
    path('mailing-lists/<int:mailing_list_id>/delete/', MailingListDeleteView.as_view(), name='mailing_list_delete'),
    path('mailing-lists/<int:mailing_list_id>/', MailingListDetailView.as_view(), name='mailing_list_detail'),

    path('', MailingListListView.as_view(), name='home'),
    path('logs/', LogListView.as_view(), name='log_list'),
    path('logs/<int:mailing_list_id>/', LogListView.as_view(), name='log_list_detail'),
]