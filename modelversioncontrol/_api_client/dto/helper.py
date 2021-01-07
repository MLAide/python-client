from dataclasses import field
from dataclasses_json import config, DataClassJsonMixin
from datetime import datetime
from dateutil.parser import isoparse
from marshmallow import fields
from typing import Optional


def optional_iso_datetime_encoder(value: Optional[datetime]) -> str:
    return datetime.isoformat(value) if value is not None else None


def optional_iso_datetime_decoder(value: Optional[str]) -> datetime:
    return isoparse(value) if value is not None else None


def datetime_field():
    return field(
        default=None,
        metadata=config(
            encoder=optional_iso_datetime_encoder,
            decoder=optional_iso_datetime_decoder,
            mm_field=fields.DateTime(format='iso')
        )
    )


class ExtendedDtoSerializer(DataClassJsonMixin):
    def to_dict_without_none_values(self):
        d = self.to_dict()

        # Remove values from dict that are None
        return {k: v for k, v in d.items() if v is not None}
