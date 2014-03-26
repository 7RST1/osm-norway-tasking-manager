# -*- coding: utf-8 -*-
<%inherit file="base.mako"/>
<%block name="header">
<div class="brand">OSM Tasking Manager</div>
</%block>
<%block name="content">
<script type="text/javascript" src="${request.static_url('osmtm:static/js/lib/angular.min.js')}"></script>
<div class="container" ng-app="projects">
  <div class="row" ng-controller="projectCrtl">

    <div class="project well" ng-repeat="project in projects">
      <ul class="nav project-stats">
        <li><i class="icon-user"></i><span></span>
        </li>
        <li class="row">
          <table>
            <tr>
              <td>
                <div style="border: 1px solid #ccc;" class="progress">
                  <div style="width: {{project.done * 100}}%;" class="bar"></div>
                </div>
              </td>
              <td>{{project.done * 100}}%</td>
            </tr>
          </table>
        </li>
      </ul>
      <h4><a href="project/{{project.id}}">{{project.name}}</a>
      </h4>
      <div class="clear"></div>
      <div class="world_map">
        <div style="top: {{(-project.centroid[1] + 90) * 60 / 180 - 1}}px; left: {{(project.centroid[0] + 180) * 120 / 360 - 1}}px;" class="marker"></div>
      </div>
      {{project.short_description}}
      <div class="clear"></div>
      <span class="created-by">${_('Created by')} {{project.author}}</span> -
      <span class="updated-at">${_('Updated')} <span class="timeago">{{project.last_update | timeAgo}}</span></span>
    </div>
  </div>
</div>
<%
  from osmtm.models import dumps
%>

<script>
  projects = ${dumps([project.as_dict(request.locale_name) for project in projects])|n};
</script>
<script type="text/javascript" src="${request.static_url('osmtm:static/js/home.js')}"></script>
</%block>
