"""Taches 3, 4, 5 (et bonus) : vues de l'API.

A FAIRE :
  - SalleViewSet (ModelViewSet), avec l'action `occupation` (tache 5)
  - ReservationViewSet (ModelViewSet), avec perform_create (tache 3)
"""
from rest_framework import viewsets  # noqa: F401  (a utiliser)

from .models import Reservation, Salle  # noqa: F401  (a utiliser)

# TODO : votre code ici

from django.utils import timezone
from django.utils.dateparse import parse_datetime

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Reservation, Salle
from .permissions import IsOwnerOrReadOnly
from .serializers import ReservationSerializer, SalleSerializer


class SalleViewSet(viewsets.ModelViewSet):
    queryset = Salle.objects.all()
    serializer_class = SalleSerializer

    def get_permissions(self):
        if self.request.method in ("GET", "HEAD", "OPTIONS"):
            return [AllowAny()]

        return [IsAdminUser()]

    @action(detail=True, methods=["get"])
    def occupation(self, request, pk=None):
        salle = self.get_object()

        debut = parse_datetime(request.query_params.get("debut", ""))
        fin = parse_datetime(request.query_params.get("fin", ""))

        if debut is None or fin is None:
            return Response(
                {
                    "detail": (
                        "Les paramètres 'debut' et 'fin' sont "
                        "requis au format ISO 8601."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if timezone.is_naive(debut):
            debut = timezone.make_aware(debut)

        if timezone.is_naive(fin):
            fin = timezone.make_aware(fin)

        if fin <= debut:
            return Response(
                {"detail": "'fin' doit être postérieure à 'debut'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reservations = Reservation.objects.filter(
            salle=salle,
            statut=Reservation.Statut.CONFIRMEE,
            debut__lt=fin,
            fin__gt=debut,
        )

        duree_totale = (fin - debut).total_seconds()
        duree_occupee = 0

        for reservation in reservations:
            debut_reservation = max(reservation.debut, debut)
            fin_reservation = min(reservation.fin, fin)

            duree_occupee += (
                fin_reservation - debut_reservation
            ).total_seconds()

        taux_occupation = duree_occupee / duree_totale

        return Response(
            {"taux_occupation": taux_occupation}
        )


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.select_related("salle", "utilisateur")
    serializer_class = ReservationSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()

        salle = self.request.query_params.get("salle")
        date = self.request.query_params.get("date")

        if salle:
            queryset = queryset.filter(salle_id=salle)

        if date:
            queryset = queryset.filter(debut__date=date)

        return queryset