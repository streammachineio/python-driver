from dataclasses import dataclass


from ..serializer import SerializationType, SerializationProvider
from ..serializer.type import UnsupportedSerializationTypeException


@dataclass
class StrmPrivacyEventDTO(object):
    event: object
    serialization_type: SerializationType

    def get_schema_ref(self) -> str:
        return self.event.get_strm_schema_ref()

    def get_schema_type(self) -> str:
        return self.event.get_strm_schema_type()

    def get_serialization_type_header(self) -> str:
        if (self.serialization_type is SerializationType.JSON or
                self.serialization_type is SerializationType.AVRO_JSON):
            return "application/json"
        elif self.serialization_type is SerializationType.AVRO_BINARY:
            return "application/x-avro-binary"
        else:
            raise UnsupportedSerializationTypeException(
                f"Serialization type '{self.serialization_type}' is not supported")

    def serialize(self) -> bytes:
        stream_machine_schema = self.event.get_strm_schema()
        serializer = SerializationProvider.get_serializer(self.get_schema_ref(), self.get_schema_type(),
                                                          stream_machine_schema)

        return serializer.serialize(self.event, self.serialization_type)
