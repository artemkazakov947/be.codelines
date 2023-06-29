import os

from django.db import models


def team_foto_file_path(instance, filename: str):
    _, extension = os.path.splitext(filename)

    file = f"{instance.first_name}_{instance.last_name}.{extension}"

    return os.path.join("uploads/team/", file)


class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.ForeignKey(
        Role, on_delete=models.SET_DEFAULT, related_name="employees", default="member"
    )
    foto = models.ImageField(upload_to=team_foto_file_path)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role.name})"
