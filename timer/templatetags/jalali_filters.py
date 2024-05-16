from django import template
import jdatetime

register = template.Library()

@register.filter
def to_jalali(value, date_format='%Y/%m/%d'):
    if not value:
        return ''

    if isinstance(value, jdatetime.datetime) or isinstance(value, jdatetime.date):
        return value.strftime(date_format)
    try:
        jalali_date = jdatetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return jalali_date.strftime(date_format)
    except ValueError:
        return value

