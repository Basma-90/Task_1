from django.db import models
class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=280)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=100)

    def __str__(self):
        return self.name
