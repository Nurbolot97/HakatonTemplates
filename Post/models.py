from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone



class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    body = models.TextField(db_index=True, blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    slug = models.SlugField(max_length=150, unique=True)
    date_pub = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='post')

    class Meta:
        ordering = ('-date_pub',)


    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
    

    def __str__(self):
        return f"{self.title} by {self.author}"

        

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, 
                                    related_name="comments_posts",
                                    blank=True, null=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, 
                                        related_name='users_comments',
                                       blank=True, null=True)

    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)


    class Meta:
        ordering = ('created_date',)

    def __str__(self):  
        return f"Comment by {self.author} on {self.post}"


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)



    def get_absolute_url(self):
        return reverse('tag_detail', kwargs={'slug': self.slug})


    def __str__(self):
        return f"{self.title}"

