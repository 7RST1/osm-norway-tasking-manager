from pyramid.view import view_config
from pyramid.url import route_url
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPBadRequest,
    HTTPUnauthorized
    )
from ..models import (
    DBSession,
    Task,
    TaskHistory,
    User
    )

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import and_
from geoalchemy2.functions import ST_Union, ST_Disjoint

from pyramid.security import authenticated_userid

import random

@view_config(route_name='task_xhr', renderer='task.mako',
        http_cache=0)
def task_xhr(request):
    id = request.matchdict['id']
    session = DBSession()
    task = session.query(Task).get(id)

    user_id = authenticated_userid(request)
    if user_id:
        user = session.query(User).get(user_id)
    else:
        user = None

    locked_task = get_locked_task(task.project_id, user)

    filter = and_(TaskHistory.task_id==id, TaskHistory.old_state!=None)
    history = session.query(TaskHistory).filter(filter) \
        .order_by(TaskHistory.id.desc()).all()
    return dict(task=task,
            user=user,
            locked_task=locked_task,
            history=history)

@view_config(route_name='task_done', renderer='json')
def done(request):
    id = request.matchdict['id']
    session = DBSession()
    task = session.query(Task).get(id)

    user_id = authenticated_userid(request)

    if not user_id:
        return HTTPUnauthorized()

    user = session.query(User).get(user_id)

    if not user:
        return HTTPUnauthorized()

    task.state = 2
    task.user = None
    session.add(task)
    return dict(success=True,
            msg="Task marked as done. Thanks for your contribution")

@view_config(route_name='task_lock', renderer="json")
def lock(request):
    task_id = request.matchdict['id']
    session = DBSession()
    user_id = authenticated_userid(request)

    if not user_id:
        return HTTPUnauthorized()

    user = session.query(User).get(user_id)

    if not user:
        return HTTPUnauthorized()

    task = session.query(Task).get(task_id)

    task.user = user
    task.state = 1 # working
    session.add(task)
    return dict(success=True, task=dict(id=task.id))

@view_config(route_name='task_unlock', renderer="json")
def unlock(request):
    task_id = request.matchdict['id']
    session = DBSession()

    task = session.query(Task).get(task_id)

    task.user = None
    task.state = 0 # working
    session.add(task)
    return dict(success=True, task=dict(id=task.id))

@view_config(route_name='task_invalidate', renderer="json")
def invalidate(request):
    task_id = request.matchdict['id']
    session = DBSession()
    user_id = authenticated_userid(request)

    if not user_id:
        return HTTPUnauthorized()

    user = session.query(User).get(user_id)

    if not user:
        return HTTPUnauthorized()

    task = session.query(Task).get(task_id)

    task.user = user
    task.state = 0
    session.add(task)

    comment = request.params['comment']
    task.add_comment(comment)

    return dict(success=True,
            msg="Task invalidated.")

@view_config(route_name='task_split', renderer='json')
def split(request):
    task_id = request.matchdict['id']
    session = DBSession()
    user_id = authenticated_userid(request)

    if not user_id:
        return HTTPUnauthorized()

    user = session.query(User).get(user_id)

    if not user:
        return HTTPUnauthorized()

    task = session.query(Task).get(task_id)

    if task.zoom is None or (task.zoom - task.project.zoom) > 0:
        return HTTPBadRequest

    new_tasks = []
    for i in range(0, 2):
        for j in range(0, 2):
            t = Task(int(task.x)*2 + i, int(task.y)*2 + j, int(task.zoom)+1)
            t.project = task.project

    session.delete(task)

    return dict()


def get_locked_task(project_id, user):
    session = DBSession()
    print project_id
    print user
    try:
        filter = and_(Task.user==user, Task.state==1, Task.project_id==project_id)
        return session.query(Task).filter(filter).one()
    except NoResultFound, e:
        return None

@view_config(route_name='task_random', http_cache=0, renderer='json')
def random_task(request):
    "Gets a random not-done task. First it tries to get one that does not border any in-progress tasks."
    session = DBSession()
    project_id = request.matchdict['project']

    # we will ask about the area occupied by tasks locked by others, so we can steer clear of them
    state1 = session.query(
        Task.geometry.ST_Union().label('taskunion')
        ).filter_by(project_id=project_id, state=1).subquery()

    # first search attempt - all available tasks that do not border busy tasks
    taskgetter = session.query(Task) \
        .filter_by(project_id=project_id, state=0) \
        .filter(Task.geometry.ST_Disjoint(state1.c.taskunion))
    count = taskgetter.count()
    if count != 0:
        atask = taskgetter.offset(random.randint(0, count-1)).first()
        return HTTPFound(location = route_url('project', request, project=project_id) + "#task/%i" % atask.id)

    # second search attempt - if the non-bordering constraint gave us no hits, we discard that constraint
    taskgetter = session.query(Task) \
        .filter_by(project_id=project_id, state=0)
    count = taskgetter.count()
    if count != 0:
        atask = taskgetter.offset(random.randint(0, count-1)).first()
        return dict(success=True, task=dict(id=atask.id))

    return dict(success=False, msg="Random task... none available! Sorry.")

