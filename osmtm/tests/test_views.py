from . import BaseTestCase

class TestViewsFunctional(BaseTestCase):

    def test_authenticated(self):

        headers = self.remember(self.admin_user_id)
        try:
            res = self.testapp.get('/', headers=headers, status=200)
        finally:
            self.forget()
        self.failUnless('admin_user' in res.body)

    def test_prefered_editor(self):
        self.testapp.get('/user/prefered_editor/the_editor', status=200, xhr=True)
        self.assertEqual(self.testapp.cookies['prefered_editor'], 'the_editor')

    def test_prefered_language(self):
        self.testapp.get('/user/prefered_language/the_language', status=200, xhr=True)
        self.assertEqual(self.testapp.cookies['_LOCALE_'], 'the_language')
