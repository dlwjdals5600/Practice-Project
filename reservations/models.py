from django.db import models
from core import models as core_models

class Reservation(core_models.TimeStampedModel):

    '''Reservation Model Definition'''

    status = models.CharField(
        max_length=12)
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey('users.User', on_delete=models.CASCADE)
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE)

    class Meta:
        db_table = 'reservations'