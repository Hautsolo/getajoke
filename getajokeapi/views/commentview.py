from rest_framework import serializers, viewsets, permissions, status
from rest_framework.response import Response
from getajokeapi.models import Comment, User,Joke 
from django.shortcuts import get_object_or_404

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'created_at','joke']


class CommentViewSet(viewsets.ViewSet):
    """Comments view"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single comment"""
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all comments"""
        joke_id = request.query_params.get('joke_id', None)
        if joke_id is not None:
            comments = Comment.objects.filter(joke_id=joke_id)
        else:
            comments = Comment.objects.all()

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized comment instance
        """
        user = User.objects.get(pk=request.data["user_id"])
        joke = Joke.objects.get(pk=request.data['joke_id'])

        comment = Comment.objects.create(
            content = request.data["content"],
            user = user,
            joke = joke,
        )
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handle PUT requests to update a comment"""
        comment = get_object_or_404(Comment, pk=pk)
        comment.content = request.data.get("content", comment.content)
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """Handle DELETE requests to delete a comment"""
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
