from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from tasks.models import Task


class Command(BaseCommand):
    help = "Create default user groups and assign permissions"

    def handle(self, *args, **kwargs):
        groups = {
            "Admin": None,  # Admins get all permissions
            "Manager": ["view_task"],  # Can list all tasks
            "User": [],  # No extra permissions, only owns their tasks
        }

        for group_name, permissions in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)

            if permissions:
                perms = Permission.objects.filter(
                    content_type__app_label="tasks", codename__in=permissions
                )
                group.permissions.set(perms)

            self.stdout.write(
                self.style.SUCCESS(f'Group "{group_name}" configured successfully')
            )
