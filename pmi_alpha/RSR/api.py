from rest_framework import routers, serializers, viewsets
from .models import *
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# Serializers define the API representation.
class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ('Name', 'Email', 'Address')

# ViewSets define the view behavior.
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class SkillCount(APIView):
    renderer_classes = (JSONRenderer, )
    queryset = PersonToSkills.objects.all()
    def get(self, request, format=None):
        print(request.GET)
        arr =[]
        for skill in Skills.objects.all():
            d = {}
            d['name'] = skill.Name
            d['count']= PersonToSkills.objects.filter(SkillsID=skill.pk).count()
            arr.append(d)
        new_arr = list(reversed(sorted(arr,key=lambda k:k['count'])))
        print(new_arr[0:10])
        return Response(new_arr[0:10])
