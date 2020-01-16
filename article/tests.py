import json
import datetime

from django.test       import TestCase
from django.test       import Client
from django.utils      import timezone

from .models    import *

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

        Categories.objects.create(
            id =3,
            name = 'living'
        )

        Tags.objects.create(
            id =1,
            name = 'trend'
        )
        Tags.objects.create(
            id =2,
            name = 'shopping'
        )

        Tags.objects.create(
            id =12,
            name = 'ppl'
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

        ArticleDetails.objects.create(
            id =3,
            title = 'BEAUTY NEW YEAR',
            caption_date = '2020.01.07',
            description = 'beautiful'
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

        Articles.objects.create(
            id =3,
            title = 'BEAUTY NEW YEAR',
            image_url = 'http://img.vogue.co.kr/vogue/2020/01/style_5e129975d71d0.jpg',
            caption = 'BEAUTY NEW YEAR',
            created_date = datetime.datetime.strptime("2020-01-07 22:24:00", "%Y-%m-%d %H:%M:%S"),
            article_detail = ArticleDetails.objects.get(id=3)
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

        CategoryTagArticles.objects.create(
            article = Articles.objects.get(id=3),
            category = Categories.objects.get(id=3),
            tag = Tags.objects.get(id=12)
        )

    def tearDown(self):
        Categories.objects.all().delete()
        Tags.objects.all().delete()
        ArticleDetails.objects.all().delete()
        Articles.objects.all().delete()
        CategoryTagArticles.objects.all().delete()
    
    def test_categoryview(self):
        client = Client()
        response = client.get('/article/category')
        self.assertEqual(response.status_code, 200)

    def test_tagview(self):
        client= Client()
        response = client.get('/article/tag')
        self.assertEqual(response.status_code, 200)

    def test_ArticleView(self):
        client = Client()

        response = client.get('/article/1')
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

        response = client.get('/article/1?tag_id=1&offset=hi')
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

    def test_MainView(self):
        client = Client()

        response = client.get('/article/main')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'data': [{
                'detail_id': 3,
                'image_url': 'http://img.vogue.co.kr/vogue/2020/01/style_5e129975d71d0.jpg',
                'title': 'BEAUTY NEW YEAR'
            }]
        })

    def test_MainViewFail(self):
        client = Client()

        response = client.get('/article/main/1')
        self.assertEqual(response.status_code, 404)

    def test_MainViewException(self):
        client = Client()

        response = client.get('/article/main?limit=hi')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"INVALID_VALUE"})

class VideoTest(TestCase):
    client = Client()
    def setUp(self):
        category = Categories.objects.create(
            id   = 1,    
            name = 'Video',
        )
        Video.objects.create(
            id = 1,    
            content = "지방시의 새로운 2019 가을/겨울 컬렉션 광고 캠페인을 지금 만나보세요",
            title = "Givenchy 2019 Fall Winter",
            video_url = "https://player.vimeo.com/video/359012485?api=1&player_id=player1",
            background_image = "http://img.vogue.co.kr/vogue/2019/09/style_5d722bdc058d0-400x305.jpg",
            category = category
        )

    def tearDown(self):
        Video.objects.get(id=1).delete()

    def test_video_view(self):
        client = Client()
        response = client.get('/article/video')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {
                'id': 1,
                'title': 'Givenchy 2019 Fall Winter',
                'background_image': 'http://img.vogue.co.kr/vogue/2019/09/style_5d722bdc058d0-400x305.jpg'
                }
            ]
        )

    def test_video_details(self):
        client = Client()
        response = client.get('/article/video/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'id': 1, 
            'title': 'Givenchy 2019 Fall Winter', 
            'background_image': 'http://img.vogue.co.kr/vogue/2019/09/style_5d722bdc058d0-400x305.jpg', 
            'category': 'Video', 
            'video_url': 'https://player.vimeo.com/video/359012485?api=1&player_id=player1', 
            'content': '지방시의 새로운 2019 가을/겨울 컬렉션 광고 캠페인을 지금 만나보세요'
            }
        )

    def test_video_exception(self):
        client = Client()
        response = client.get('/article/video/2')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message':'ARTICLE_NOT_FOUND'})
