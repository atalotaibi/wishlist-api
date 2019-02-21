from rest_framework import serializers
from items.models import Item, FavoriteItem
from django.contrib.auth.models import User




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']



class ItemListSerializer(serializers.ModelSerializer):
    detail = serializers.HyperlinkedIdentityField(
        view_name = "api-detail",
        lookup_field = "id",
        lookup_url_kwarg = "item_id",
        )
    
    num_of_likes = serializers.SerializerMethodField()

    def get_num_of_likes(self, obj):
        FavNum = obj.favoriteitem_set.all().count()
        return FavNum
        
    
    
    class Meta:
        model = Item
        fields = '__all__'
    

class FavSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = FavoriteItem
        fields = ['user']


class ItemDetailSerializer(serializers.ModelSerializer):
    # owner = OwnerSerializer()
    favorited_by = serializers.SerializerMethodField()
    class Meta:
        model = Item
        fields = '__all__'

    def get_favorited_by(self,obj):
        FavItems = obj.favoriteitem_set.all()
        return FavSerializer( FavItems ,many=True).data
