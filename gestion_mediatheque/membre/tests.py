from django.test import TestCase, Client
from django.urls import reverse  # Ajouté ici
from bibliothecaire.models import Book, DVD, CD, BoardGame

class MembreTests(TestCase):
    def setUp(self):
        self.client = Client()
        Book.objects.create(title='Livre Public', author='Auteur')
        DVD.objects.create(title='DVD Public', director='Réalisateur')
        CD.objects.create(title='CD Public', artist='Artiste')
        BoardGame.objects.create(title='Jeu Public', creator='Créateur')

    # Test 1 : Afficher la liste des médias (public)
    def test_media_list(self):
        response = self.client.get(reverse('membre:media_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Livre Public')
        self.assertContains(response, 'DVD Public')
        self.assertContains(response, 'CD Public')
        self.assertContains(response, 'Jeu Public')