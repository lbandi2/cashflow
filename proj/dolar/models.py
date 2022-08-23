from django.db import models
from datetime import datetime, timedelta

class Cotizacion(models.Model):
    datetime = models.DateTimeField()
    currency = models.CharField(max_length=50, blank=False, null=False)
    name = models.CharField(max_length=50, blank=False, null=False)
    buy = models.FloatField()
    sell = models.FloatField()
    other = models.FloatField()

    def __str__(self):
        return f"{self.currency.upper()} {self.name.upper()} {datetime.strftime(self.datetime, '%Y-%m-%d %H:%M:%S')}"

    def date_month(self):
        return datetime.strftime("%m-%d", self.datetime)

    def prev_entry(self, days_back=1):
        result = None
        given_date = self.datetime.date() - timedelta(days=days_back)
        cotiz = Cotizacion.objects.order_by('-datetime').filter(currency=self.currency).filter(name=self.name).filter(datetime__date__lt = given_date)[:1]
        if len(cotiz) > 0:
            result = cotiz[0]
            return result
        return None

    def time_relative(self):
        days = (datetime.now().date() - self.datetime.date()).days
        hours = (datetime.now().hour - self.datetime.hour)
        minutes = (datetime.now().minute - self.datetime.minute)
        if days == 0:
            # difference = 'Hoy'
            if hours == 1:
                difference = f'Hace 1 h'
            elif hours > 1:
                difference = f'Hace {hours} hs'
            else:
                difference = f'Hace {minutes} min'
        elif days == 1:
            difference = 'Ayer'
        elif days > 1:
            difference = f'Hace {days} días'
        return difference

    def last_variation(self):
        # values = Cotizacion.objects.order_by('-datetime').filter(name=self.name)[:2]
        # values = Cotizacion.objects.order_by('-datetime').filter(name=self.name).filter(datetime__lt=self.datetime)[:1]
        if self.prev_entry() is not None:
            result = ((self.sell - self.prev_entry().sell) / self.sell) * 100 #TODO: Needs fixing
            formatted_result = "{0:.2f}".format(result)
            return f'{formatted_result} %'
        return '0 %'
