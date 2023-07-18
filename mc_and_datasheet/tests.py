from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import MC_section, Field, File, CardData  # import your models here

class SectionViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.section = MC_section.objects.create(name='test_section', mc_section_session=self.user.username)
        self.field = Field.objects.create(field_question='test_question', field_session=self.user.username, mc_section=self.section)
        self.url = reverse('mc_and_datasheet:section', args=[self.section.id])  # replace with your url name

    def test_section_view_get(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mc_and_datasheet/section.html')  # replace with your template
        self.assertContains(response, 'test_section')

    def test_section_view_post_save(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.url, {'save': 'save', 'a'+str(self.field.id): 'test_answer'})
        self.field.refresh_from_db()
        self.assertEqual(self.field.field_answer, 'test_answer')  # replace with your logic

