from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from banking_system.settings import ADMIN_LOGIN_REDIRECT_URL
from common.models import LookUpMapping
from common.views import send_trx_email_to_user
from customer.models import AccountMaster, TransactionHistory


class CustomerTransaction(LoginRequiredMixin, View):
    def get(self, request):

        if request.user.is_superuser:
            return HttpResponseRedirect(ADMIN_LOGIN_REDIRECT_URL)

        trx_type = LookUpMapping.objects.filter(lum_head__lu_code__iexact='TRX_TYPE').all()

        context = {
            'trx_type': trx_type
        }
        return render(request, 'customer/transaction.html', context)

    def post(self, request):
        form = request.POST
        print(form)
        user_id = request.user.id

        account_no = form.get('account_no')
        amount = float(form.get('amount', 0) or 0.0)
        trx_type_id = form.get('trx_type_id')

        # try:
        account_obj = AccountMaster.objects.get(account_no=account_no, account_holder_id=user_id)
        trx_code = LookUpMapping.objects.filter(pk=trx_type_id).values_list('lum_code', flat=True)
        if trx_code:
            current_bal = float(account_obj.account_bal or 0.0)
            if trx_code[0].upper() == 'CREDIT':
                new_bal = current_bal + amount
                account_obj.account_bal = new_bal
                account_obj.save()

                TransactionHistory.objects.create(trx_account_id=account_obj.pk,
                                                  trx_amount=amount,
                                                  trx_type_id=trx_type_id,
                                                  trx_last_bal=current_bal,
                                                  trx_cur_bal=new_bal)

                subject = 'Transaction alert from Bank'
                message = f'Dear {request.user.first_name} {request.user.last_name} your account is credited with {amount} ' \
                          f'Your current balance is {new_bal} Thank You for banking with us'
                send_trx_email_to_user(request, subject, message)

            elif trx_code[0].upper() == 'DEBIT':
                print('deebit')
                if current_bal < amount or current_bal == 0.0:
                    context = {
                        'type': 1,
                        'is_success': False,
                        'msg': 'Insufficient balance'
                    }
                    return JsonResponse(context)

                new_bal = current_bal - amount
                account_obj.account_bal = new_bal
                account_obj.save()

                TransactionHistory.objects.create(trx_account_id=account_obj.pk,
                                                  trx_amount=amount,
                                                  trx_type_id=trx_type_id,
                                                  trx_last_bal=current_bal,
                                                  trx_cur_bal=new_bal)

                subject = 'Transaction alert from Bank'
                message = f'Dear {request.user.first_name} {request.user.last_name} your account has been debited by {amount} ' \
                          f'Your current balance is {new_bal} Thank You for banking with us'
                send_trx_email_to_user(request, subject, message)

            else:
                context = {
                    'type': 2,
                    'is_success': False,
                    'msg': 'Something unexpected happen please try after sometime'
                }
                return JsonResponse(context)

            context = {
                    'is_success': True,
                    'msg': 'Transaction successful'
                }
            return JsonResponse(context)

        context = {
            'type': 1,
            'is_success': False,
            'msg': 'Something unexpected happen please try after sometime'
        }
        return JsonResponse(context)

        # except Exception as e:
        #     print(e)
        #     context = {
        #         'is_success': False,
        #         'msg': 'Something unexpected happen please try after sometime'
        #     }
        #     return JsonResponse(context)


class CheckBalance(LoginRequiredMixin, View):
    def get(self, request):

        accounts = AccountMaster.objects.filter(account_holder_id=request.user.id).all()

        context = {
            'accounts': accounts
        }
        return render(request, 'customer/check_balance.html', context)

    def post(self, request):
        form = request.POST
        print(form)
        account_no = form.get('account_no')

        try:
            is_success = True
            account_bal = AccountMaster.objects.get(account_no=account_no)
            account_bal = account_bal.account_bal
        except:
            account_bal = 0
            is_success = True

        context = {
            'is_success': is_success,
            'account_bal': account_bal
        }
        return JsonResponse(context)












