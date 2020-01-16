import json
import datetime

from django.test       import TestCase
from django.test       import Client
from django.utils      import timezone

from article.models    import *

class MyCalcTest(TestCase):
    def setUp(self):
        client = Client()

        Categories.objects.create(
            id =1,
            name = 'fashion'
        )

        Categories.objects.create(
            id =2,
            name = 'beauty'
        )

        Tags.objects.create(
            id =1,
            name = 'trend'
        )
        Tags.objects.create(
            id =2,
            name = 'shopping'
        )

        ArticleDetails.objects.create(
            id = 1,
            title = 'WOMAN WITH A PLAN',
            caption_date = '2020.01.08',
            description = 'good'
        )

        ArticleDetails.objects.create(
            id =2,
            title = 'RESHAPE THE FUTURE',
            caption_date = '2020.01.07',
            description = 'looks good'
        )

        t1 = datetime.datetime.strptime("2020-01-01 22:24:00", "%Y-%m-%d %H:%M:%S")

        Articles.objects.create(
            id =1,
            title = 'RESHAPE THE FUTURE',
            image_url = 'http://img.vogue.co.kr/vogue/2019/12/style_5dfc71ea05818-600x900.jpg',
            caption = 'Plan C’의 디자이너 카롤리나 카스틸리오니',
            created_date = datetime.datetime.strptime("2020-01-01 22:24:00", "%Y-%m-%d %H:%M:%S"),
            article_detail = ArticleDetails.objects.get(id=1)
        )

        Articles.objects.create(
            id =2,
            title = 'WOMAN WITH A PLAN',
            image_url = 'http://img.vogue.co.kr/vogue/2019/12/style_5dfc5cab87d49-600x900.jpg',
            caption = '2020년대 패션 생태계에서 가장 유효한 가치',
            created_date = datetime.datetime.strptime("2020-01-07 22:24:00", "%Y-%m-%d %H:%M:%S"),
            article_detail = ArticleDetails.objects.get(id=2)
        )

        CategoryTagArticles.objects.create(
            article = Articles.objects.get(id=1),
            category = Categories.objects.get(id=1),
            tag = Tags.objects.get(id=1)
        )

        CategoryTagArticles.objects.create(
            article = Articles.objects.get(id=2),
            category = Categories.objects.get(id=2),
            tag = Tags.objects.get(id=2)
        )

    def tearDown(self):
        Categories.objects.all().delete()
        Tags.objects.all().delete()
        ArticleDetails.objects.all().delete()
        Articles.objects.all().delete()
        CategoryTagArticles.objects.all().delete()

    def test_ArticleView(self):
        client = Client()

        response = client.get('/article/articles/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'data': [{
                'title': 'RESHAPE THE FUTURE',
                'image_url': 'http://img.vogue.co.kr/vogue/2019/12/style_5dfc71ea05818-600x900.jpg',
                'detail_id': 1
            }]
        })

    def test_ArticleViewException(self):
        client = Client()

        response = client.get('/article/articles/1?tag_id=1&offset=hi')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"INVALID_VALUE"})

    def test_SearchView(self):
        client = Client()

        response = client.get('/article/search?keyword=RESHAPE')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'data': [{
                'detail_id': 1,
                'image_url': 'http://img.vogue.co.kr/vogue/2019/12/style_5dfc71ea05818-600x900.jpg',
                'title': 'RESHAPE THE FUTURE'
            }]
        })
    
    def test_DetailView(self):
        client = Client()

        response = client.get('/article/details/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'detail': [{
                'title': 'WOMAN WITH A PLAN',
                'caption_date': '2020.01.08',
                'description': 'good'
            }],
            'article_list': [{
                'title': 'RESHAPE THE FUTURE',
                'caption_date': '',
                'image_url': 'http://img.vogue.co.kr/vogue/2019/12/style_5dfc71ea05818-600x900.jpg',
                'caption': 'Plan C’의 디자이너 카롤리나 카스틸리오니',
                'detail_id': 1
            }]
        })

    def test_SearchFail(self):
        client = Client()

        response = client.get('/article/search/')
        self.assertEqual(response.status_code, 404)

    def test_DetailViewFail(self):
        client = Client()

        response = client.get('/article/details')
        self.assertEqual(response.status_code, 404)

    def test_DetailViewException(self):
        client = Client()

        response = client.get('/article/details/100')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"message":"INVALID_ID"})
