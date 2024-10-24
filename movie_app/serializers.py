from rest_framework import serializers
from rest_framework.authtoken.admin import User

from .models import Director, Movie, Review, ConfirmationCode


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'name']

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Имя режиссера должно содержать хотя бы 2 символа.")
        return value


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'duration', 'director']

    def validate_title(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Название фильма должно содержать хотя бы 2 символа.")
        return value

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError("Длительность фильма должна быть больше 0.")
        return value

    def validate(self, data):
        if len(data['description']) < 10:
            raise serializers.ValidationError("Описание должно содержать хотя бы 10 символов.")
        return data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'movie', 'stars']

    def validate_stars(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5.")
        return value

    def validate_text(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Текст отзыва должен содержать хотя бы 10 символов.")
        return value


class MovieWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'duration', 'director', 'reviews', 'rating']

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            average_rating = sum([review.stars for review in reviews]) / reviews.count()
            return round(average_rating, 2)
        return 0


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            is_active=False  # Пользователь создается неактивным
        )
        ConfirmationCode.objects.create(user=user)  # Генерация и привязка кода
        return user


class UserConfirmationSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
            confirmation_code = ConfirmationCode.objects.get(user=user)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден.")
        except ConfirmationCode.DoesNotExist:
            raise serializers.ValidationError("Код подтверждения не найден.")

        if confirmation_code.code != data['code']:
            raise serializers.ValidationError("Неверный код подтверждения.")

        return data

    def save(self, validated_data):
        user = User.objects.get(username=validated_data['username'])
        user.is_active = True  # Активируем пользователя
        user.save()
        ConfirmationCode.objects.get(user=user).delete()  # Удаляем код после подтверждения
