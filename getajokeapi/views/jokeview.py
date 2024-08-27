from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, viewsets, status
from getajokeapi.models import Joke, User, Tag, PostTag
from django.db.models import Count

# Serializer
class JokeSerializer(serializers.ModelSerializer):
    upvotes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Joke
        fields = ['id', 'content', 'user', 'upvotes_count', 'comments_count', 'created_at', 'tags', 'user_id']
        depth = 2
        

class JokeViewSet(viewsets.ModelViewSet):
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

    def retrieve(self, request, pk=None):
        try:
            joke = Joke.objects.annotate(comments_count=Count('comments')).get(pk=pk)
            serializer = JokeSerializer(joke)
            return Response(serializer.data)
        except Joke.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        try:
            user = request.query_params.get('uid', None)
            if user is not None:
                user_id = User.objects.get(uid=user)
                jokes = Joke.objects.filter(user=user_id).annotate(comments_count=Count('comments'))
            else:
                jokes = Joke.objects.annotate(comments_count=Count('comments')).all()

            serializer = JokeSerializer(jokes, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        try:
            user = User.objects.get(uid=request.data["uid"])
            joke = Joke.objects.create(
                user=user,
                content=request.data["content"]
            )

            for tag_id in request.data.get("tags", []):
                tag = Tag.objects.get(pk=tag_id)
                PostTag.objects.create(joke=joke, tag=tag)

            for tag_label in request.data.get("newTags", []):
                new_tag = Tag.objects.create(label=tag_label)
                PostTag.objects.create(joke=joke, tag=new_tag)

            serializer = JokeSerializer(joke)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def upvote(self, request, pk=None):
        try:
            joke = self.get_object()
            joke.upvote()  # Increment the upvote count
            serializer = JokeSerializer(joke)
            return Response({
                'status': 'joke upvoted',
                'upvotes_count': serializer.data['upvotes_count']
            }, status=status.HTTP_200_OK)
        except Joke.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Joke not found'
            }, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            joke = Joke.objects.get(pk=pk)
            joke.content = request.data["content"]
            joke.save()

            PostTag.objects.filter(joke=joke).delete()
            
            for tag_id in request.data.get("tags", []):
                tag = Tag.objects.get(pk=tag_id)
                PostTag.objects.create(joke=joke, tag=tag)
            
            new_tags = []
            for tag in request.data.get("newTags", []):
                new_tag = Tag.objects.create(label=tag)
                new_tags.append(new_tag)

            for tag in new_tags:
                PostTag.objects.create(joke=joke, tag=tag)

            serializer = JokeSerializer(joke)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Joke.DoesNotExist:
            return Response({'error': 'Joke not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            joke = Joke.objects.get(pk=pk)
            joke.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Joke.DoesNotExist:
            return Response({'error': 'Joke not found'}, status=status.HTTP_404_NOT_FOUND)
