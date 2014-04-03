# -*- coding: utf-8 -*-
<div>
  <%include file="task.status.mako" />
  <a href="#task/${task.id}">Task #${task.id}</a> in <a class="clear" href="#">Project #${task.project_id}</a>
  <a class="btn btn-sm btn-link clear pull-right" title="${_('Clear selection')}"><i class="glyphicon glyphicon-remove"></i></a>
  <div id="task_actions">
% if task.locked:
  <%include file="task.locked.mako" />
% else:
  <%include file="task.unlocked.mako" />
% endif

% if task.state in [task.state_ready, task.state_invalidated]:
    <%include file="task.state.ready.mako" />
% endif

% if task.state == task.state_done:
    <%include file="task.state.done.mako" />
% endif

    <%include file="task.instructions.mako" />
    <hr />
    <h4>${_('History')}</h4>
    <div><%include file="task.history.mako" /></div>
  </div>
</div>

<%
from geoalchemy2 import shape
from geoalchemy2.functions import ST_Centroid
import geojson
geometry_as_shape = shape.to_shape(task.geometry)
centroid = geometry_as_shape.centroid
bounds = geometry_as_shape.bounds
project = task.project
%>
<script>
var task_geometry = ${geojson.dumps(geometry_as_shape)|n};
var task_centroid = [${centroid.x}, ${centroid.y}];
var task_bounds = [${bounds[0]}, ${bounds[1]}, ${bounds[2]}, ${bounds[3]}];
$('[rel=tooltip]').tooltip();
var login_url = "${request.route_url('login')}";
var gpx_url = "${request.route_url('task_gpx', project=task.project_id, task=task.id)}";
% if project.imagery is not None and project.imagery != 'None' and \
    (project.license in user.accepted_licenses or not project.license):
var imagery_url = "${project.imagery}";
% endif
</script>
