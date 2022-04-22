from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from .models import CartItem


class CartItemForm(forms.ModelForm):
    request_type = forms.CharField(max_length=3, required=True)

    class Meta:
        model = CartItem
        fields = ['cart', 'quantity', 'product', 'request_type']

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data['product']
        if not cleaned_data["request_type"] in ("dec", "inc"):
            raise ValidationError(_("requested type is not valid"))
        try:
            data = CartItem.objects.get(product=product)
            if cleaned_data["request_type"] == "inc":
                if data.quantity + cleaned_data['quantity'] > product.max_order_quantity:
                    raise ValidationError(_("quantity is more than allowed value"))
            if cleaned_data["request_type"] == "dec":
                if data.quantity - cleaned_data['quantity'] < product.min_order_quantity:
                    raise ValidationError(_("quantity is less than allowed value"))

        except CartItem.DoesNotExist:
            raise ValidationError(_("product not found"))

    def save_or_update(self):
        try:
            data = CartItem.objects.get(product=self.cleaned_data['product'])

            if self.cleaned_data["request_type"] == "inc":
                data.quantity += self.cleaned_data['quantity']

            if self.cleaned_data["request_type"] == "dec":
                data.quantity -= self.cleaned_data['quantity']
            data.save()
        except CartItem.DoesNotExist:
            self.save()
