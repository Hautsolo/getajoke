from rest_framework.response import Response
from rest_framework import serializers, viewsets, permissions, status
from getajokeapi.models import Joke, User, Tag, PostTag
from django.conf import settings
from django.db.models import Count
from rest_framework.decorators import api_view

# Serializer
class JokeSerializer(serializers.ModelSerializer):
    upvotes_count = serializers.IntegerField(source='upvotes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Joke
        fields = ['id', 'content', 'user', 'upvotes_count', 'comments_count', 'created_at', 'tags', 'user_id']
        depth = 2


class JokeViewSet(viewsets.ModelViewSet):
    # queryset = Joke.objects.all()
    # serializer_class = JokeSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)  # Changed 'request.user' to 'request.user'

    def retrieve(self, request, pk):
        try:
            joke = Joke.objects.annotate(comments_count=Count('comments')).get(pk=pk)  # Fixed typo 'comment_count'
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
            # Log incoming request data
            print(f"Request Data: {request.data}")

            # Retrieve the user based on the provided uid
            user = User.objects.get(uid=request.data["uid"])
            print(f"User Retrieved: {user}")

            # Create the Joke object
            joke = Joke.objects.create(
                user=user,  # Associate with the user
                content=request.data["content"]
            )
            print(f"Joke Created: {joke}")

            # Handle existing tags
            for tag_id in request.data.get("tags", []):
                tag = Tag.objects.get(pk=tag_id)
                PostTag.objects.create(joke=joke, tag=tag)
                print(f"Added Existing Tag: {tag}")

            # Handle new tags
            for tag_label in request.data.get("newTags", []):
                new_tag = Tag.objects.create(label=tag_label)
                PostTag.objects.create(joke=joke, tag=new_tag)
                print(f"Added New Tag: {new_tag}")

            # Serialize the Joke object to return the response
            serializer = JokeSerializer(joke)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error: {e}")  # Print the exception for debugging
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)



    def update(self, request, pk):
        joke = Joke.objects.get(pk=pk)

        joke.content = request.data["content"]
        joke.save()

        # Update tags
        PostTag.objects.filter(joke=joke).delete()  # Clear existing tags
        
        # Add new/existing tags
        for tag_id in request.data.get("tags", []):
            tag = Tag.objects.get(pk=tag_id)
            PostTag.objects.create(
                joke=joke,
                tag=tag
            )
        
        # Handling new tags
        new_tags = []
        for tag in request.data.get("newTags", []):
            new_tag = Tag.objects.create(
                label=tag
            )
            new_tags.append(new_tag)

        for tag in new_tags:
            PostTag.objects.create(
                joke=joke,
                tag=tag
            )

        serializer = JokeSerializer(joke)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        joke = Joke.objects.get(pk=pk)
        joke.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def upvote_joke(request, joke_id):
        try:
            joke = Joke.objects.get(id=joke_id)
            joke.upvotes_count += 1
            joke.save()
            return JsonResponse({'upvotes_count': joke.upvotes_count})
        except Joke.DoesNotExist:
            return JsonResponse({'error': 'Joke not found'}, status=404)
        
