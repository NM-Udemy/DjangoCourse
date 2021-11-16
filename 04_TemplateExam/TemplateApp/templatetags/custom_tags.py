from django import template
from datetime import datetime
import math

register =template.Library()


@register.filter(name='status_to')
def convert(status, name):
    return 'C'
@register.filter(name='calcurate_datetime_to_now')
def calcurate_datetime_to_now(value):
    join_datetime = datetime.strptime(value, '%Y/%m/%d')
    now_datetime = datetime.now()
    # timedelta class
    diff_datetime = now_datetime - join_datetime
    diff_days = diff_datetime.days
    diff_years = math.floor(diff_days / 365)
    diff_months = math.floor((diff_days - 365 * diff_years) / 30)
    return f'{diff_years}年 {diff_months}カ月'

