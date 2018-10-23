from django.test import TestCase
from django.contrib.auth.models import User
from .models import *


# Create your tests here.

# Create your tests here.

class UserTest(TestCase):
    def setUp(self):
        self.user = User(username='slim', first_name='slim', last_name='leskey', email='slimleskey@gmail.com')

    def test_instance(self):
        self.assertTrue(isinstance(self.user, User))

    def test_data(self):
        self.assertTrue(self.user.username, "slim")
        self.assertTrue(self.user.first_name, "slim")
        self.assertTrue(self.user.last_name, 'leskey')
        self.assertTrue(self.user.email, 'slimleskey@gmail.com')

    def test_save(self):
        self.user.save()
        users = User.objects.all()
        self.assertTrue(len(users) > 0)

    def test_delete(self):
        user = User.objects.filter(id=1)
        user.delete()
        users = User.objects.all()
        self.assertTrue(len(users) == 0)


class ProfileTest(TestCase):
    def setUp(self):
        self.new_user = User(username='aa', first_name='a', last_name='a', email='a@gmail.com')
        self.new_user.save()
        self.new_profile = Profile(user=self.new_user, contact="123456789", bio='yoyo')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_profile, Profile))

    def test_data(self):
        self.assertTrue(self.new_profile.bio, "wuehh")
        self.assertTrue(self.new_profile.user, self.new_user)

    def test_save(self):
        self.new_profile.save()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) > 0)

    def test_delete(self):
        profile = Profile.objects.filter(id=1)
        profile.delete()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) == 0)

    def test_edit_profile(self):
        self.new_profile.save()
        self.update_profile = Profile.objects.filter(bio='wueh').update(bio='aaabbbcccddd')
        self.updated_profile = Profile.objects.get(bio='aaabbbcccddd')
        self.assertTrue(self.updated_profile.bio, 'aaabbbcccddd')


class projectsTest(TestCase):
    def setUp(self):
        self.user = User(username='slim', first_name='slim', last_name='leskey', email='slimleskey@gmail.com')
        self.user.save()
        self.new_profile = Profile(user=self.user, contact="123456789", bio='wueh')
        self.new_profile.save()
        self.new_post = Projects(user=self.user, link="https://www.google.com")

    def test_instance(self):
        self.assertTrue(isinstance(self.new_post, Projects))

    def test_data(self):
        self.assertTrue(self.new_post.link, "https://www.google.com")

    def test_save(self):
        self.new_post.save()
        posts = Projects.objects.all()
        self.assertTrue(len(posts) > 0)

    def test_delete(self):
        post = Projects.objects.filter(id=1)
        post.delete()
        posts = Projects.objects.all()
        self.assertTrue(len(posts) == 0)

    def test_update_post(self):
        self.new_post.save()
        self.update_post = Projects.objects.filter(link='https://www.google.com').update(link='https://www.instadk.com')
        self.updated_post = Projects.objects.get(link='https://www.instadk.com')
        self.assertTrue(self.updated_post.link, 'https://www.instadk.com')



class CommentTest(TestCase):
    def setUp(self):
        self.new_user = User(username='aa', first_name='a', last_name='a', email='a@gmail.com')
        self.new_user.save()
        self.new_profile = Profile(user=self.new_user, contact="123456789", bio='wueh')
        self.new_profile.save()
        self.new_post = Projects(user=self.new_user, link='https://www.google.com')
        self.new_post.save()
        self.comment = Comments(user=self.new_user, post=self.new_post, comment='good')

    def test_instance(self):
        self.assertTrue(isinstance(self.comment, Comments))

    def test_data(self):
        self.assertTrue(self.comment.comment, "good")

    def test_comments(self):
        self.comment.save()
        comments = Comments.objects.all()
        self.assertTrue(len(comments) > 0)