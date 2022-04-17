from datetime import timedelta, datetime
from decimal import Decimal
from pprint import pprint
from time import mktime

import os
import requests
import json
from uuid import uuid4
import logging

from azbankgateways import bankfactories
from azbankgateways.exceptions import AZBankGatewaysException
from azbankgateways import models as bank_models, default_settings as settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.utils.translation import gettext as _
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django_downloadview.views.object import ObjectDownloadView

from utils.functions import cart_to_order
from .forms import CartItemForm
from .models import *
from config.settings.base import MINIMUM_ORDER_AMOUNT
from .permitions import LearningBoughtUserMixin

logger = logging.getLogger('store.views')


class CartListAddView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = {'cart': request.user.cart}
        cart_has_item = CartItem.objects.filter(cart=request.user.cart).exists()
        context['cart_has_item'] = cart_has_item
        if cart_has_item:
            context['cart_item'] = CartItem.objects.filter(cart=request.user.cart).order_by('id')
            cart_sum = 0
            for item in context['cart_item']:
                cart_sum += item.product.price * Decimal(item.quantity)
            context['cart_sum'] = cart_sum
        return render(request=self.request, template_name="store/cart.html", context=context)

    def post(self, request, *args, **kwargs):
        post_copy = request.POST.copy()
        post_copy['cart'] = self.request.user.cart
        form = CartItemForm(data=post_copy)
        if form.is_valid():
            messages.success(request, _('product added to cart'))
            form.save_or_update()
        else:
            for key in form.errors:
                for error in form.errors[key]:
                    messages.error(request, error)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class CartPutDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, pk=kwargs['pk'])
        post_copy = request.POST.copy()
        post_copy['cart'] = self.request.user.cart
        form = CartItemForm(data=post_copy, instance=cart_item)
        if form.is_valid():
            messages.success(request, _('product updated'))
            form.save_or_update()
        else:
            for key in form.errors:
                for error in form.errors[key]:
                    messages.error(request, error)
        return redirect(reverse('store:cart'), permanent=True)

    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(CartItem, pk=kwargs['pk'])
        if request.user.cart.pk == obj.cart.pk:
            obj.delete()
            return HttpResponse("deleted")
        else:
            return HttpResponse(status=404)


class OrderListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(owner=request.user)
        context = {'orders': orders, 'has_order': orders.exists()}
        return render(request=self.request, template_name="store/orders.html", context=context)


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, owner=request.user, pk=kwargs["pk"])
        context = {'order': order}
        return render(request=request, template_name="store/order.html", context=context)


class PaymentListAddView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        payments = Payment.objects.filter(owner=request.user)
        context = {'payments': payments, 'has_payments': payments.exists()}
        return render(request=self.request, template_name="store/payments.html", context=context)

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            order_id = request.POST.get('order_id')
            try:
                order = Order.objects.get(owner=request.user, pk=order_id)
            except Order.DoesNotExist:
                order = cart_to_order(request)
            if order.total_price <= MINIMUM_ORDER_AMOUNT:
                messages.success(request, _('minimum order amount should be more than 100,000 IRR'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            request.user.cart.cartitem_set.all().delete()
            factory = bankfactories.BankFactory()
            try:
                bank = factory.auto_create(bank_models.BankType.ZARINPAL)
                bank.set_request(request)
                bank.set_amount(int(order.total_price))
                bank.set_client_callback_url(reverse_lazy('store:callback-gateway'))
                bank.set_mobile_number(order.owner.mobile)
                bank_record = bank.ready()
                Payment.objects.create(
                    owner=request.user,
                    order=order,
                    amount=(int(order.total_price)),
                    transaction=bank_record,
                )
                return bank.redirect_gateway()
            except AZBankGatewaysException as e:
                logging.critical(e)
                # TODO: redirect to failed page.
                raise e


class CallbackGatewayView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
        if not tracking_code:
            logging.error("tracking code is not in url query param.")
            raise Http404
        try:
            bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
        except bank_models.Bank.DoesNotExist:
            logging.error("bank record is not valid")
            raise Http404
        if bank_record.is_success:
            try:
                payment = Payment.objects.get(content_type=ContentType.objects.get_for_model(bank_record),
                                              object_id=bank_record.pk)
                payment.status = Payment.STATUS_CONFIRMED
                payment.save()
                payment.order.status = Order.ORDER_STATUS_PAYED
                payment.order.save()
                paid_order_items = payment.order.orderitem_set.all()
                bayer = payment.owner
                for item in paid_order_items:
                    item.product.add_buyer(bayer)
                return HttpResponse("پرداخت با موفقیت انجام شد.")
            except Payment.DoesNotExist:
                logging.error(f"payment for {bank_record.pk} was successful but has no oder")
                return HttpResponse("خطایی در پرداخت رخ داده است جهت بازپرداخت وجه با پشتیبانی تماس حاصل نمایید.")
        logging.error(f"payment {bank_record.pk} with amount {bank_record.amount} was not successful")
        return HttpResponse(
            "پرداخت با شکست مواجه شده است.اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")


class ServiceIndexView(ListView):
    model = Service
    template_name = 'service/index.html'
    paginate_by = 6

    # all_posts = Post.objects.order_by('pub_date').filter(status='Published')

    def get_queryset(self):
        return self.model.objects.order_by('pub_date').filter(status='Published')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['model'] = ContentType.objects.get_for_model(Service).pk
        data['formmy'] = CartItemForm()

        return data


class ServiceSlugView(DetailView):
    template_name = 'service/slug.html'
    model = Service

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        event = self.object
        user_id = self.request.user.pk
        data['owner'] = event.purchaser.filter(pk=user_id).exists()
        return data


class ServiceCategoryView(ListView):
    model = Service
    template_name = 'service/category.html'
    paginate_by = 6

    def get_queryset(self):
        category = self.kwargs['category']
        return self.model.objects.order_by('pub_date').filter(category__name__iexact=category)


class LearningIndexView(ListView):
    model = LearningPost
    template_name = 'learning/index.html'
    paginate_by = 6

    # all_posts = Post.objects.order_by('pub_date').filter(status='Published')

    def get_queryset(self):
        return self.model.objects.order_by('pub_date').filter(status='Published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = LearningCategory.objects.all()
        context['tags'] = LearningPost.blog_tags_list()
        return context


class LearningSlugView(DetailView):
    template_name = 'learning/slug.html'
    model = LearningPost

    def get_context_data(self, **kwargs):
        validity_link_time = datetime.now() + timedelta(hours=10)
        validity_link_time_unix = int(mktime(validity_link_time.timetuple()))
        url = f"https://napi.arvancloud.com/vod/2.0/videos/{self.object.video.arvan_id}"
        headers = {'Authorization': os.environ.get('ARVAN_API_KEY')}
        payload = {'secure_expire_time': validity_link_time_unix, 'secure_ip': '1.1.1.1'}
        # if os.environ.get('DJANGO_SETTINGS_MODULE') == 'config.settings.production':
        payload['secure_ip'] = self.get_client_ip()
        r = requests.get(url, headers=headers, params=payload)
        logging.info(self.get_client_ip())
        logging.info(r.json()["data"])
        data = super().get_context_data(**kwargs)
        if r.status_code == 200:
            respone = r.json()
            data['video_url'] = respone["data"]["player_url"]
            data['status'] = True
        else:
            data['status'] = False
        return data

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


class LearningTagView(ListView):
    model = LearningPost
    template_name = 'learning/tag.html'
    paginate_by = 6

    def get_queryset(self):
        tag = self.request.GET.get("tag", "")
        tag = tag.lower()
        return self.model.objects.order_by('pub_date').filter(status='Published').filter(tags__contains=tag)


class LearningCategoryView(ListView):
    model = LearningPost
    template_name = 'learning/category.html'
    paginate_by = 6

    def get_queryset(self):
        category = self.kwargs['category']
        return self.model.objects.order_by('pub_date').filter(category__name__iexact=category)


class LearningAttachmentView(LearningBoughtUserMixin, ObjectDownloadView):
    model = LearningPost
    file_field = "attachment"


@staff_member_required
def refresh(request):
    url = f"https://napi.arvancloud.com/vod/2.0/channels/{os.environ.get('ARVAN_CHANNEL_ID')}/videos"
    headers = {'Authorization': os.environ.get('ARVAN_API_KEY')}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        respone = r.json()
        ids = VideoFile.objects.values_list('arvan_id')
        list(ids)
        id_list = [i[0] for i in ids]
        video_file = []
        for video in respone['data']:
            if video['id'] not in id_list:
                video_file.append(VideoFile(arvan_id=video['id'], name=video['title']))
        VideoFile.objects.bulk_create(video_file)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


class EventIndexView(ListView):
    model = Event
    template_name = 'event/index.html'
    paginate_by = 6

    # all_posts = Post.objects.order_by('pub_date').filter(status='Published')

    def get_queryset(self):
        return self.model.objects.order_by('pub_date').filter(status='Published')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['model'] = ContentType.objects.get_for_model(Event).pk
        data['formmy'] = CartItemForm()

        return data


class EventSlugView(DetailView):
    template_name = 'event/slug.html'
    model = Event

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        event = self.object
        user_id = self.request.user.pk
        data['owner'] = event.purchaser.filter(pk=user_id).exists()
        return data


class EventCategoryView(ListView):
    model = Event
    template_name = 'learning/category.html'
    paginate_by = 6

    def get_queryset(self):
        category = self.kwargs['category']
        return self.model.objects.order_by('pub_date').filter(category__name__iexact=category)
