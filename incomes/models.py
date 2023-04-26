


from django.db import models
from authentication.models import User

# Create your models here.


class Income(models.Model):
    SOURCE_OPTIONS = [
        ('SALARY', 'SALARY'),
        ('BUSINESS', 'BUSINESS'),
        ('SIDE-HUSTLES', 'SIDE-HUSTLES'),

        ('OTHERS', 'OTHERS'),
    ]
    source = models.CharField(choices=SOURCE_OPTIONS, max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    description = models.TextField(max_length=300)
    # who owns the models invidual owner has individual owner
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)

    class Meta:
        # defining how our datas need to be order by date and many more
        
        ordering = ["-date"]

    def __str__(self) -> str:
        return str(self.owner)+'s'+"income"
