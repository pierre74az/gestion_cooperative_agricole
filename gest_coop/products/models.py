from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('seeds', 'Semences'),
        ('fertilizers', 'Engrais'),
        ('cereals', 'Céréales'),
        ('vegetables', 'Légumes'),
        
    )

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)

    specifications = models.TextField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    @classmethod
    def get_category_choices(cls):
        return cls.CATEGORY_CHOICES