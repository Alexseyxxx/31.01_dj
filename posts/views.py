import logging
from django.views import View
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from posts.models import Posts


logger = logging.getLogger()


class PostsView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        posts: QuerySet[Posts]= Posts.objects.all()
        if not posts:
            return render(request=request, template_name= "posts.html", 
                          status=404
                          )
        return render(request=request, template_name="posts.html",
                      context={"posts":posts}
                       )

    def post(self, request: HttpRequest) -> HttpResponse:
        pass

    def put(self, request: HttpRequest) -> HttpResponse:
        pass

    def patch(self, request: HttpRequest) -> HttpResponse:
        pass

    def delete(self, request: HttpRequest) -> HttpResponse:
        pass

