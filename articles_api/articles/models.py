from django.db import models


# create a model for persistence
class Articles(models.Model):
    # author
    author = models.CharField(max_length=255, null=False)
    # article title
    title = models.CharField(max_length=255, null=False)

    def __str__(self):
        return '{} : {}'.format(self.title, self.author)
