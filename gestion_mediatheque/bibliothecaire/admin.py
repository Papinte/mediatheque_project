from django.contrib import admin
from .models import Borrower, Book, DVD, CD, BoardGame

admin.site.register(Borrower)
admin.site.register(Book)
admin.site.register(DVD)
admin.site.register(CD)
admin.site.register(BoardGame)