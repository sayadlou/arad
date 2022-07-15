from captcha.fields import CaptchaTextInput


class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = 'account/custom_field.html'


class AdminCaptchaTextInput(CaptchaTextInput):
    template_name = 'account/admin_custom_field.html'
