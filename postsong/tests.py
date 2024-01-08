from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Artist, Song

class SongTestCase(TestCase):
    def setUp(self):
        # Criar objetos de teste, se necessário
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.artist = Artist.objects.create(name='Test Artist')
        self.song_data = {
            'title': 'Test Song',
            'artist': self.artist,
            'key': 'C',
            'tuning': 'Standard',
        }

    def test_postsong_view_get(self):
        # Testar a view postsong com uma solicitação GET
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('postsong'))

        self.assertEqual(response.status_code, 200 )
        self.assertIn('artists', response.context)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_postsong_view_post_success(self):
        # Testar a view postsong com uma solicitação POST bem-sucedida
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('postsong'), data=self.song_data)

        self.assertEqual(response.status_code, 302)  # Deve redirecionar após um POST bem-sucedido

        # Adicione mais asserções conforme necessário para verificar o comportamento esperado

    def test_postsong_view_post_failure(self):
        # Testar a view postsong com uma solicitação POST mal-sucedida
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('postsong'), data={})

        self.assertEqual(response.status_code, 200)  # Deve permanecer na mesma página após um POST mal-sucedido

        # Adicione mais asserções conforme necessário para verificar o comportamento esperado

    def test_postchord_view(self):
        # Testar a view postchord
        self.client.login(username='testuser', password='testpassword')

        # Suponha que você precisa de dados específicos na sessão para acessar esta view
        self.client.session['liberar_postchord'] = True
        self.client.session['artist'] = 'Test Artist'
        self.client.session['title'] = 'Test Song'

        response = self.client.get(reverse('postchord'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('song', response.context)
        self.assertIn('lyric', response.context)

    def test_finally_post_chord_view(self):
        # Testar a view finally_post_chord
        self.client.login(username='testuser', password='testpassword')

        # Suponha que você precisa de dados específicos na sessão para acessar esta view
        self.client.session['user_id'] = self.user.id
        self.client.session['liberar_postchord'] = True
        self.client.session['artist'] = 'Test Artist'
        self.client.session['title'] = 'Test Song'

        response = self.client.post(reverse('song-posted'), data={'chords': 'C G Am F', 'description': 'Test description'})

        self.assertEqual(response.status_code, 302)  # Deve redirecionar após um POST bem-sucedido

        # Adicione mais asserções conforme necessário para verificar o comportamento esperado

    # Você pode adicionar mais métodos de teste conforme necessário
