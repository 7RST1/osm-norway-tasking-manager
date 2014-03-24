## works for ready or invalidated tasks
% if user and task.user == user:
  <form action="${request.route_url('task_done', task=task.id, project=task.project_id)}" method="POST" class="form-horizontal">
    <p>
    <button type="submit" class="btn btn-success btn-small"><i class="icon-ok icon-white"></i> ${_('Mark task as done')}</button>
    </p>
  </form>
  <%include file="task.split.mako" />
% endif
