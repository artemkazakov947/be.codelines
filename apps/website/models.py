import os

from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from taggit.managers import TaggableManager


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


class Skill(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Job(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    skill = models.ManyToManyField(Skill, related_name="jobs")
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.name

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def get_absolute_url(self):
        return reverse_lazy("website:job-detail", kwargs={"slug": self.slug})


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    created = models.DateField(auto_now_add=True)
    time_to_read = models.IntegerField()
    slug = models.SlugField(blank=True, unique=True)
    tag = TaggableManager()

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def get_absolute_url(self):
        return reverse_lazy("website:post-detail", kwargs={"slug": self.slug})
