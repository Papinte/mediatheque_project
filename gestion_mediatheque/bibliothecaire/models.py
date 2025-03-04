from django.db import models
from django.utils import timezone

class Media(models.Model):
    title = models.CharField(max_length=200)
    available = models.BooleanField(default=True)
    borrow_date = models.DateTimeField(null=True, blank=True)
    borrower = models.ForeignKey('Borrower', on_delete=models.SET_NULL, null=True, blank=True)
    empruntable = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.title}"

    def is_overdue(self):
        if self.borrow_date and not self.available:
            return (timezone.now() - self.borrow_date).days > 7
        return False

class Book(Media):
    author = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} (Book)"

class DVD(Media):
    director = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} (DVD)"

class CD(Media):
    artist = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} (CD)"

class BoardGame(models.Model):
    title = models.CharField(max_length=200)
    creator = models.CharField(max_length=100)
    empruntable = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} (Board Game)"

class Borrower(models.Model):
    name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, default="default@example.com", null=False, blank=False)
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} {self.first_name}"