import pytest
from jsonschema import validate
from rest_framework import serializers

from drf_jsonschema_serializer import to_jsonschema
from testapp.models import Album, Track


@pytest.mark.django_db
def test_string_related_field():
    album = Album.objects.create(
        album_name="Collected Stories", artist="H.P. Lovecraft"
    )
    track1 = track1 = Track.objects.create(
        album=album, order=1, title="The Dunwich Horror", duration=10
    )
    Track.objects.create(album=album, order=2, title="The Call of Cthulhu", duration=15)
    Track.objects.create(
        album=album, order=3, title="At the Mountains of Madness", duration=20
    )

    class AlbumSerializer(serializers.ModelSerializer):
        class Meta:
            model = Album
            fields = ("album_name", "artist", "tracks")

    class TrackSerializer(serializers.ModelSerializer):
        class Meta:
            model = Track
            fields = ("order", "title", "duration")

    json_schema = to_jsonschema(TrackSerializer())

    valid = {"title": "The Dunwich Horror", "order": 1, "duration": 11}

    validate(valid, json_schema)

    serializer = TrackSerializer(track1, data=valid)
    assert serializer.is_valid()

    serializer.save()
    assert track1.duration == 11

    invalid = {"title": "The Dunwich Horror", "order": 1}

    serializer = TrackSerializer(track1, data=invalid)
    assert not serializer.is_valid()

    album_data = AlbumSerializer(album).data

    assert album_data == {
        "album_name": "Collected Stories",
        "artist": "H.P. Lovecraft",
        "tracks": [1, 2, 3],
    }

    album_serializer = AlbumSerializer(album, album_data)
    json_schema = to_jsonschema(album_serializer)

    validate(album_data, json_schema)
