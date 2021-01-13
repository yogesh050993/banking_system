from django.db import models


class LookUp(models.Model):
    lu_id = models.BigAutoField(primary_key=True)
    lu_code = models.CharField(max_length=30, unique=True, verbose_name='Code')
    lu_desc = models.CharField(max_length=100, verbose_name='Description')

    lu_cr_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    lu_upd_at = models.DateTimeField(null=True, blank=True, verbose_name='Updated At')
    lu_cr_user = models.ForeignKey("user_master.CustomUser", verbose_name='Created User', on_delete=models.PROTECT)

    class Meta:
        db_table = 'lookup'
        verbose_name = 'Look Up'
        verbose_name_plural = 'Look Up'

    def __str__(self):
        return self.lu_code


class LookUpMapping(models.Model):
    lum_id = models.BigAutoField(primary_key=True)
    lum_head = models.ForeignKey(LookUp, on_delete=models.CASCADE, verbose_name='LookUp Head')
    lum_code = models.CharField(max_length=30, unique=True, verbose_name='Code')
    lum_desc = models.CharField(max_length=100, verbose_name='Description')

    lum_cr_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    lum_upd_at = models.DateTimeField(null=True, blank=True, verbose_name='Updated At')
    lum_cr_user = models.ForeignKey("user_master.CustomUser", verbose_name='Created User', on_delete=models.PROTECT)

    class Meta:
        db_table = 'lookup_mapping'
        verbose_name = 'Look Up Mapping'
        verbose_name_plural = 'Look Up Mapping'

    def __str__(self):
        return self.lum_code




