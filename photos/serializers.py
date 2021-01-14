from rest_framework import serializers

from .models import Photo


def descent_orders(orders):
    return tuple(orders) + tuple(['-' + order for order in orders])


class BaseSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(
        read_only=True,
        help_text='Date and time when instance was created'
    )

    updated_at = serializers.DateTimeField(
        read_only=True,
        help_text='Date and time when instance was updated'
    )

    # List of fields that are serialized only if explicit required
    explicit_req = ()

    # noinspection PyUnresolvedReferences
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(BaseSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        elif len(self.explicit_req):
            for field_name in self.explicit_req:
                self.fields.pop(field_name)

    class Meta:
        fields = (
            'id',
            'created_at',
            'updated_at'
        )


class PhotoSerializer(BaseSerializer):
    class Meta:
        model = Photo

        fields = BaseSerializer.Meta.fields + (
            'session',
            'side',
            'temperature',
            'error',
            'image',
        )

        extra_kwargs = {
            'temperature': {'read_only': True},
            'error': {'read_only': True},
            'image': {'read_only': True}
        }
