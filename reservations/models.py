import datetime
from django.db import models
from django.utils import timezone
from core import models as core_models
from . import managers

class BetweenDay(core_models.TimeStampedModel):

    day = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "BetweenDay"
        verbose_name_plural = "BetweenDays"
    
    def __str__(self):
        return str(self.day)


class Reservation(core_models.TimeStampedModel):

    '''Reservation Model Definition'''

    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELED = 'canceled'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'confirmed'),
        (STATUS_CANCELED, 'canceled'),
    )

    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING)
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey('users.User', on_delete=models.CASCADE)
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE)
    objects = managers.CustomReservationManager()

    def __str__(self):
        return f'{self.room} - {self.check_in}'
    
    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now < self.check_out
    
    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()
        return now >= self.check_out
    
    is_finished.boolean = True

    class Meta:
        db_table = 'reservations'
    

    def save(self, *args, **kwargs):
        if self.pk is None:
            start = self.check_in
            print(start)
            end = self.check_out
            difference = end - start
            existing_BetweenDay = BetweenDay.objects.filter(reservation__room=self.room,
                day__range=(start, end)
            ).exists()
            if not existing_BetweenDay:
                super().save(*args,  **kwargs)
                for i in range(difference.days + 1):
                    day = start + datetime.timedelta(days=i)
                    print(day)
                    BetweenDay.objects.create(day=day, reservation=self)
                return
        return super().save(*args, **kwargs)