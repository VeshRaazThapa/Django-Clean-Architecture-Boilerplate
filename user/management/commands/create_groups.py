from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from user.models import UserRole


class Command(BaseCommand):
    help_text = "Create user groups"

    def handle(self, **options):
        groups = [
            {"id": 101, "name": "Country User", "type": "Admin"},
            {"id": 102, "name": "Province User", "type": "Admin"},
            {"id": 103, "name": "District User", "type": "Admin"},
            {"id": 104, "name": "Municipality Administrator", "type": "Admin"},
            {"id": 105, "name": "Ward Administrator", "type": "Admin"},
            {"id": 106, "name": "Municipality Data Collector", "type": "Data Collector"},
            {"id": 107, "name": "Ward Data Collector", "type": "Data Collector"},
            {"id": 108, "name": "Municipality Reporter", "type": "Reporter"},
            {"id": 109, "name": "Ward Reporter", "type": "Reporter"},
            {"id": 110, "name": "Municipality Monitor", "type": "Reporter"},
            {"id": 111, "name": "Ward Monitor", "type": "Reporter"},
            {"id": 112, "name": "General", "type": "General"},
            {"id": 113, "name": "Mobile User", "type": "General"},
        ]
        for item in groups:
            # print(item)
            Group.objects.get_or_create(name=item['name'], id=item['id'])
            self.stdout.write(self.style.SUCCESS("Group {} created successfully".format(item)))
        #
        for roles in UserRole.objects.all():
            print(roles.group.id)
            print(roles.group.name)
            print(roles.user)
        #     if roles.group.id == 1:
        #         print(True)
        #         roles.group_id = 104
        #         roles.save()
        #
        #     if roles.group.id == 5:
        #         print(True)
        #         roles.group_id = 112
        #         roles.save()
        #
        #     if roles.group.id == 6:
        #         print(True)
        #         roles.group_id = 113
        #         roles.save()
