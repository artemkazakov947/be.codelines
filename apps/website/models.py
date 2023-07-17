import random

from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from phonenumber_field.modelfields import PhoneNumberField
from taggit.managers import TaggableManager

from base.helpers import team_foto_file_path, case_file_path


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
    content = RichTextUploadingField()
    created = models.DateField(auto_now_add=True)
    time_to_read = models.IntegerField()
    slug = models.SlugField(blank=True, unique=True)
    tag = TaggableManager()

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def send_new_post_notification(self) -> None:
        emails = [email.email for email in EmailForPostNotification.objects.all()]
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject=self.title, message=self.content, from_email=email_from, recipient_list=emails)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.slug:
            self.slug = slugify(self.title)
        self.send_new_post_notification()
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def get_absolute_url(self):
        return reverse_lazy("website:post-detail", kwargs={"slug": self.slug})


class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = RichTextUploadingField()

    def __str__(self):
        return self.name


class EmailForPostNotification(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class RequestFromUser(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    question = models.TextField()
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"Question from {self.full_name} from {self.created}"

    def send_users_request_to_admin(self) -> None:
        email = settings.EMAIL_HOST_USER
        email_from = self.email
        message = f"name: {self.full_name}, \n " \
                  f"contact: {(self.email, self.phone_number.national_number)}, \n " \
                  f"question: {self.question}"
        send_mail(subject=str(self), message=message, from_email=email_from, recipient_list=[email])

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.send_users_request_to_admin()
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class Case(models.Model):
    name = models.CharField(max_length=255, unique=True)
    company = models.CharField(max_length=255)
    briefing = RichTextUploadingField()
    result = RichTextUploadingField()
    cover = models.ImageField(upload_to=case_file_path)
    slug = models.SlugField(default="default_slug")
    # product = models.ForeignKey() TODO: implement product model

    def __str__(self):
        return self.name

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def get_absolute_url(self):
        return reverse_lazy("website:case-detail", kwargs={"slug": self.slug})

    @staticmethod
    def get_two_random_obj():
        return random.sample(list(Case.objects.all()), 2)
