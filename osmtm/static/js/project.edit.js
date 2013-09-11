$(document).ready(function() {
    var converter = new Showdown.converter();

    var workflow = $('#id_workflow'),
        workflow_preview = $('#workflow_preview');
    workflow.keyup(function() {
        var html = converter.makeHtml(workflow.val());
        workflow_preview.html(html);
    }).trigger('keyup');

    $('#languages a:first').tab('show');
});
