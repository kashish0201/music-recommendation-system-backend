from django.shortcuts import render
from rest_framework import generics, permissions, status
from .serializers import SongSerializer, LikedSongSerializer
from .models import Song, Liked_song
from django.db.models import Q 
from rest_framework.response import Response

# import os
# from google.oauth2 import service_account
# from googleapiclient.discovery import build

# creds = service_account.Credentials.from_service_account_file(
#     'C:\\Users\\DELL\\Desktop\\be project\\auth\\music\\fifth-curve-382316-7b08a22495ae.json', scopes=['https://www.googleapis.com/auth/drive']
# )

class getSongByGenre(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = SongSerializer

    def get(self, request, music_genre):
        try:
            print(music_genre.capitalize())
            songs = Song.objects.filter(genre = music_genre.capitalize())
            
            data = []
            for song in songs:
                isLiked = len(Liked_song.objects.filter(user = request.user, song = song)) > 0
                data.append({
                    "name": song.name,
                    "url": song.audio_file,
                    "id": song.id,
                    "isLiked": isLiked
                })

            return Response({
                "songs": data
            }, status = status.HTTP_200_OK)
        except Exception as e:
            return Response ({
                "message": "Failed to fetch songs for " + music_genre,
                "error": str(e)
            }, status = status.HTTP_404_NOT_FOUND)
    

class getSongBySearch(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated)
    serializer_class = SongSerializer

    def get(self, request, search_query):
        songs = Song.objects.filter(Q(name__icontains= search_query))
        return songs
    
class LikeSong(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LikedSongSerializer

    def post(self, request):
        try:
            song = Song.objects.get(id = request.data['song'])
            user = request.user

            try:
                liked_song = Liked_song.objects.get(song = song, user = user)
            except:
                liked_song = None

            if liked_song:
                liked_song.delete()
                return Response({
                    "message" : "Song unliked",
                }, status = status.HTTP_200_OK)

            Liked_song.objects.create(song = song, user = user)
            return Response({
                "message" : "Song liked",
            }, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message" : "Song cannot be liked",
                "exception" : str(e),
            }, status = status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        try:
            user = request.user
            liked_songs_queryset = Liked_song.objects.filter(user = user)
            liked_songs = [q for q in liked_songs_queryset]
                        
            data = []

            for song in liked_songs:
                data.append({
                    "name": song.song.name,
                    "url": song.song.audio_file,
                    "id": song.song.id,
                    "isLiked": True
                })

            return Response({
                "songs" : data,
            }, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message" : "No Liked Songs FOund",
                "exception" : str(e),
            }, status = status.HTTP_404_NOT_FOUND)

            
class getAllGenre(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SongSerializer

    def get(self, request):
        try:
            queryset = Song.objects.order_by().values_list('genre').distinct()
            genres = [q[0] for q in queryset]
            return Response({
                "message" : genres,
            }, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": "Unauthorized Access",
                "exception": str(e)
            }, status = status.HTTP_401_UNAUTHORIZED)



# class UploadFiles(generics.GenericAPIView):
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = SongSerializer

#     def post(self, request):
#         # genre = request.genre

#         try:
#             # Set the ID of the folder you want to list files from
#             folder_id = '1i0tjXKuObKYi9j7LucKjuD-TE72THV80'

#             print(creds)
#             # Connect to the Drive API
#             service = build('drive', 'v3', credentials=creds)
#             print(service)

#             # Get a list of all files in the folder
#             results = service.files().list(q=f"'{folder_id}' in parents", fields="nextPageToken, files(id, name, webViewLink)").execute()
            
#             print(results)
#             items = results.get('files', [])

#             # Print out the file names and URLs
#             if not items:
#                 print('No files found.')
#             else:
#                 print("Blue")
#                 print('Files:')
#                 for item in items:
#                     Song.objects.create(audio_file=item["webViewLink"], name=item["name"], genre="Rock")
#                     print(f'{item["name"]} ({item["webViewLink"]})')
#         except Exception:
#             print('fatt gaya')

#         return Response({
#             "message" : "Song dekho",
#         }, status = status.HTTP_200_OK)
