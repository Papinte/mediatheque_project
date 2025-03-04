from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Borrower, Book, DVD, CD, BoardGame
from django.utils import timezone
import datetime

class BibliothecaireTests(TestCase):
    def setUp(self):
        # Créer un client et un utilisateur bibliothécaire
        self.client = Client()
        self.user = User.objects.create_user(username='biblio', password='test123')
        self.client.login(username='biblio', password='test123')

        # Données initiales
        self.borrower = Borrower.objects.create(name='Dupont', first_name='Jean', email='jean.dupont@example.com')
        self.book = Book.objects.create(title='Livre Test', author='Auteur Test')
        self.dvd = DVD.objects.create(title='DVD Test', director='Réalisateur Test')
        self.cd = CD.objects.create(title='CD Test', artist='Artiste Test')
        self.boardgame = BoardGame.objects.create(title='Jeu Test', creator='Créateur Test')

    # Afficher la page d’index (protégée)
    def test_index(self):
        response = self.client.get(reverse('bibliothecaire:index'))
        self.assertEqual(response.status_code, 200)

    # Afficher la liste des membres
    def test_borrower_list(self):
        response = self.client.get(reverse('bibliothecaire:borrower_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dupont')

    # Créer un membre
    def test_borrower_create(self):
        response = self.client.post(reverse('bibliothecaire:borrower_create'), {
            'name': 'Martin',
            'first_name': 'Luc',
            'email': 'luc.martin@example.com',
            'blocked': 'off'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Borrower.objects.count(), 2)  # 1 initial + 1 créé
        self.assertTrue(Borrower.objects.filter(name='Martin').exists())

    # Mettre à jour un membre
    def test_borrower_update(self):
        response = self.client.post(reverse('bibliothecaire:borrower_update', args=[self.borrower.pk]), {
            'name': 'Dupont',
            'first_name': 'Jean-Paul',
            'email': 'jean.dupont@example.com',
            'blocked': 'off'
        })
        self.assertEqual(response.status_code, 302)
        self.borrower.refresh_from_db()
        self.assertEqual(self.borrower.first_name, 'Jean-Paul')

    #Supprimer un membre
    def test_borrower_delete(self):
        response = self.client.post(reverse('bibliothecaire:borrower_delete', args=[self.borrower.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Borrower.objects.filter(pk=self.borrower.pk).exists())

    # Afficher la liste des médias
    def test_media_list(self):
        response = self.client.get(reverse('bibliothecaire:media_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Livre Test')
        self.assertContains(response, 'Jeu Test')

    # Ajouter un média (exemple avec Book)
    def test_media_create_book(self):
        response = self.client.post(reverse('bibliothecaire:media_create'), {
            'media_type': 'Book',
            'title': 'Nouveau Livre',
            'author': 'Auteur Nouveau'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(title='Nouveau Livre').exists())

    # Créer un emprunt
    def test_borrow_media(self):
        response = self.client.post(reverse('bibliothecaire:borrow_media', args=[self.book.pk]), {
            'borrower': self.borrower.pk
        })
        self.assertEqual(response.status_code, 302)
        self.book.refresh_from_db()
        self.assertFalse(self.book.available)
        self.assertEqual(self.book.borrower, self.borrower)

    # Retourner un emprunt
    def test_return_media(self):
        self.book.available = False
        self.book.borrower = self.borrower
        self.book.borrow_date = timezone.now()
        self.book.save()
        response = self.client.post(reverse('bibliothecaire:return_media', args=[self.book.pk]))
        self.assertEqual(response.status_code, 302)
        self.book.refresh_from_db()
        self.assertTrue(self.book.available)
        self.assertIsNone(self.book.borrower)

    # Contrainte - Max 3 emprunts
    def test_max_3_emprunts(self):
        # Créer 3 emprunts
        for i in range(3):
            book = Book.objects.create(title=f'Livre {i}', author='Test')
            book.available = False
            book.borrower = self.borrower
            book.borrow_date = timezone.now()
            book.save()
        # Tenter un 4e emprunt
        new_book = Book.objects.create(title='Livre 4', author='Test')
        response = self.client.post(reverse('bibliothecaire:borrow_media', args=[new_book.pk]), {
            'borrower': self.borrower.pk
        })
        self.assertEqual(response.status_code, 302)
        new_book.refresh_from_db()
        self.assertTrue(new_book.available)

    # Contrainte - Pas d’emprunt si retard
    def test_pas_emprunt_si_retard(self):
        self.book.available = False
        self.book.borrower = self.borrower
        self.book.borrow_date = timezone.now() - datetime.timedelta(days=8)  # Retard
        self.book.save()
        new_book = Book.objects.create(title='Nouveau', author='Test')
        response = self.client.post(reverse('bibliothecaire:borrow_media', args=[new_book.pk]), {
            'borrower': self.borrower.pk
        })
        self.assertEqual(response.status_code, 302)
        new_book.refresh_from_db()
        self.assertTrue(new_book.available)

    # Contrainte - Jeux non empruntables
    def test_jeux_non_empruntables(self):
        response = self.client.post(reverse('bibliothecaire:borrow_media', args=[self.boardgame.pk]), {
            'borrower': self.borrower.pk
        })
        self.assertEqual(response.status_code, 302)
        self.boardgame.refresh_from_db()
        self.assertTrue(self.boardgame.empruntable is False)

    # Sécurité - Accès sans connexion
    def test_acces_sans_connexion(self):
        self.client.logout()
        response = self.client.get(reverse('bibliothecaire:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/bibliothecaire/')