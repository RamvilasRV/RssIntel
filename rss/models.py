from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class RssFeed(models.Model):
	url = models.URLField(max_length=200)  # Stores the RSS Feed URL
	title = models.CharField(max_length=255)  # Stores the title for the field (parsed)
	description = models.TextField(blank=True, null=True)  # Stores the description of the feed (parsed)
	author = models.CharField(max_length=50,blank=True, null=True ) # Stores the author of the field
	logo = models.URLField(max_length=200, blank=True, null=True)  # Optional: Store an image URL for the feed (parsed, user enterd)
	category = models.CharField(max_length=100, blank=True, null=True)  # Optional: Store the category of the feed
	public = models.BooleanField(default=False)  # Flag to indicate if the feed should be made public 
	custom = models.BooleanField(default=True)  # Flag to indicate if the feed is custom (1 if given by the user)

	def __str__(self):
		return self.title


class Subscriptions(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key to Django's User model
	rss_feed = models.ForeignKey(RssFeed, on_delete=models.CASCADE)  # Foreign key to RssFeed table
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('user', 'rss_feed')  # Keeping the pair unique so that a user cant subscribe to it more than once

	def __str__(self):
		return f"{self.user.username} subscribed to {self.RssFeed.title}"


"""
	Published date will be displayed on the page and will not be stored on the database
	No point in storing the refreshed time, since the page will be refreshed everytime the rss is opend.
"""
