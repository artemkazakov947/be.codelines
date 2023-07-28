from django.template.defaultfilters import slugify
from django.test import TestCase
from django.urls import reverse

from apps.website.forms import EmailPostNotificationForm, RequestFromUserForm
from apps.website.models import Role, Employee, Job, Skill, Case, EmailForPostNotification, RequestFromUser


class TestModel(TestCase):
    def test_employee(self):
        role = Role.objects.create(name="test_role")
        first_name = "Test first"
        last_name = "Last test"

        employee = Employee.objects.create(
            first_name=first_name,
            last_name=last_name,
            role=role,
        )

        self.assertEqual(str(employee), f"{employee.first_name} {employee.last_name} ({employee.role.name})")

    def test_get_absolute_url_for_job(self):
        skill = Skill.objects.create(name="test_skill")
        job = Job.objects.create(
            name="Test_name",
            description="Test description"
        )
        job.skill.add(skill)
        slug_name = slugify(job.name)

        self.assertEqual(job.get_absolute_url(), f"/jobs/{slug_name}/")

    def test_case_get_two_random_obj(self):
        case_num = 10
        for i in range(case_num):
            Case.objects.create(
                name=f"Case_name # {i}",
                company=f"Company # {i}",
                briefing=f"Briefing # {i}",
                result=f"Result # {i}",
            )

        self.assertEqual(len(Case.get_two_random_obj()), 2)


class TestForm(TestCase):
    def test_email_post_notification(self):
        form_data = {
            "email": "test@test.com"
        }
        form = EmailPostNotificationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_request_from_user_form(self):
        form_data = {
            "full_name": "Test Full",
            "email": "test@test.com",
            "phone_number": "+380506152456",
            "question": "Test question"
        }
        form = RequestFromUserForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class TestView(TestCase):

    def test_create_email_for_post_notification(self):
        form_data = {
            "email": "test@test.com"
        }
        self.client.post(reverse("website:email-notification"), data=form_data)
        new_email = EmailForPostNotification.objects.get(email=form_data["email"])

        self.assertTrue(EmailForPostNotification.objects.filter(email=new_email.email).exists())
        self.assertEqual(new_email.email, form_data["email"])

    def test_create_request_from_user(self):
        form_data = {
            "full_name": "Test Full",
            "email": "test@test.com",
            "phone_number": "+32479269sdc534",
            "question": "Test question",
            "privacy": True
        }

        response = self.client.post(reverse("website:request-from-user"), data=form_data)
        new_question = RequestFromUser.objects.filter(email=form_data["email"])

        self.assertTrue(new_question.exists())
        self.assertEqual(response.status_code, 302)

        new_question = RequestFromUser.objects.get(full_name=form_data["full_name"])

        self.assertEqual(new_question.full_name, form_data["full_name"])
        self.assertEqual(new_question.email, form_data["email"])
        self.assertEqual(new_question.phone_number, form_data["phone_number"])
        self.assertEqual(new_question.question, form_data["question"])
