# infresturtura rest 
from rest_framework import serializers
# nuestro modelo
from toys.models import Toy

class ToySerializer(serializers.Serializer):
    # lo que se va mostrar en el JSON
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150)
    description = serializers.CharField(max_length=250)
    release_date = serializers.DateTimeField()
    toy_category = serializers.CharField(max_length=200)
    was_included_in_home = serializers.BooleanField(required=False)
    
    # el metodo que recibe la validacion, que viene de mi base de datos
    def create(self, validated_data):
        return Toy.objects.create(**validated_data)

    # una ves que son validados entonces se actualiza
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.release_date = validated_data.get('release_date', instance.release_date)
        instance.toy_category = validated_data.get('toy_category', instance.toy_category)
        instance.was_included_in_home = validated_data.get('was_included_in_home', instance.was_included_in_home)
        instance.save()

        return instance