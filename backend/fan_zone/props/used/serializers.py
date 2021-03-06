from rest_framework import serializers

from authentication.models import User
from authentication.serializers import AdminSerializer

from cinetubbies.utils.func import deepcopy
from cinetubbies.utils.func import update

from fan_zone.props.models import Prop
from fan_zone.props.serializers import PropSerializer


class PublicSerializer(PropSerializer):
  owner = AdminSerializer(
    read_only=True,
  )
  expiration_date = serializers.DateField()
  approved = serializers.BooleanField(
    read_only=True,
  )
  pending_approval = serializers.BooleanField(
    read_only=True,
  )


  def to_representation(self, obj):
    ret = super().to_representation(obj)
    ret['expirationDate'] = ret.pop('expiration_date')
    ret['pendingApproval'] = ret.pop('pending_approval')
    return ret


class MemberSerializer(PublicSerializer):
  owner_id = serializers.PrimaryKeyRelatedField(
    queryset=User.objects.all(),
    write_only=True,
    source='owner'
  )

  def to_internal_value(self, data):
    d = deepcopy(data)
    d['owner_id'] = d.pop('ownerId')
    d['category_id'] = d.pop('categoryId')
    d['expiration_date'] = d.pop('expirationDate')
    return super().to_internal_value(d)

  def create(self, validated_data):
    return Prop.objects.create(**validated_data)

  def update(self, prop, validated_data):
    prop = update(prop, **validated_data)
    prop.save()
    return prop
