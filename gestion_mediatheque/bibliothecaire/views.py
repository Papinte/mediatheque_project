from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Borrower, Book, DVD, CD, BoardGame, Media
from django.utils import timezone

@login_required
def index(request):
    return render(request, 'bibliothecaire/index.html')

# Vue pour afficher la liste de tous les emprunteurs
@login_required
def borrower_list(request):
    borrowers = Borrower.objects.all()
    return render(request, 'bibliothecaire/borrower_list.html', {'borrowers': borrowers})

# Vue pour créer un nouvel emprunteur
@login_required
def borrower_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        blocked = request.POST.get('blocked') == 'on'
        Borrower.objects.create(name=name, first_name=first_name, email=email, blocked=blocked)
        messages.success(request, f"{name} {first_name} a été créé avec succès.")
        return redirect('bibliothecaire:borrower_list')
    return render(request, 'bibliothecaire/borrower_form.html')

# Vue pour mettre à jour un emprunteur existant
@login_required
def borrower_update(request, pk):
    borrower = get_object_or_404(Borrower, pk=pk)
    if request.method == 'POST':
        borrower.name = request.POST.get('name')
        borrower.first_name = request.POST.get('first_name')
        borrower.email = request.POST.get('email')
        borrower.blocked = request.POST.get('blocked') == 'on'
        borrower.save()
        messages.success(request, f"{borrower.name} {borrower.first_name} a été mis à jour avec succès.")
        return redirect('bibliothecaire:borrower_list')
    return render(request, 'bibliothecaire/borrower_form.html', {'borrower': borrower})

# Vue pour supprimer un emprunteur
@login_required
def borrower_delete(request, pk):
    borrower = get_object_or_404(Borrower, pk=pk)
    if request.method == 'POST':
        # Vérifie si l'emprunteur a des médias empruntés non disponibles
        if Book.objects.filter(borrower=borrower, available=False).exists() or \
           DVD.objects.filter(borrower=borrower, available=False).exists() or \
           CD.objects.filter(borrower=borrower, available=False).exists():
            full_name = f"{borrower.name} {borrower.first_name}"
            messages.error(request, f"Impossible de supprimer {full_name} : il a emprunté des médias.")
        else:
            full_name = f"{borrower.name} {borrower.first_name}"
            borrower.delete()
            messages.success(request, f"{full_name} a été supprimé avec succès.")
        return redirect('bibliothecaire:borrower_list')
    messages.error(request, "Cette action nécessite une confirmation via un formulaire.")
    return redirect('bibliothecaire:borrower_list')

# Vue pour afficher la liste de tous les médias
@login_required
def media_list(request):
    books = Book.objects.all()
    dvds = DVD.objects.all()
    cds = CD.objects.all()
    boardgames = BoardGame.objects.all()
    return render(request, 'bibliothecaire/media_list.html', {
        'books': books,
        'dvds': dvds,
        'cds': cds,
        'boardgames': boardgames,
    })

# Vue pour créer un nouveau média
@login_required
def media_create(request):
    if request.method == 'POST':
        media_type = request.POST.get('media_type')
        title = request.POST.get('title')
        if media_type == 'Book':
            author = request.POST.get('author')
            Book.objects.create(title=title, author=author)
        elif media_type == 'DVD':
            director = request.POST.get('director')
            DVD.objects.create(title=title, director=director)
        elif media_type == 'CD':
            artist = request.POST.get('artist')
            CD.objects.create(title=title, artist=artist)
        elif media_type == 'BoardGame':
            creator = request.POST.get('creator')
            BoardGame.objects.create(title=title, creator=creator)
        messages.success(request, f"{title} a été créé avec succès.")
        return redirect('bibliothecaire:media_list')
    return render(request, 'bibliothecaire/media_create.html')

# Vue pour mettre à jour un livre
@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.save()
        messages.success(request, f"{book.title} a été mis à jour avec succès.")
        return redirect('bibliothecaire:media_list')
    return render(request, 'bibliothecaire/media_update.html', {'media': book, 'media_type': 'Book'})

# Vue pour supprimer un livre
@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        titre = book.title
        book.delete()
        messages.success(request, f"{titre} a été supprimé avec succès.")
        return redirect('bibliothecaire:media_list')
    messages.error(request, "Cette action nécessite une confirmation via un formulaire.")
    return redirect('bibliothecaire:media_list')

# Vue pour mettre à jour un DVD
@login_required
def dvd_update(request, pk):
    dvd = get_object_or_404(DVD, pk=pk)
    if request.method == 'POST':
        dvd.title = request.POST.get('title')
        dvd.director = request.POST.get('director')
        dvd.save()
        messages.success(request, f"{dvd.title} a été mis à jour avec succès.")
        return redirect('bibliothecaire:media_list')
    return render(request, 'bibliothecaire/media_update.html', {'media': dvd, 'media_type': 'DVD'})

@login_required
def dvd_delete(request, pk):
    dvd = get_object_or_404(DVD, pk=pk)
    if request.method == 'POST':
        titre = dvd.title
        dvd.delete()
        messages.success(request, f"{titre} a été supprimé avec succès.")
        return redirect('bibliothecaire:media_list')
    messages.error(request, "Cette action nécessite une confirmation via un formulaire.")
    return redirect('bibliothecaire:media_list')

@login_required
def cd_update(request, pk):
    cd = get_object_or_404(CD, pk=pk)
    if request.method == 'POST':
        cd.title = request.POST.get('title')
        cd.artist = request.POST.get('artist')
        cd.save()
        messages.success(request, f"{cd.title} a été mis à jour avec succès.")
        return redirect('bibliothecaire:media_list')
    return render(request, 'bibliothecaire/media_update.html', {'media': cd, 'media_type': 'CD'})

@login_required
def cd_delete(request, pk):
    cd = get_object_or_404(CD, pk=pk)
    if request.method == 'POST':
        titre = cd.title
        cd.delete()
        messages.success(request, f"{titre} a été supprimé avec succès.")
        return redirect('bibliothecaire:media_list')
    messages.error(request, "Cette action nécessite une confirmation via un formulaire.")
    return redirect('bibliothecaire:media_list')

@login_required
def boardgame_update(request, pk):
    boardgame = get_object_or_404(BoardGame, pk=pk)
    if request.method == 'POST':
        boardgame.title = request.POST.get('title')
        boardgame.creator = request.POST.get('creator')
        boardgame.save()
        messages.success(request, f"{boardgame.title} a été mis à jour avec succès.")
        return redirect('bibliothecaire:media_list')
    return render(request, 'bibliothecaire/media_update.html', {'media': boardgame, 'media_type': 'BoardGame'})

@login_required
def boardgame_delete(request, pk):
    boardgame = get_object_or_404(BoardGame, pk=pk)
    if request.method == 'POST':
        titre = boardgame.title
        boardgame.delete()
        messages.success(request, f"{titre} a été supprimé avec succès.")
        return redirect('bibliothecaire:media_list')
    messages.error(request, "Cette action nécessite une confirmation via un formulaire.")
    return redirect('bibliothecaire:media_list')


@login_required
def borrow_media(request, media_id):
    media = None
    for model in [Book, DVD, CD]:
        try:
            media = get_object_or_404(model, pk=media_id)
            break
        except:
            continue

    if not media:
        messages.error(request, "Média introuvable ou non empruntable.")
        return redirect('bibliothecaire:media_list')

    if not media.empruntable:
        messages.error(request, "Ce média ne peut pas être emprunté.")
        return redirect('bibliothecaire:media_list')

    if not media.available:
        messages.error(request, "Ce média n’est pas disponible.")
        return redirect('bibliothecaire:media_list')

    borrowers = Borrower.objects.filter(blocked=False)

    if request.method == 'POST':
        borrower_id = request.POST.get('borrower')
        borrower = get_object_or_404(Borrower, pk=borrower_id)

        if borrower.blocked:
            messages.error(request, "Cet emprunteur est bloqué.")
            return redirect('bibliothecaire:media_list')

        # Vérification des retards
        if any(media.is_overdue() for media in Book.objects.filter(borrower=borrower, available=False)) or \
           any(media.is_overdue() for media in DVD.objects.filter(borrower=borrower, available=False)) or \
           any(media.is_overdue() for media in CD.objects.filter(borrower=borrower, available=False)):
            messages.error(request, "Cet emprunteur a un retard et ne peut pas emprunter.")
            return redirect('bibliothecaire:media_list')

        borrowed_count = sum(
            model.objects.filter(borrower=borrower, available=False).count()
            for model in [Book, DVD, CD]
        )
        if borrowed_count >= 3:
            messages.error(request, "Cet emprunteur a déjà 3 emprunts actifs.")
            return redirect('bibliothecaire:media_list')

        media.available = False
        media.borrower = borrower
        media.borrow_date = timezone.now()
        media.save()
        messages.success(request, f"{media.title} a été emprunté avec succès.")
        return redirect('bibliothecaire:media_list')

    return render(request, 'bibliothecaire/borrow_form.html', {'media': media, 'borrowers': borrowers})

@login_required
def return_media(request, media_id):
    try:
        media = None
        for model in [Book, DVD, CD, BoardGame]:
            try:
                media = get_object_or_404(model, pk=media_id)
                break
            except:
                continue

        if not media:
            messages.error(request, "Média non trouvé.")
            return redirect('bibliothecaire:media_list')

        if media.available:
            messages.error(request, "Ce média est déjà disponible.")
            return redirect('bibliothecaire:media_list')

        if request.method == 'POST':
            media.available = True
            media.borrower = None
            media.borrow_date = None
            media.save()
            messages.success(request, f"{media.title} a été retourné avec succès.")
            return redirect('bibliothecaire:media_list')

        return render(request, 'bibliothecaire/return_form.html', {'media': media})
    except Exception as e:
        messages.error(request, f"Une erreur s'est produite : {str(e)}")
        return redirect('bibliothecaire:media_list')