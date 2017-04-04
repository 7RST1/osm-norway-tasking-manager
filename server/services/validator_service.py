from flask import current_app
from server.models.dtos.mapping_dto import TaskDTOs
from server.models.dtos.validator_dto import LockForValidationDTO, UnlockAfterValidationDTO
from server.models.postgis.task import Task, TaskStatus
from server.models.postgis.utils import NotFound
from server.services.project_service import ProjectService


class ValidatatorServiceError(Exception):
    """ Custom exception to notify callers that error has occurred """
    def __init__(self, message):
        if current_app:
            current_app.logger.error(message)


class ValidatorService:

    project_service = ProjectService

    def __init__(self, project_id, project_service=None):
        """
        Construct validator service and dependencies
        :param project_id: ID of project in scope
        :param project_service: Injectable project service, for unit testing
        """
        if project_service is None:
            self.project_service = ProjectService.from_project_id(project_id)
        else:
            self.project_service = project_service

    def lock_tasks_for_validation(self, validation_dto: LockForValidationDTO) -> TaskDTOs:
        """
        Lock supplied tasks for validation
        :raises ValidatatorServiceError
        """
        # Loop supplied tasks to check they can all be locked for validation
        tasks_to_lock = []
        for task_id in validation_dto.task_ids:
            task = Task.get(task_id, validation_dto.project_id)

            if task is None:
                raise NotFound(f'Task {task_id} not found')

            if TaskStatus(task.task_status) not in [TaskStatus.DONE, TaskStatus.VALIDATED]:
                raise ValidatatorServiceError(f'Task {task_id} is not DONE or VALIDATED')

            if task.task_locked:
                raise ValidatatorServiceError(f'Task: {task_id} is already locked')

            tasks_to_lock.append(task)

        user_can_validate, error_msg = self.project_service.is_user_permitted_to_validate(validation_dto.user_id)

        if not user_can_validate:
            raise ValidatatorServiceError(error_msg)

        # Lock all tasks for validation
        dtos = []
        for task in tasks_to_lock:
            task.lock_task(validation_dto.user_id)
            dtos.append(task.as_dto())

        task_dtos = TaskDTOs()
        task_dtos.tasks = dtos

        return task_dtos

    @staticmethod
    def unlock_tasks_after_validation(validated_dto: UnlockAfterValidationDTO) -> TaskDTOs:
        """
        Unlocks supplied tasks after validation
        :raises ValidatatorServiceError
        """
        # Loop supplied tasks to check they can all be unlocked after validation
        tasks_to_unlock = []
        for validated_task in validated_dto.validated_tasks:
            task = Task.get(validated_task.task_id, validated_dto.project_id)

            if task is None:
                raise NotFound(f'Task {validated_task.task_id} not found')

            if TaskStatus(task.task_status) not in [TaskStatus.DONE, TaskStatus.VALIDATED]:
                raise ValidatatorServiceError(f'Task {validated_task.task_id} is not DONE or VALIDATED')

            if not task.task_locked:
                raise ValidatatorServiceError(f'Task: {validated_task.task_id} is not locked')

            if task.lock_holder_id != validated_dto.user_id:
                raise ValidatatorServiceError('Attempting to unlock a task owned by another user')

            tasks_to_unlock.append(dict(task=task, new_state=TaskStatus[validated_task.status],
                                        comment=validated_task.comment))

        # Unlock all tasks
        dtos = []
        for task_to_unlock in tasks_to_unlock:
            task = task_to_unlock['task']
            task.unlock_task(validated_dto.user_id, task_to_unlock['new_state'], task_to_unlock['comment'])
            dtos.append(task.as_dto())

        task_dtos = TaskDTOs()
        task_dtos.tasks = dtos

        return task_dtos