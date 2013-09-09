from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest
from pyramid.url import route_url
from ..models import (
    DBSession,
    Project,
    Area
    )

import mapnik

@view_config(route_name='project', renderer='project.mako', http_cache=0)
def project(request):
    id = request.matchdict['project']
    project = DBSession.query(Project).get(id)

    if project is None:
        request.session.flash("Sorry, this project doesn't  exist")
        return HTTPFound(location = route_url('home', request))

    return dict(page_id='project', project=project)

@view_config(route_name='project_new', renderer='project.new.mako',)
def project_new(request):
    if 'form.submitted' in request.params:
        area = Area(
            request.params['geometry']
        )

        DBSession.add(area)
        DBSession.flush()

        project = Project(
            request.params['name'],
            area
        )

        DBSession.add(project)
        DBSession.flush()
        return HTTPFound(location = route_url('project_partition', request, project=project.id))
    return dict(page_id='project_new')

@view_config(route_name='project_partition', renderer='project.partition.mako', )
def project_partition(request):
    id = request.matchdict['project']
    project = DBSession.query(Project).get(id)

    if 'form.submitted' in request.params:
        zoom = int(request.params['zoom'])
        project.auto_fill(zoom)

        return HTTPFound(location = route_url('project_edit', request, project=project.id))

    return dict(page_id='project_partition', project=project)

@view_config(route_name='project_edit', renderer='project.edit.mako', )
def project_edit(request):
    id = request.matchdict['project']
    project = DBSession.query(Project).get(id)

    if 'form.submitted' in request.params:
        project.name = request.params['name']
        project.short_description = request.params['short_description']
        project.description = request.params['description']

        DBSession.add(project)
        return HTTPFound(location = route_url('project', request, project=project.id))

    return dict(page_id='project_edit', project=project)

@view_config(route_name='project_mapnik', renderer='mapnik')
def project_mapnik(request):
    x = request.matchdict['x']
    y = request.matchdict['y']
    z = request.matchdict['z']
    project_id = request.matchdict['project']

    query = '(SELECT * FROM tasks WHERE project_id = %s) as tasks' % (str(project_id))
    tasks = mapnik.Layer('Map tasks from PostGIS')
    tasks.datasource = mapnik.PostGIS(
        host='localhost',
        user='www-data',
        dbname='osmtm',
        table=query
    )
    tasks.styles.append('tile')
    tasks.srs = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"

    return [tasks]
