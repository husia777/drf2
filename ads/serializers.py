from rest_framework import serializers

from ads.models import Users, Locations


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    location = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Locations.objects.all(),
        slug_field='name',
    )
    class Meta:
        model = Users
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Locations.objects.all(),
        slug_field='name',
    )
    class Meta:
        model = Users
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    location = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Locations.objects.all(),
        slug_field='name',
    )

    class Meta:
        model = Users
        fields = '__all__'


    def is_valid(self, *, raise_exception=False):
        qd = self.initial_data.copy()
        self._locations = qd.pop('location')
        self.initial_data = qd
        valid_result = super().is_valid(raise_exception=raise_exception)
        qd.update({'location': self._locations})
        return valid_result


    def create(self, validated_data):
        validated_data.pop('location')
        user = Users.objects.create(**validated_data)

        for location in self._locations:
            user_loc, _ = Locations.objects.get_or_create(name=location)
            user.location.add(user_loc)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Locations.objects.all(),
        slug_field='name',
    )

    class Meta:
        model = Users
        fields = '__all__'


    def is_valid(self, *, raise_exception=False):
        qd = self.initial_data.copy()
        self._locations = qd.pop('location') if qd['location'] else None
        self.initial_data = qd
        valid_result = super().is_valid(raise_exception=raise_exception)
        qd.update({'location': self._locations})
        self.initial_data = qd
        return valid_result


    def save(self):
        user = super().save()

        for location in self._locations:
            user_loc, _ = Locations.objects.get_or_create(name=location)
            user.location.add(user_loc)
        user.save()
        return user


class UserDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id"]
