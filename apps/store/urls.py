from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('cart/', CartListAddView.as_view(), name='cart'),
    path('cart/<int:pk>/', CartPutDeleteView.as_view(), name='cart_item'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('order/<uuid:pk>/', OrderDetailView.as_view(), name='order_item'),
    path('payment/', PaymentListAddView.as_view(), name='payments'),
    path('confirm/', CallbackGatewayView.as_view(), name='callback-gateway'),

    path('service/', ServiceIndexView.as_view(), name='service_home'),
    path('service/<str:slug>/', ServiceSlugView.as_view(), name='service_slug'),
    path('service/category/<str:category>/', ServiceCategoryView.as_view(), name='service_category'),

    path('learning/', LearningIndexView.as_view(), name='learning_home'),
    path('learning/post/<str:slug>/', LearningSlugView.as_view(), name='learning_slug'),
    path('learning/category/<str:category>/', LearningCategoryView.as_view(), name='learning_category'),
    path('learning/attachment/<str:slug>/', LearningAttachmentView.as_view(), name='learning_attachment'),

    path('event/', EventIndexView.as_view(), name='event_home'),
    path('event/<str:slug>/', EventSlugView.as_view(), name='event_slug'),
    path('event/category/<str:category>/', EventCategoryView.as_view(), name='event_category'),

]
