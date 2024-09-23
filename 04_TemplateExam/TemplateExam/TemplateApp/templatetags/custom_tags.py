from django import template
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

register = template.Library()

@register.filter(name='calcurate_datetime_to_now')
def calcurate_datetime_to_now(value):
    # 2018/01/01、入力された日付をdate型に変換
    join_date = datetime.strptime(value, '%Y/%m/%d').date()
    
    # 現在の日付
    now_date = date.today()
    
    # 差分
    diff = relativedelta(now_date, join_date)
    
    return f'{diff.years}年 {diff.months}ヶ月'
