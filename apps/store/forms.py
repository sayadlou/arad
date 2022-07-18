from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from .models import CartItem


class CartItemEditForm(forms.ModelForm):
    request_type = forms.CharField(max_length=3, required=True)

    class Meta:
        model = CartItem
        fields = ['cart', 'quantity', 'product', 'request_type']

    def clean(self):
        cleaned_post_data = super().clean()
        product = cleaned_post_data['product']
        if not cleaned_post_data["request_type"] in ("dec", "inc", 'del'):
            raise ValidationError(_("requested type is not valid"))
        try:
            data = CartItem.objects.get(product=product)
            if cleaned_post_data["request_type"] == "inc":
                if data.quantity + cleaned_post_data['quantity'] > product.max_order_quantity:
                    raise ValidationError(_("quantity is more than allowed value"))
            if cleaned_post_data["request_type"] == "dec":
                if data.quantity - cleaned_post_data['quantity'] < product.min_order_quantity:
                    raise ValidationError(_("quantity is less than allowed value"))

        except CartItem.DoesNotExist:
            raise ValidationError(_("product not found"))

    def save_or_update(self):
        cart_item = CartItem.objects.get(product=self.cleaned_data['product'])
        if self.cleaned_data["request_type"] == "inc":
            cart_item.quantity += self.cleaned_data['quantity']
            cart_item.save()

        if self.cleaned_data["request_type"] == "dec":
            cart_item.quantity -= self.cleaned_data['quantity']
            cart_item.save()

        if self.cleaned_data["request_type"] == "del":
            cart_item.delete()


class CartItemAddForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ('cart', 'quantity', 'product',)
