import os

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone


class Employee(models.Model):
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    gender = models.CharField(
        "Пол", max_length=10, choices=[("M", "Мужской"), ("F", "Женский")]
    )
    skills = models.TextField("Навыки", blank=True)
    hire_date = models.DateField("Дата приема", default=timezone.now)
    desk_number = models.PositiveIntegerField("Номер стола", null=True, blank=True)
    role = models.CharField(
        "Должность",
        max_length=20,
        choices=[
            ("QA", "Тестировщик"),
            ("BACK", "Бекенд-разработчик"),
            ("FRONT", "Фронтенд-разработчик"),
        ],
        default="QA",
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def tenure_days(self):
        if self.hire_date:
            return (timezone.now().date() - self.hire_date).days
        return 0

    @property
    def first_image(self):
        return self.images.first()

    def clean(self):
        super().clean()
        if self.desk_number is not None:
            adjacent_desks = [self.desk_number - 1, self.desk_number + 1]
            neighbors = Employee.objects.filter(desk_number__in=adjacent_desks).exclude(
                pk=self.pk
            )

            for neighbor in neighbors:
                is_self_qa = self.role == "QA"
                is_neighbor_qa = neighbor.role == "QA"
                if is_self_qa != is_neighbor_qa:
                    raise ValidationError(
                        f"Тестировщики и разработчики не могут сидеть за соседними столами. "
                        f"За столом {neighbor.desk_number} уже сидит {neighbor.get_role_display()}."
                    )


class EmployeeImage(models.Model):
    employee = models.ForeignKey(
        Employee, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField("Изображение", upload_to="employees/")
    order = models.PositiveIntegerField(
        "Порядковый номер", default=0, blank=True, null=True
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Фото {self.order} для {self.employee}"


@receiver(post_delete, sender=EmployeeImage)
def delete_employee_image_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
