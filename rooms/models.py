from django.db import models
from django_countries.fields import CountryField
from core import models as core_models


class AbstractItem(core_models.TimeStampedModel):

    ''' Abstract Item '''

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    '''RoomType Object Definition '''

    class Meta:
        db_table = 'room_type'


class Amenity(AbstractItem):

    ''' Amenity Object Definition '''

    class Meta:
        db_table = 'amenities'


class Facility(AbstractItem):

    ''' Facility Model Definition '''

    class Meta:
        db_table = 'facilities'


class HouseRule(AbstractItem):

    ''' HouseRule Model Definition '''

    class Meta:
        db_table = 'house_rules'


class Photo(core_models.TimeStampedModel):

    ''' Photo Model Definition'''

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to='room_photos')
    room = models.ForeignKey('Room', related_name='photos' ,on_delete=models.CASCADE)

    class Meta:
        db_table = 'photos'
    
    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    ''' Room Model Definition'''

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField(help_text="총 몇 명이 예약하시나요??")
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey('users.User', on_delete=models.CASCADE)
    room_type = models.ForeignKey('RoomType', blank=True, on_delete=models.CASCADE, null=True)
    amenities = models.ManyToManyField('Amenity', related_name='rooms', blank=True)
    facilities = models.ManyToManyField('Facility', related_name='rooms', blank=True)
    house_rules = models.ManyToManyField('HouseRule', related_name='rooms', blank=True)

    class Meta:
        db_table = 'rooms'
    
    def __str__(self):
        return self.name
    
    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews), 2)
        return 0
    
    def first_photo(self):
        photo, = self.photos.all()[:1]
        print(photo)
        return photo.file.url