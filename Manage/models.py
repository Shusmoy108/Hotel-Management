from django.contrib.auth.models import User, AbstractUser
from django.db import models

# Create your models here.
from django.db.models.base import Model

star_numbers = (
        (0, "No star"),
        (1, "One star"),
        (2, "Two stars"),
        (3, "Three stars"),
        (4, "Four stars"),
        (5, "Five stars")
    )

class Guest(User):
    gender = models.CharField("Sex", max_length=10, choices=[("man", "Male"), ("women", "Female")])
    first_phone = models.IntegerField("Contact Number", max_length=15)
    second_phone = models.IntegerField("Another Contact Number", max_length=15)
    cell_phone = models.IntegerField("Landphone Number", max_length=15)
    active = models.BooleanField("Activated", default=False)





class Hotelier(Guest):
    #TODO: this is a sample permission, add relevant permissions later
    can_edit_hotel = models.BooleanField(default=False)
    can_edit_room = models.BooleanField(default=False)
    can_delete_hotel = models.BooleanField(default=False)
    can_delete_room = models.BooleanField(default=False)
    can_add_room= models.BooleanField(default=False)
    can_add_hotel= models.BooleanField(default=True)
    can_add_hotel= models.BooleanField(default=False)


    def __str__(self):
        return str(self.first_name)

    class Meta:
        verbose_name = "Hotel owner"
        verbose_name_plural = "Hotel owners"

class Commsion(models.Model):
    hotelier = models.ForeignKey(Hotelier, verbose_name="Hotelier")
    total = models.BigIntegerField('Total Number', default=0)
    start_date = models.DateField("Stay from", auto_now=True)
    end_date = models.DateField("Checkout Date", auto_now=True)
    status = models.BooleanField("Payment status", default=False)


    class Meta:
        verbose_name = "Wage"
        verbose_name_plural = "Fees"


class Hotel(models.Model) :
    name = models.CharField("Name", max_length=20)
    hotelier = models.ForeignKey(Hotelier, verbose_name="Hotelier")
    star_number = models.IntegerField("Star", max_length=1, choices=star_numbers)
    average_star_number = models.FloatField("Average star", default=0)
    critic_number = models.IntegerField("The number of commenters", default=0)
    grade = models.IntegerField("Grade", default=0)
    credit_number = models.IntegerField("Credit number", blank=False)
    address = models.TextField("Address", max_length=200, blank=False)
    city = models.CharField("City", max_length=20)
    phone_number = models.BigIntegerField("Contact Number")
    lake = models.BooleanField("Lake")
    pool = models.BooleanField(" Pool")
    sport = models.BooleanField("Sports facilities")
    breakfast = models.BooleanField("Breakfast")
    wifi = models.BooleanField("Wifi")
    parking = models.BooleanField("Parking")
    cafe = models.BooleanField("Cafe")


    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Hotel"
        verbose_name_plural = "Hotels"


class HotelPhoto(models.Model):
    photo = models.ImageField("Photo",upload_to=r"photo\hotelphotos")
    hotel = models.ForeignKey(Hotel, verbose_name="Hotel")

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, verbose_name="Hotel")
    type = models.CharField("Type", max_length=20)
    cost = models.BigIntegerField("Daily cost")
    area = models.IntegerField("Area")
    king_bed = models.IntegerField("Double bed")
    queen_bed = models.IntegerField("Single bed")
    tv = models.BooleanField("TV")
    wifi = models.BooleanField("Wifi")
    kitchen = models.BooleanField("kitchen")
    extra_bed = models.BooleanField("Cot")

    def __str__(self):
        return str( "Hotel " +self.hotel.name + ": room " + self.type)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"



class RoomPhoto(models.Model):
    room = models.ForeignKey(Room, verbose_name="room")
    photo = models.ImageField("Picture", upload_to=r"photo\roomphotos")



class Passenger(Guest):
    room = models.ManyToManyField(Room, verbose_name="room", through="Reservation")

    def __str__(self):
        return str(self.first_name)

    class Meta:
        verbose_name = "Passenger"
        verbose_name_plural = "Passengers"


class Reservation(models.Model):
    passenger = models.ForeignKey(Passenger, verbose_name="Passenger")
    room = models.ForeignKey(Room, verbose_name="Room")
    start_date = models.DateField("Stay from")
    end_date = models.DateField("Checkout Date")
    request_time = models.DateTimeField("Request Time", auto_now=True)
    total_cost = models.BigIntegerField("Total Cost")
    status_choices = (
        (1, "Paid"),
        (0, "Unpaid"),

    )
    status = models.IntegerField("Status", default=0)

    def __str__(self):
        return self.room.type + ": " + str(self.passenger)

    class Meta:
        verbose_name = "Reservation Request"
        verbose_name_plural = "Reservation Requests"


class Transaction(models.Model):
    reservation = models.OneToOneField(Reservation, verbose_name="Reservation Request")
    refrence_number = models.IntegerField("Refrence number", max_length=7)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"


class Comment(models.Model):
    passenger = models.ForeignKey(Passenger, verbose_name="Passenger")
    hotel = models.ForeignKey(Hotel, verbose_name="Hotel")
    text = models.TextField("Comment")
    star_number = models.IntegerField(choices=star_numbers, max_length=1)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
            return '%s: %s' % (self.passenger.first_name, self.text)



class Activation(models.Model):
    activation_link = models.CharField("Activation Link", max_length=20)
    user_id = models.IntegerField("User ID")


