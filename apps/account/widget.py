from captcha.fields import CaptchaTextInput


class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = 'account/custom_field.html'
