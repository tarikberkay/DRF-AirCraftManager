from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from aircraft.models import Personel, Team, Part, Aircraft, AircraftPart
from aircraft.rest.serializers import (
    PersonelSerializer,
    TeamSerializer,
    PartAllSerializer,
    PartSerializer,
    AircraftSerializer,
    AircraftPartSerializer,
)

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import get_object_or_404

from drf_spectacular.utils import (
    extend_schema, inline_serializer, OpenApiParameter, OpenApiTypes)


class PersonelView(APIView):
    """ Tüm personelleri getirir. """
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Personel"],
    )
    def get(self, request):
        personels = Personel.objects.all()
        serializer = PersonelSerializer(personels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PersonelDetailView(APIView):
    """Personelin detayını görmek için API."""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Personel"],
    )
    def get(self, request, pk):
        try:
            personnel = Personel.objects.get(pk=pk)
            serializer = PersonelSerializer(personnel)
            return Response(serializer.data)
        except Personel.DoesNotExist:
            return Response({"error": "Personnel not found."}, status=status.HTTP_404_NOT_FOUND)


class TeamListView(APIView):
    """Takım listesini görmek için API."""
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Team"],
    )
    def get(self, request):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeamDetailView(APIView):
    """Takımların detaylarını görmek için API."""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Team"],
    )
    def get(self, request, pk):
        try:
            team = Team.objects.get(pk=pk)
            serializer = TeamSerializer(team)
            return Response(serializer.data)
        except Team.DoesNotExist:
            return Response({"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND)


class PartView(APIView):
    """Bütün Parçaların listesini gösteren API."""
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["part"],
    )
    def get(self, request):
        parts = Part.objects.all()
        serializer = PartAllSerializer(instance=parts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PartListCreateView(APIView):
    """Parçaların listelenmesi ve yeni parça eklenmesi için API."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        parts = Part.objects.filter(team=request.user.personel.team)
        serializer = PartSerializer(parts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(team=request.user.personel.team)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PartProduceView(APIView):
    """Parça üretim işlemi."""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            # Sadece kullanıcının takımına ait olan parçayı getiriyoruz
            part = Part.objects.get(pk=pk, team=request.user.personel.team)
            amount = int(request.data.get("amount", 1))
            part.produce_part(amount)
            return Response({"status": "Part produced successfully."}, status=status.HTTP_200_OK)
        except Part.DoesNotExist:
            return Response({"error": "Part not found or not allowed."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PartRecycleView(APIView):
    """Parça geri dönüşüm işlemi."""
    permission_classes = [IsAuthenticated]

    def delete(self, request, part_id):
        # Kullanıcının takımı üzerinden ilgili parçayı getiriyoruz
        part = get_object_or_404(
            Part, id=part_id, team=request.user.personel.team)

        # Parçayı geri dönüşüme göndererek tamamen silme
        part.delete()
        return Response({"message": "Part recycled (deleted) successfully."}, status=status.HTTP_204_NO_CONTENT)


class AircraftListCreateView(APIView):
    """Uçakların listelenmesi ve yeni uçak eklenmesi için API."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        aircrafts = Aircraft.objects.all()
        serializer = AircraftSerializer(aircrafts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AircraftSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AircraftAssembleView(APIView):
    """Uçağı monte etme işlemi."""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            aircraft = Aircraft.objects.get(pk=pk)
            assembly_status = aircraft.assemble_aircraft()
            return Response({"status": assembly_status}, status=status.HTTP_200_OK)
        except Aircraft.DoesNotExist:
            return Response({"error": "Aircraft not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
