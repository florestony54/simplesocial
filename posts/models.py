from django.db import models
from django.urls import reverse
from django.conf import settings

import misaka
from django.utils import timezone
from groups.models import Group

from django.contrib.auth import get_user_model
User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name='posts',
                                null=True, blank=True,
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def approve_comments(self):
        return self.comments.filter(approved_comments=True)

    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username':self.user.username,
                                                'pk':self.pk})

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'message']

###########################################################
#COMMENTS TODO: MAKE A VIEW FOR COMMENTS
###########################################################

class Comment(models.Model):
    post = models.ForeignKey('posts.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list') #after comment submitted, return to list of posts
                                    #maybe change to return to post that was commented on instead

    def __str__(self):
        return self.text
