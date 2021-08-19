from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from processingUrl.models import Urls
from processingUrl.serializer import BaseUrlSerializer
from services.urlGenerator import GeneratorShortUrl
from shortUrl.settings import env


class UrlView(APIView):
    @api_view(['POST'])
    def makeUrl(self):
        code = GeneratorShortUrl.getShortUrl()
        originalUrl = self.data['originalUrl']

        if 'https://' not in originalUrl and 'http://' not in originalUrl:
            return JsonResponse({"error": {"message": "Protocol is required"}}, status=400, safe=False)

        query_set = Urls.objects.all()
        allCodes = BaseUrlSerializer(query_set, many=True)
        codes = []
        for url in allCodes.data:
            codes.append(url['hash_url'])

        existCode = False
        if code in codes:
            existCode = True

        while existCode:
            code = GeneratorShortUrl.getShortUrl()
            if code not in codes:
                existCode = False

        hash_url = env('APP_URL') + code
        createdData = {
            'hash_url': code,
            'original_url': originalUrl

        }
        createUrl = BaseUrlSerializer(data=createdData, many=False)
        if createUrl.is_valid():
            createUrl.save()
            return JsonResponse({"data": {"hashUrl": hash_url, "originalUrl": originalUrl}}, status=200, safe=False)
        else:
            raise BaseException(message=createUrl.errors)

    @cache_page(60 * 10)
    @api_view(['GET'])
    def getUrl(self, link):
        try:
            query_set = Urls.objects.get(hash_url=link)
        except Urls.DoesNotExist:
            query_set = None

        existShortLink = BaseUrlSerializer(query_set, many=False).data

        if existShortLink is not None:
            return redirect(existShortLink['original_url'], 302)

        return JsonResponse({"data": {"message": "Short link not found"}}, status=404, safe=False)
