import uuid
from datetime import datetime

import pytz
import xlwt as xlwt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.generic import View

from banking_system import settings
from banking_system.settings import TIME_ZONE
from customer.models import AccountMaster, TransactionHistory
from user_master.models import CustomUser


def get_unique_username():
    """
    Recursive function to return the unique username by validating from CustomUser model

    """
    username = f'{generate_random_int_number()}'
    is_exists = CustomUser.objects.filter(username__iexact=username).exists()
    if not is_exists:
        return username

    return get_unique_username()


def generate_random_int_number():
    """
    Function to generate random integer numbers of 11 digits and return that value in str format

    """
    return str(uuid.uuid1().int)[:10]


def convert_datetime_as_timezone(time_zone, datetime_obj, dateformat):
    """
    Function to convert datetime object into given timezone
    :param time_zone: it must be in "Asia/Kolkata, Asia/Riyadh, America/Denver etc" these formats only
    :param datetime_obj: it must be the datetime objects of utc timezone
    :param dateformat: it must be the string representation of datetime format the output will be in that format only
    :return: it will return datetime in string in the given format after converting into given timezone

    """
    from pytz import timezone as pytimezone
    try:
        timezone_date = datetime_obj.astimezone(pytimezone(time_zone))
        str_datetime = timezone_date.strftime(dateformat)

    except Exception as e:
        print(e, 'printing exception in func==>convert_datetime_as_timezone app==>common --------> 1')
        str_datetime = ''

    return str_datetime


def check_email(request):
    form = request.GET
    email = form.get('email')
    is_exists = CustomUser.objects.filter(email__iexact=email).exists()

    return JsonResponse({'is_exists': is_exists})


def send_trx_email_to_user(request, subject, message):
    recipient_email = request.user.email
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [recipient_email, ]
    is_mail_send = send_mail(subject, message, email_from, recipient_list)
    return is_mail_send


class AdminHome(LoginRequiredMixin, View):
    def get(self, request):
        accounts = AccountMaster.objects.all()
        context = {
            'accounts': accounts
        }
        return render(request, 'common/admin_home.html', context)

    def post(self, request):
        form = request.POST

        print(form)

        accounts = form.getlist('account_no')
        from_date = form.get('from_date')
        from_time = form.get('from_time')
        to_date = form.get('to_date')
        to_time = form.get('to_time')

        filters = Q(trx_account_id__in=accounts)

        if from_time:
            utc_dt = get_utc_dt_time(from_date, from_time)
            filters = filters & Q(trx_dt_time__gte=utc_dt)

        elif from_date:
            if from_date:
                filters = filters & Q(trx_dt_time__date__gte=from_date)

        if to_time:
            utc_dt = get_utc_dt_time(from_date, from_time)
            filters = filters & Q(trx_dt_time__lte=utc_dt)

        elif to_date:
            filters = filters & Q(trx_dt_time__date__lte=to_date)

        print(filters)
        print('------------------------------------------------------------------------------')
        trx_his = TransactionHistory.objects.filter(filters).order_by('-pk')
        global trx_list
        trx_list = []
        sr_no = 1
        for trx in trx_his:
            trx_dict = {
                'sr_no': sr_no,
                'acc_no': trx.trx_account.account_no,
                'fullname': trx.trx_account.fullname,
                'trx_type': trx.trx_type.lum_desc,
                'trx_amount': float(trx.trx_amount),
                'trx_last_bal': float(trx.trx_last_bal),
                'trx_cur_bal': float(trx.trx_cur_bal),
                'trx_on': convert_datetime_as_timezone(TIME_ZONE, trx.trx_dt_time, '%b %d, %Y %I:%M %p'),
            }
            sr_no += 1
            trx_list.append(trx_dict)

        print(trx_list)

        return JsonResponse({'is_success': True})


def render_to_excel_report(request):
    """
    common function to print data into excel
    :param request:
    :return:
    """
    item_List = trx_list
    filename, sheet_name = 'File.xls', 'Sheet'
    columns = ['Sr No', 'Account Number', 'Fullname', 'Transaction Type', 'Trx Amount', 'Last Balance',
               'Current Balance', 'Date']

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(sheet_name)
    ws.set_show_grid(0)  # hide grid from the excel sheet

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    font_style.font.name = 'Lato'
    font_style.font.height = 20 * 9

    font_style = xlwt.XFStyle()
    font_style.font.name = 'Lato'
    font_style.font.height = 20 * 9

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    font_style.font.name = 'Lato'
    font_style.font.height = 20 * 9

    for col_num in range(len(columns)):
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.MEDIUM
        borders.right = xlwt.Borders.MEDIUM
        borders.top = xlwt.Borders.MEDIUM
        borders.bottom = xlwt.Borders.MEDIUM
        borders.left_colour = 0x80
        borders.right_colour = 0x80
        borders.top_colour = 0x80
        borders.bottom_colour = 0x80
        font_style.borders = borders
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['silver_ega']
        font_style.pattern = pattern
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    font_style.font.name = 'Lato'
    font_style.font.height = 20 * 9

    rows = item_List

    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN
    borders.left_colour = 0x00
    borders.right_colour = 0x00
    borders.top_colour = 0x00
    borders.bottom_colour = 0x00
    font_style.borders = borders

    for row in rows:
        new_row = list(row.values())
        row_num += 1
        for col_num in range(len(new_row)):
            ws.write(row_num, col_num, new_row[col_num], font_style)

    wb.save(response)
    return response


def get_utc_dt_time(date_str, time_str):
    """
    Function to change datetime string into date time object & convert from local
    timezone to utc timezone for fetching tha data from db
    :param date_str:
    :param time_str:

    """
    local = pytz.timezone(TIME_ZONE)
    naive = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)

    return utc_dt























