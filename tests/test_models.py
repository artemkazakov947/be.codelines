# from unittest import TestCase
# from apps.website.models import Role, Employee
#
#
# class TestModel(TestCase):
#     def test_employee(self):
#         role = Role.objects.create(name="test_role")
#         first_name = "Test first"
#         last_name = "Last test"
#
#         employee = Employee.objects.create(
#             first_name=first_name,
#             last_name=last_name,
#             role=role,
#         )
#
#         self.assertEqual(str(employee), f"{employee.first_name} {employee.last_name} ({employee.role.name})")
