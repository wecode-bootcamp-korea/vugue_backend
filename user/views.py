import json
import bcrypt
import jwt

from vugue.settings         import SECRET_KEY
from django.views           import View
from django.http            import JsonResponse, HttpResponse

from .models                import User
from user.utils             import login_decorator

class UserView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if len(data['password']) < 5:
                return JsonResponse({'message':'SHORT_PASSWORD'}, status = 400)

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            if User.objects.filter(name=data['name']).exists():
                return JsonResponse({'message': 'NAME_ALREADY_EXIST'}, status=400)

            User(
                    name = data['name'],
                    password = hashed_password.decode('utf-8')
                ).save()

            return HttpResponse(status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEYS'}, status=400)
        
        except TypeError:
            return JsonResponse({'message' : 'WRONG_INPUT_VALUE'}, status=400)


class AuthView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            user = User.objects.get(name = data['name'])
            if bcrypt.checkpw(data['password'].encode('utf-8'),user.password.encode('utf-8')):
                access_token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm = 'HS256')
                return JsonResponse({'access_token': access_token.decode('utf-8')}, status=200)

            else:
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status=401)

        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=400)

        except TypeError:
            return JsonResponse({'message':'WRONG_INPUT_VALUE'}, status=400)

