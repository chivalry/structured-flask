import unittest

from base import BaseTestCase


class TestMainPlueprint(BaseTestCase):
    def test_index(self):
        # Ensure Flask is set up.
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome!', response.data)
        self.assertIn(b'Login', response.data)

    def test_404(self):
        # Ensure 404 error is handled.
        response = self.client.get('/404')
        self.assert404(response)
        self.assertTemplateUsed('errors/404.html')


if __name__ == '__main__':
    unittest.main()
