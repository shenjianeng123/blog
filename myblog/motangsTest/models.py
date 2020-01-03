from django.db import models
# from datetime import date,time,timezone
from django.utils import timezone
from django.contrib.auth.models import User

from django.urls import reverse

from taggit.managers import TaggableManager

# Create your models here.



class PublishedManager(models.Manager):
    
    def get_queryset(self):
        # draft
        return super(PublishedManager,self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (('draft','Dratf'),('published','Published'))
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    author = models.ForeignKey(User,on_delete = models.CASCADE,related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default ='draft')
    
    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):

        return self.title

    ########
    objects = models.Manager() 

    published  = PublishedManager() # 自定义(生成过滤器前面的就是管理器)

    tags = TaggableManager()

    #########
    def get_absolute_url(self):

        return reverse('MoTangSblog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
    def __str__(self):

         return 'Comment by {} on {}'.format(self.name, self.post)

        
        






