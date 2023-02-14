from django.db import models


class Album(models.Model):
    album_name = models.CharField("Album Name", max_length=100)
    artist = models.CharField(max_length=100)


class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks',
                              on_delete=models.CASCADE)
    order = models.IntegerField(help_text="The order of the track")
    title = models.CharField(max_length=100)
    duration = models.IntegerField()

    class Meta:
        unique_together = ('album', 'order')
        ordering = ['order']

    def __str__(self):
        return '%d: %s' % (self.order, self.title)
