from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField('gender', default='M', max_length=1)
    city = models.CharField('city', blank=True, max_length=64, default='Unknown')
    birthdate = models.DateField('birthdate', null=True)
    role = models.CharField('status', choices=(
        ('admin', 'Administrator'), ('user', 'User'), ('artist', 'Artist')), max_length=20,
                            default='User'
    )
    image = models.ImageField('image', upload_to='avatars/', null=True)

    def __str__(self):
        return str(User.username)

    @staticmethod
    def get_profile_by_id(user_id):
        profile = Profile.objects.get(user=user_id)
        if profile is None:
            profile = Profile(user=user_id)
            profile.save()
            return profile
        return profile

    @staticmethod
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @staticmethod
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class ArtistProfile(Profile):
    theme = models.CharField('theme', default='Nature', blank=True, max_length=64)
    picsuploaded = models.IntegerField('pictures_uploaded', default=1)
    messages = models.IntegerField('messages', default=1)
    style = models.CharField('style', default='Aerography', blank=True, max_length=64)

    def __str__(self):
        return str(User.username)


class Picture(models.Model):
    image = models.ImageField('image', upload_to='arts/', null=True)
    title = models.CharField('title', default='Some Awesome Picture', blank=True, max_length=64)
    uploaded_at = models.DateField('uploaded_at', auto_now_add=True, null=True)
    theme = models.CharField('theme', default='Nature', blank=True, max_length=64)
    ratecount = models.IntegerField('rate_count', default=0)
    style = models.CharField('style', default='Aerography', blank=True, max_length=64)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)


class News(models.Model):
    image = models.ImageField('image', upload_to='news/', null=True)
    title = models.CharField('title', default='Bla bla bla!', blank=True, max_length=100)
    text = models.CharField('text', default='bla bla bla', blank=True, max_length=500)
    expodate = models.DateField('expo_date', null=True)
    expotheme = models.CharField('expo_theme', default='Nature', blank=True, max_length=64)

    def __str__(self):
        return str(self.title)


class ENews(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)


class PhysNews(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    begintime = models.TimeField('begin_time')
    price = models.IntegerField('price', default=100)


class Message(models.Model):
    sender = models.ForeignKey(get_user_model(), related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(get_user_model(), related_name="receiver", on_delete=models.CASCADE)
    msg_content = models.TextField('message_content', blank=True, null=True)
    created_at = models.TimeField('created_at', null=True, auto_now_add=True)


def edit_profile(user_id, first_name, last_name, birthdate, city, role):
    user = User.objects.get(id=user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.profile.birthdate = birthdate
    user.profile.city = city
    user.profile.role = role
    user.save()


def change_avatar(user_id, image):
    user = User.objects.get(id=user_id)
    user.profile.image = image
    user.save()


def upload_image(user_id, title, theme, style, image):
    Picture.objects.create(title=title, theme=theme, style=style, image=image,
                           author=User.objects.get(id=user_id))


def send_message(sender_id, receiver, msg_content):
    Message.objects.create(sender=User.objects.get(id=sender_id), receiver=User.objects.get(username=receiver),
                           msg_content=msg_content)


def upload_news(image, title, text, expodate, expotheme):
    News.objects.create(image=image, title=title, text=text, expodate=expodate, expotheme=expotheme)
