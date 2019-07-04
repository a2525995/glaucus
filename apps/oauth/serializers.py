from rest_framework import serializers
from apps.oauth.models import User, Group
from tools.utils import sha_256


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("uid", "username", "password", "name", "admin", "developer", 'last_login', 'date_joined')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('uid', 'username', 'last_login', 'date_joined')

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.password = sha_256(validated_data.get('password'))
        instance.save()
        return instance


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("gid", "create_or_delete", "update")
        read_only_fields = ('gid',)

#
# class SlidesSerializer(serializers.ModelSerializer):
#     """
#      此处的`fields`字段是用来替换上面Serializer内部Meta类中指定的`fields`属性值
#     """
#
#     def __init__(self, *args, **kwargs):
#         # 在super执行之前
#         # 将传递的`fields`中的字段从kwargs取出并剔除，避免其传递给基类ModelSerializer
#         # 注意此处`fields`中在默认`self.fields`属性中不存在的字段将无法被序列化 也就是`fields`中的字段应该
#         # 是`self.fields`的子集
#         fields = kwargs.pop('fields', None)
#
#         super(BaseModeSerializer, self).__init__(*args, **kwargs)
#
#         if fields is not None:
#             # 从默认`self.fields`属性中剔除非`fields`中指定的字段
#             allowed = set(fields)
#             existing = set(self.fields.keys())
#             for field_name in existing - allowed:
#                 self.fields.pop(field_name)
#
#     class Meta:
#         model = models.Slides
#         fields = ('id', 'title', 'image', 'url', 'no',)
# >>> print SlidesSerializer(sides)
# {'id': 2, 'title': '道地良品', 'image': '/daodi.png', 'url': 'www.daodikeji.com', 'no': 'DD_BJ_001'}
# >>> print SlidesSerializer(sides, fields=('id', 'title'))
# {'id': 2, 'title': '道地良品'}
