from django.contrib.auth.models import User, Group
from django.db import models
from rest_framework import serializers, viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.hashers import make_password
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import action
from rest_framework.response import Response

# Complaint Model
class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Resolved', 'Resolved')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

# Serializer
class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'

# ViewSet
class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def update_status(self, request, pk=None):
        complaint = self.get_object()
        complaint.status = request.data.get('status', complaint.status)
        complaint.save()
        return Response({'status': complaint.status, 'message': 'Status updated successfully'})

# Router Setup
router = DefaultRouter()
router.register(r'complaints', ComplaintViewSet)

# URL Patterns
urlpatterns = [
    path('api/', include(router.urls)),
]
