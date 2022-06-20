from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
class HelloView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {'inster': 'email'}
        content = {'inster': 'password'}
        content = {'inster': 'username'}
        return Response(content)