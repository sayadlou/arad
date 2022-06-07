from django import template

register = template.Library()


@register.filter(is_safe=False)
def str_month_to_persian(value, arg=None):
    month_pairs = (
        ('Farvardin', 'فروردین'),
        ('Ordibehesht', 'اردیبهشت'),
        ('Khordad', 'خرداد'),
        ('Tir', 'تیر'),
        ('Mordad', 'مرداد'),
        ('Shahrivar', 'شهریور'),
        ('Mehr', 'مهر'),
        ('Aban', 'آبان'),
        ('Azar', 'آذر'),
        ('Dey', 'دی'),
        ('Bahman', 'بهمن'),
        ('Esfand', 'اسفند'),
    )
    for month_pair in month_pairs:
        return value.replace(month_pair[0], month_pair[1])
