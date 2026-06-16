from django.db import models

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=250)
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date', '-updated_date']
        db_table = 'category'


class Post(models.Model):
    author = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    category = models.ForeignKey("Category", models.CASCADE)
    content = models.TextField()
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date', '-updated_date']
        db_table = 'post'
