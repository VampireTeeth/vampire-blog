import unittest, mongoengine, datetime, models

class BlogTest(unittest.TestCase):

    def setUp(self):
        mongoengine.connect('vampire-blog-test')

    def tearDown(self):
        models.Blog.objects().delete()
        models.User.objects().delete()


    def testSave(self):
        u = models.User(first_name='Steven', last_name='Liu', email='steven.weike.liu@gmail.com')
        u.save()
        users = models.User.objects(first_name='Steven')
        for u in users:
            self.assertEqual(u.first_name, 'Steven')

        b = models.Blog(dateTime=datetime.datetime.now(),
                content='This is a sample blog content',
                author=u)
        b.save()

        bs = models.Blog.objects(author=u)

        for b in bs:
            self.assertEqual(b.author.first_name, 'Steven')
            self.assertEqual(b.content, 'This is a sample blog content')

