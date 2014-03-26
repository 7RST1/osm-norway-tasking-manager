# -*- coding: utf-8 -*-
<%inherit file="base.mako"/>
<%block name="header">
<a href="${request.route_url('home')}" class="brand"><i class="icon-home"></i></a>
<div class="brand">New Project</div>
</%block>
<%block name="content">
<div class="container">
    <h3>What kind of project are you about to create?</h3>
    <div class="row">
      <div class="span6">
        <label class="radio">
          <input type="radio" id="grid" name="type" value="grid"/>
          Square Grid
          <p class="help-block">
            Area of interest is split into square grids.
          </p>
        </label>
      </div>
      <div class="span6">
        <label class="radio">
          <input type="radio" id="import" name="type" value="import" />
          Imported Geometries
          <p class="help-block">
            You already have polygons you want people to work on.
          </p>
        </label>
      </div>
    </div>
</div>
<script>
  $('input[type=radio]').attr('checked', false);
  $('input[type=radio]').on('change', function() {
    switch ($(this)[0].id) {
      case "grid":
        window.location = "${request.route_url('project_new_grid')}";
        break;
      case "import":
        window.location = "${request.route_url('project_new_import')}";
        break;
    }
  });
</script>
</%block>
