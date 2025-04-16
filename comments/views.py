from django.views import View
from django.http import HttpRequest, HttpResponse
from posts.models import Posts
from .models import Comment
from django.http import JsonResponse

class CreateCommentView(View):
    def post(self, request: HttpRequest, post_id: int) -> HttpResponse:
        if not request.user.is_authenticated:
            return HttpResponse("Unauthorized", status=401)

        comment_text = request.POST.get("comment")
        parent_id = request.POST.get("parent_comment")

        if not comment_text:
            return HttpResponse("Comment text is required", status=400)

        try:
            post = Posts.objects.get(id=post_id)
        except Posts.DoesNotExist:
            return HttpResponse("Post not found", status=404)

        try:
            parent_comment = Comment.objects.get(id=parent_id) if parent_id else None
        except Comment.DoesNotExist:
            parent_comment = None

        new_comment = Comment.objects.create(
            author=request.user,
            post=post,
            text=comment_text,
            parent_comment=parent_comment  
        )

        return HttpResponse(f"Comment created with ID {new_comment.id}", status=201)
    
class LikeCommentView(View):
    def post(self, request, comment_id):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        comment = Comment.objects.get(id=comment_id)
        comment.likes += 1
        comment.save()
        return JsonResponse({'likes': comment.likes})


class DislikeCommentView(View):
    def post(self, request, comment_id):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        comment = Comment.objects.get(id=comment_id)
        comment.dislikes += 1
        comment.save()
        return JsonResponse({'dislikes': comment.dislikes})