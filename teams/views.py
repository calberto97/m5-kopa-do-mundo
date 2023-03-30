from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.forms.models import model_to_dict
from teams.models import Team
from teams.utils import data_processing
from teams.exceptions import (
    ImpossibleTitlesError,
    InvalidYearCupError,
    NegativeTitlesError,
)


class TeamsView(APIView):
    def post(self, request):
        payload = request.data
        try:
            data_processing(payload)

            team = Team(**payload)
            team.save()

            return Response(model_to_dict(team), 201)
        except (
            NegativeTitlesError,
            InvalidYearCupError,
            ImpossibleTitlesError,
        ) as err:
            # return Response(f"{err.__class__.__name__}: {err.message}")
            return Response({"error": err.message}, 400)

    def get(self, request):
        data = Team.objects.all()
        data_dict = []

        for element in data:
            e = model_to_dict(element)
            data_dict.append(e)

        return Response(data_dict, 200)
