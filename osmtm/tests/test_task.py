from . import BaseTestCase

class TestTaskFunctional(BaseTestCase):

    def test_task(self):
        self.testapp.get('/project/1/task/1', status=200, xhr=True)

    def test_task__not_found(self):
        self.testapp.get('/project/1/task/99', status=404, xhr=True)

    def test_task__loggedin(self):
        headers = self.login_as_user1()
        self.testapp.get('/project/1/task/1', status=200,
                headers=headers,
                xhr=True)

    def test_task_done__not_loggedin(self):
        res = self.testapp.get('/project/1/task/1/done', status=302, xhr=True)

    def test_task_done__not_locked(self):
        headers = self.login_as_user1()
        self.testapp.get('/project/1/task/1/done', status=403,
                headers=headers,
                xhr=True)

    def test_task_done__locked(self):
        headers = self.login_as_user1()
        self.testapp.get('/project/1/task/2/lock', status=200,
                headers=headers,
                xhr=True)
        self.testapp.get('/project/1/task/2/done', status=200,
                headers=headers,
                xhr=True)

    def test_task_lock__not_loggedin(self):
        res = self.testapp.get('/project/1/task/3/lock', status=302, xhr=True)

    def test_task_lock(self):
        headers_user1 = self.login_as_user1()
        res = self.testapp.get('/project/1/task/3/lock', status=200,
                headers=headers_user1,
                xhr=True)
        self.assertTrue(res.json['success'])

        headers_user2 = self.login_as_user2()
        res = self.testapp.get('/project/1/task/3/lock', status=200,
                headers=headers_user2,
                xhr=True)
        # already locked by user1
        self.assertFalse(res.json['success'])

        # unlock the tile for later tests
        self.testapp.get('/project/1/task/3/unlock',
                headers=headers_user1,
                xhr=True)

    def test_task_lock__other_task_locked(self):
        headers = self.login_as_user1()
        headers_user1 = self.login_as_user1()
        res = self.testapp.get('/project/1/task/3/lock', status=200,
                headers=headers_user1,
                xhr=True)
        res = self.testapp.get('/project/1/task/4/lock', status=400,
                headers=headers,
                xhr=True)

        # unlock the tile for later tests
        self.testapp.get('/project/1/task/3/unlock',
                headers=headers_user1,
                xhr=True)

    def test_task_unlock(self):
        headers = self.login_as_user1()
        res = self.testapp.get('/project/1/task/3/lock', status=200,
                headers=headers,
                xhr=True)
        res = self.testapp.get('/project/1/task/3/unlock', status=200,
                headers=headers,
                xhr=True)
        self.assertTrue(res.json['success'])

    def test_task_invalidate(self):
        headers = self.login_as_user1()
        self.testapp.get('/project/1/task/5/lock',
                headers=headers,
                xhr=True)
        self.testapp.get('/project/1/task/5/done', status=200,
                headers=headers,
                xhr=True)

        headers = self.login_as_user2()
        self.testapp.get('/project/1/task/5/lock',
                headers=headers,
                xhr=True)
        res = self.testapp.get('/project/1/task/5/invalidate', status=200,
                params={
                    'comment': 'a comment'
                },
                headers=headers,
                xhr=True)

    def test_task_split(self):
        headers = self.login_as_user1()
        self.testapp.get('/project/1/task/6/lock',
                headers=headers,
                xhr=True)

        self.testapp.get('/project/1/task/6/split', status=200,
                headers=headers,
                xhr=True)

        self.testapp.get('/project/1/task/6', status=200,
                headers=headers,
                xhr=True)

        self.testapp.get('/project/1/task/10/lock',
                headers=headers,
                xhr=True)

        # can't split more than once
        self.testapp.get('/project/1/task/10/split', status=400,
                headers=headers,
                xhr=True)

        # unlock the tile for later tests
        self.testapp.get('/project/1/task/10/unlock',
                headers=headers,
                xhr=True)

    def test_task_random(self):
        headers = self.login_as_user1()
        res = self.testapp.get('/project/1/random', status=200,
                headers=headers,
                xhr=True)
        self.assertTrue(res.json['success'])

    def test_task_random__bordering_busy_tasks(self):
        import geoalchemy2
        import shapely
        import transaction
        from osmtm.models import Area, Project, DBSession

        shape = shapely.geometry.Polygon(
            [(7.23, 41.25), (7.23, 41.12), (7.41, 41.20)])
        geometry = geoalchemy2.shape.from_shape(shape, 4326)
        area = Area(geometry)
        project = Project(u'test project')
        project.area = area
        project.auto_fill(12)

        DBSession.add(project)
        DBSession.flush()
        project_id = project.id

        task = project.tasks[0]
        task.locked = True

        transaction.commit()

        headers = self.login_as_user1()
        res = self.testapp.get('/project/%d/random' % project_id, status=200,
                headers=headers,
                xhr=True)
        self.assertTrue(res.json['success'])

    def test_task_random__none_available(self):
        import geoalchemy2
        import shapely
        import transaction
        from osmtm.models import Area, Project, DBSession

        shape = shapely.geometry.Polygon(
            [(7.23, 41.25), (7.23, 41.12), (7.41, 41.20)])
        geometry = geoalchemy2.shape.from_shape(shape, 4326)
        area = Area(geometry)
        project = Project(u'test project')
        project.area = area
        project.auto_fill(10)

        DBSession.add(project)
        DBSession.flush()
        project_id = project.id

        for task in project.tasks:
            task.state = task.state_done
            DBSession.add(task)

        transaction.commit()

        headers = self.login_as_user1()
        res = self.testapp.get('/project/%d/random' % project_id, status=200,
                headers=headers,
                xhr=True)
        self.assertFalse(res.json['success'])
