from django.db import models

from user_master.models import CustomUser


class AccountMaster(models.Model):
    account_no = models.CharField(max_length=15, unique=True, verbose_name='Account Number')
    fullname = models.CharField(max_length=150, verbose_name='Full Name')
    account_bal = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name='Account Balance')

    upd_date = models.DateTimeField(verbose_name='Updated Date')
    account_holder = models.OneToOneField(CustomUser, on_delete=models.PROTECT, related_name='customer', verbose_name='Account Holder')

    class Meta:
        db_table = 'account_master'
        verbose_name = 'Account Master'
        verbose_name_plural = 'Account Master'

    def __str__(self):
        return self.account_no


class TransactionHistory(models.Model):
    trx_account = models.ForeignKey(AccountMaster, on_delete=models.PROTECT, verbose_name='Account Number')
    trx_amount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Transaction Amount')
    trx_type = models.ForeignKey("common.LookUpMapping", on_delete=models.PROTECT, verbose_name='Transaction Type')
    trx_dt_time = models.DateTimeField(auto_now_add=True, verbose_name='Transact At')
    trx_last_bal = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Last Balance')
    trx_cur_bal = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Current Balance')

    class Meta:
        db_table = 'transaction_history'
        verbose_name = 'Transaction History'
        verbose_name_plural = 'Transaction History'

    def __str__(self):
        return str(self.trx_amount)

