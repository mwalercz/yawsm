from lib.serializers import JsonDeserializer, JsonSerializer


def deserializer(c):
    return JsonDeserializer()


def serializer(c):
    return JsonSerializer()


def register(c):
    c.add_service(serializer)
    c.add_service(deserializer)
