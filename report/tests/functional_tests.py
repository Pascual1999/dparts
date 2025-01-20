from django.test import RequestFactory, TestCase, tag
from django.contrib.auth import get_user_model
from report.views import report_view


User = get_user_model()


@tag('functional_tests')
class ReportTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email='testemail@gmailcom',
            password='testpassword')

    def test_generate_report(self):
        """ Prueba de generación de reporte """
        request = self.factory.get('admin/report/')
        request.user = self.user

        response = report_view(request)
        self.assertEqual(response.status_code, 200)
