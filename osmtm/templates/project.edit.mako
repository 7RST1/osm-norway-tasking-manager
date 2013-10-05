# -*- coding: utf-8 -*-
<%inherit file="base.mako"/>
<%block name="header">
<a href="${request.route_url('home')}" class="brand"><i class="icon-home"></i></a>
<div class="brand">${project.name} - Edit</div>
</%block>
<%block name="content">
<script>
  var converter = new Showdown.converter();
</script>
<div class="container">
  <form method="post" action="" enctype="multipart/form-data" class="form">
    <div class="tabbable tabs">
      <ul class="nav nav-tabs">
        <li><a href="#description" data-toggle="tab">Description</a></li>
        <li><a href="#area" data-toggle="tab">Area</a></li>
        <li><a href="#imagery" data-toggle="tab">Imagery</a></li>
      </ul>
      <div class="tab-content">
        <div class="tab-pane" id="description">
          ${description()}
        </div>
        <div class="tab-pane" id="area">
          Area modifications are not available yet.
        </div>
        <div class="tab-pane" id="imagery">
          ${imagery()}
        </div>
      </div>
    </div>
    <div class="form-actions"><a href="${request.route_url('project', project=project.id)}" class="btn">Cancel</a>
      <input id="id_submit" type="submit" value="Save the modifications" name="form.submitted" class="btn btn-primary"/>
    </div>
  </form>
  <script type="text/javascript" src="${request.static_url('osmtm:static/js/project.edit.js')}"></script>
</div>
</%block>
<%block name="description">
    <div class="tabbable tabs-left">
      <ul class="nav nav-tabs" id="languages">
        % for locale, translation in project.translations.iteritems():
        <li><a href="#${locale}" data-toggle="tab">${locale}</a></li>
        % endfor
      </ul>
      <div class="tab-content">
        % for locale, translation in project.translations.iteritems():
        <div class="tab-pane active" id="${locale}">
          <input id="id_name" type="text" name="name_${locale}"
                 value="${translation.name}"
                 placeholder="Name"
                 class="text input-xxlarge"/>

          <!-- short_description -->
          <label for="id_short_description" class="control-label">Short Description</label>
          <div class="tab-content">
            <div class="tab-pane active" id="short_description_${locale}_edit">
              <textarea id="id_short_description_${locale}"
                        name="short_description_${locale}"
                        style="width: 80%;"
                        rows="3" class="text span4">${translation.short_description}</textarea>
            </div>
          </div>

          <!-- description -->
          <label for="id_description" class="control-label">Description</label>
          <ul class="nav nav-pills small">
            <li class="active">
              <a href="#description_${locale}_edit" data-toggle="tab">Edit</a>
            </li>
            <li>
              <a href="#description_${locale}_preview" data-toggle="tab">Preview</a>
            </li>
          </ul>
          <div class="tab-content">
            <div class="tab-pane active" id="description_${locale}_edit">
              <textarea id="id_description_${locale}"
                        name="description_${locale}"
                        style="width: 80%;"
                        rows="5" class="text span4">${translation.description}</textarea>
            </div>
            <div class="tab-pane preview" id="description_${locale}_preview"></div>
          </div>
        </div>
        <script>
          (function () {
            var description = $('#id_description_${locale}'),
            description_preview = $('#description_${locale}_preview');
            description.keyup(function() {
              var html = converter.makeHtml(description.val());
              description_preview.html(html);
            }).trigger('keyup');
          })();
        </script>
        % endfor
      </div>
    </div>
</%block>

<%block name="imagery">
<div class="form-horizontal">
<div class="control-group">
  <label class="control-label" for="id_imagery">URL to service</label>
  <div class="controls">
    <input type="text" class="span9" id="id_imagery" name="imagery" value="${project.imagery}"/>
    <p class="help-block">
    <strong>Note:</strong> Follow this format for TMS urls.<br>tms[22]:http://hiu-maps.net/hot/1.0.0/kathmandu_flipped/{zoom}/{x}/{y}.png
    </p>
  </div>
</div>
<div class="control-group">
  <label class="control-label" for="id_license">Required License</label>
  <div class="controls">
    <select id="id_license" name="license_id">
      <option value="" />
      % for l in licenses:
      <%
      selected = ""
      if project.license is not None and l.id == project.license.id:
        selected = "selected"
      %>
      <option value="${l.id}" ${selected}>${l.name}</a>
      % endfor
    </select>
  </div>
</div>
</div>
</%block>
