from django import forms
from cart.models import Order

class OrderForm(forms.ModelForm):
    payment_choice=[('Online','Online'),('COD','COD')]
    payment_method = forms.ChoiceField(choices=payment_choice,widget=forms.RadioSelect,required=True)
    class Meta:
        model=Order
        fields=['address','phone','payment_method']
        