import unittest
import transaction

from pyramid import testing

from .models import DBSession


def _initTestingDB():
    from sqlalchemy import create_engine
    engine = create_engine('postgresql://www-data@localhost/osmtm_tests')
    from .models import (
        Base,
        Job,
        )
    DBSession.configure(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with transaction.manager:
        job = Job(
            title=u'one',
            geometry='{"type":"Polygon","coordinates":[[[7.237243652343749,41.25922682850892],[7.23175048828125,41.12074559016745],[7.415771484374999,41.20552261955812],[7.237243652343749,41.25922682850892]]]}'
        )
        DBSession.add(job)

def _registerRoutes(config):
    config.add_route('home', '/')
    config.add_route('job_new', '/job/new')
    config.add_route('job', '/job/{job}')
    config.add_route('job_edit', '/job/{job}/edit')
    config.add_route('job_mapnik', '/job/{job}/{z}/{x}/{y}.{format}')

class TestJob(unittest.TestCase):
    def setUp(self):
        _initTestingDB()
        self.config = testing.setUp()
        _registerRoutes(self.config)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_it(self):
        from .views.job import job
        request = testing.DummyRequest()

        request.matchdict = {'job': 1}
        info = job(request)
        from .models import Job
        self.assertEqual(info['job'], DBSession.query(Job).get(1))

        # doesn't exist
        request.matchdict = {'job': 999}
        response = job(request)
        self.assertEqual(response.location, 'http://example.com/')

class TestJobNew(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        _registerRoutes(self.config)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_it(self):
        from .views.job import job_new

        request = testing.DummyRequest()
        response = job_new(request)

        request = testing.DummyRequest()
        request.params = {
            'form.submitted': True,
            'title':u'NewJob',
            'geometry':'{"type":"Polygon","coordinates":[[[7.237243652343749,41.25922682850892],[7.23175048828125,41.12074559016745],[7.415771484374999,41.20552261955812],[7.237243652343749,41.25922682850892]]]}'
        }
        response = job_new(request)
        self.assertEqual(response.location, 'http://example.com/job/2/edit')

class TestJobEdit(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        _registerRoutes(self.config)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_it(self):
        from .views.job import job_edit

        request = testing.DummyRequest()
        request.matchdict = {'job': 1}
        response = job_edit(request)
        from .models import Job
        self.assertEqual(response['job'], DBSession.query(Job).get(1))

        request = testing.DummyRequest()
        request.matchdict = {'job': 1}
        request.params = {
            'form.submitted': True,
            'title':u'NewJob',
            'short_description':u'SomeShortDescription',
            'description':u'SomeDescription',
        }
        response = job_edit(request)
        self.assertEqual(response.location, 'http://example.com/job/1')

class TestJobMapnik(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        _registerRoutes(self.config)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_it(self):
        from .views.job import job_mapnik

        request = testing.DummyRequest()
        request.matchdict = {
            'job': 1,
            'x': 532,
            'y': 383,
            'z': 10,
            'format': 'png'
        }
        response = job_mapnik(request)
        import mapnik
        self.assertEqual(isinstance(response[0], mapnik.Layer), True)

class FunctionalTests(unittest.TestCase):

    def setUp(self):
        from osmtm import main
        settings = {
            'sqlalchemy.url': 'postgresql://www-data@localhost/osmtm_tests'
        }
        self.app = main({}, **settings)

        from webtest import TestApp
        self.testapp = TestApp(self.app)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_home(self):
        res = self.testapp.get('', status=200)
        self.failUnless('one' in res.body)

    def test_job_mapnik(self):
        res = self.testapp.get('/job/1/10/532/383.png')
        self.assertTrue(res.content_type == 'image/png')

        res = self.testapp.get('/job/1/10/532/383.json')
        self.assertTrue('grid' in res.body)
