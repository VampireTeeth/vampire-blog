import unittest, mongoengine, datetime, models



MODELS = [models.Article, models.User, models.Comment]
class BaseTest(unittest.TestCase):

    def setUp(self):
        mongoengine.connect('vampire-blog-test')

    def tearDown(self):
        for model in MODELS: model.objects().delete()

class ArticleTest(BaseTest):

    def testSave(self):
        u = models.User(first_name='Steven', last_name='Liu', email='steven.weike.liu@gmail.com')
        u.save()
        users = models.User.objects(first_name='Steven')
        for u in users:
            self.assertEqual(u.first_name, 'Steven')

        b = models.Article(dateTime=datetime.datetime.now(),
                title='First Article',
                content='This is a sample blog content',
                author=u)
        b.save()

        bs = models.Article.objects(author=u)

        for b in bs:
            self.assertEqual(b.author.first_name, 'Steven')
            self.assertEqual(b.content, 'This is a sample blog content')

    def testSaveWithNonRequiredFieldsOnly(self):
        u = models.User(first_name='Steven', last_name='Liu', email='steven.weike.liu@gmail.com')
        u.save()

        b = models.Article(title='Title',author=u)
        b.save()
        bs = models.Article.objects(author=u)

        for b in bs:
            self.assertEqual(b.author.first_name, 'Steven')
            self.assertEqual(b.content, None)

    def testSaveManyBlogsWithSameUser(self):
        u = models.User(first_name='Steven', last_name='Liu', email='steven.weike.liu@gmail.com')
        u.save()

        b1 = models.Article(author=u, title='AAd', content='Blog1')
        b2 = models.Article(author=u, title='another', content='Blog2')

        b1.save()
        b2.save()

        bs = models.Article.objects(author=u)
        self.assertEqual(2, len(bs))


        for b in bs:
            self.assertIn(b.content, ['Blog1', 'Blog2'])

class CommentTest(BaseTest):
    def testSave(self):
        content = 'haha this is a stupid comment'
        c = models.Comment(content=content)
        c.save()

        comments = models.Comment.objects(content=content)
        self.assertEqual(1, len(comments))
        self.assertEqual(content, comments[0].content)

