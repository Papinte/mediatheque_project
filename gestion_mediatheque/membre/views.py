from django.shortcuts import render
from bibliothecaire.models import Book, DVD, CD, BoardGame

def media_list(request):
    books = Book.objects.all()
    dvds = DVD.objects.all()
    cds = CD.objects.all()
    board_games = BoardGame.objects.all()
    return render(request, 'membre/media_list.html', {
        'books': books,
        'dvds': dvds,
        'cds': cds,
        'board_games': board_games,
    })