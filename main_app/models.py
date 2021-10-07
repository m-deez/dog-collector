from django.db import models

class Dog(models.Model):

    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    img = models.CharField(max_length=250)
    bio = models.TextField(max_length=500)
    verified_doggo = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Collar(models.Model):

    brand = models.CharField(max_length=150)
    length = models.IntegerField(default=0)
    color = models.CharField(max_length=100)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name="collars")

    def __str__(self):
        return self.brand

class Walker(models.Model):

    name = models.CharField(max_length=150)
    dog = models.ManyToManyField(Dog)

    def __str__(self):
        return self.name