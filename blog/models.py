from django.conf import settings
from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    text = models.TextField()    
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
    	return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title

def get_image_filename(instance, filename):
    post_id = instance.post.id

    return "post_images/%s/%s" % (post_id, filename) 

class Images(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_image_filename,
                              verbose_name='Image')

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text