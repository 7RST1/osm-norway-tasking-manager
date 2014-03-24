<p class="muted">
<span>${_('Task is too big?')}</span>
  % if task.zoom is not None:
    <%
      disabled = ""
      tooltip = ""
      if (task.zoom - task.project.zoom) > 0:
        disabled = "disabled linethrough"
        tooltip = "You cannot split this task more."
    %>
      <a id="split" href="${request.route_url('task_split', task=task.id, project=task.project_id)}"
         rel="tooltip" data-original-title="${tooltip}"
         data-confirm="${_('Are you sure you want to split this task?')}"
         class="${disabled}">
         ${_('Split')} <i class="icon-split"></i>
      </a>
  % endif
</p>
