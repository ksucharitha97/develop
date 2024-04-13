from django.db import models

# Create your models here.
class Student(models.Model):
    title = models.CharField(max_length =50)
    fname = models.CharField(max_length=10)
    lname = models.CharField(max_length=21)
    email = models.EmailField(max_length=12)
    def __str__(self):
       return self.title_name() 

class Category(models.Model):
    name = models.CharField(default='uncategorized',max_length=100)
    is_activate = models.BooleanField(default=True)    
    def __str__(self):
        return self.name()    

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'



class Product(models.Model):
    Category= models.ForeignKey(Category,on_delete=models.CASCADE,related_name = 'catgeories')
    product_name = models.CharField(max_length=120)
    desc = models.TextField()
    created_date = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.title_name()
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Product'
        verbose_name_plural = 'Products'