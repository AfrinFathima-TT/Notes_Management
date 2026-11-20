from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from notes_app.serializers import RegisterSerializer,NotesSerializer,TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from notes_app.models import NotesDb,TaskDb
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


class RegistrationView(APIView):
    def post(self,request):
        serializer_instance = RegisterSerializer(data = request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={
                "Message" : "Registration Successful...!"
            })
        else:
            return Response(data=serializer_instance.errors)

class UserListView(APIView):
    def get(self,request):
        qs = User.objects.all()
        serializer_instance = RegisterSerializer(qs,many=True)
        return Response(serializer_instance.data,status=200)

class NotesListCreateView(APIView):
    permission_classes =[IsAuthenticated]
    def get(self,request):
        notes = NotesDb.objects.filter(user=request.user)
        serializer_instance = NotesSerializer(notes,many=True)
        return Response(serializer_instance.data)

    def post(self,request):
        form_data = request.data
        serializer_instance = NotesSerializer(data = form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(user = request.user)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class NotesRetrieveUpdateDeleteView(APIView):
    permission_classes =[IsAuthenticated]
    def get(self,request,pk):
        notes_object = get_object_or_404(NotesDb,id = pk)
        if notes_object.user == request.user:
           serializer_instance = NotesSerializer(notes_object)
           return Response(data=serializer_instance.data)
        else:
            raise serializers.ValidationError("Access Denied...!")

    def put(self,request,pk):
        notes_object = get_object_or_404(NotesDb,id=pk)

        if notes_object.user == request.user:
            serializer_instance = NotesSerializer(data=request.data,instance = notes_object)
            if serializer_instance.is_valid():
                serializer_instance.save()
                return Response(data=serializer_instance.data)
            else:
                return Response(data=serializer_instance.errors)
        else:
            raise serializers.ValidationError("Access Denied...!") 

    def delete(self,request,pk):
        notes_object=get_object_or_404(NotesDb,id=pk)
        if notes_object.user != request.user:
            raise serializers.ValidationError("Access Denied...!")
        else:
            notes_object.delete()
            return Response(data={
                "Message" : "Notes Deleted...!"
            })
class LogoutView(APIView):
    permission_classes =[IsAuthenticated]
    def post(self,request):
        request.user.auth_token.delete()
        return Response({
            "Message" : "Logout Success...!"
        })
         



class TaskListCreateView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        tasks = TaskDb.objects.filter(user=request.user)
        serializer_instance = TaskSerializer(tasks,many=True)
        return Response(serializer_instance.data)

    def post(self,request):
        serializer_instance = TaskSerializer(data = request.data)
        if serializer_instance.is_valid():
            serializer_instance.save(user = request.user)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)


class TaskRetriveUpdateDeleteView(APIView):
    permission_classes =[IsAuthenticated]

    def get_task(self,request,id):
        return get_object_or_404(TaskDb,id=id,user=request.user)

    def get(self, request, id):
        task = self.get_task(request, id)
        serializer_instance = TaskSerializer(task)
        return Response(serializer_instance.data)

    def put(self, request, id):
        task = self.get_task(request, id)

        serializer_instance = TaskSerializer(task,data=request.data)

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data)

        return Response(serializer_instance.errors)

    def delete(self, request, id):
        task = self.get_task(request, id)
        
        task.delete()
        return Response(data={
            "Message" : "Task Deleted...!"
        })


class JWT_Logout(APIView):
    permission_classes =[IsAuthenticated]
    def post(self,request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                "Message" : "Logout Success"
            })
        except Exception:
            return Response({
                "Error" : "Invalid refresh token"
            })
    