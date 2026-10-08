"""Tache 1 et 2 : serializers et validation.

A FAIRE :
  - SalleSerializer (ModelSerializer)
  - ReservationSerializer (ModelSerializer) :
      * le champ `utilisateur` est en LECTURE SEULE (il sera renseigne par la vue)
      * validation : `fin` strictement apres `debut`
      * validation : pas de chevauchement avec une autre reservation CONFIRMEE
        de la meme salle
"""
from rest_framework import serializers

from .models import Reservation, Salle  # noqa: F401  (a utiliser)

# TODO : votre code ici

from rest_framework import serializers

from .models import Reservation, Salle


class SalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salle
        fields = ["nom", "capacite", "batiment"]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            "salle",
            "utilisateur",
            "debut",
            "fin",
            "motif",
            "statut",
            "cree_le",
        ]
        read_only_fields = ["utilisateur", "cree_le"]

    def validate(self, data):
        debut = data.get("debut", self.instance.debut if self.instance else None)
        fin = data.get("fin", self.instance.fin if self.instance else None)
        salle = data.get("salle", self.instance.salle if self.instance else None)
        statut = data.get(
            "statut",
            self.instance.statut if self.instance else Reservation.Statut.CONFIRMEE,
        )

        if debut and fin and fin <= debut:
            raise serializers.ValidationError(
                {"fin": "La fin doit être postérieure au début."}
            )

        if salle and debut and fin and statut == Reservation.Statut.CONFIRMEE:
            reservations = Reservation.objects.filter(
                salle=salle,
                statut=Reservation.Statut.CONFIRMEE,
                debut__lt=fin,
                fin__gt=debut,
            )

            if self.instance:
                reservations = reservations.exclude(pk=self.instance.pk)

            if reservations.exists():
                raise serializers.ValidationError(
                    "Cette salle est déjà réservée sur cette période."
                )

        return data