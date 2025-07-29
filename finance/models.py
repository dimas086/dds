from django.db import models
from django.core.exceptions import ValidationError

class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        unique_together = ['name', 'type']

    def __str__(self):
        return f"{self.name} ({self.type.name})"

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    class Meta:
        unique_together = ['name', 'category']

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class Transaction(models.Model):
    date = models.DateField(auto_now_add=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(blank=True, null=True)

    def clean(self):
        if self.subcategory.category != self.category:
            raise ValidationError("Подкатегория не соответствует выбранной категории.")
        if self.category.type != self.type:
            raise ValidationError("Категория не соответствует выбранному типу.")

    def __str__(self):
        return f"{self.date} - {self.amount} руб. ({self.category.name})"
