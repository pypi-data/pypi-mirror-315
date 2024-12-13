from typing import Any

import terminusgps.wialon.flags as flags
from terminusgps.wialon.session import WialonSession


class WialonBase:
    def __init__(
        self, *, id: str | None = None, session: WialonSession, **kwargs
    ) -> None:
        self._session = session

        if not id:
            self._id = self.create(**kwargs)
        else:
            self._id = id
        self.populate()

    def __str__(self) -> str:
        return f"{self.__class__}:{self.id}"

    @property
    def session(self) -> WialonSession:
        return self._session

    @property
    def id(self) -> int | None:
        return int(self._id) if self._id else None

    def has_access(self, other_item: "WialonBase") -> bool:
        response = self.session.wialon_api.core_check_accessors(
            **{"items": [other_item.id], "flags": False}
        )
        if self.id in response.keys():
            return True
        return False

    def create(self) -> int | None:
        """Creates a Wialon object and returns the newly created Wialon object's id."""
        raise NotImplementedError("Subclasses must implement this method.")

    def populate(self) -> None:
        """Retrieves and sets hw_type and name for this Wialon object."""
        item = self.session.wialon_api.core_search_item(
            **{"id": self.id, "flags": flags.DATAFLAG_UNIT_BASE}
        ).get("item", {})
        self.hw_type = item.get("cls", None)
        self.name = item.get("nm", None)
        self.uid = item.get("uid", None)

    def rename(self, new_name: str) -> None:
        self.session.wialon_api.item_update_name(
            **{"itemId": self.id, "name": new_name}
        )
        self.populate()

    def add_afield(self, field: tuple[str, str]) -> None:
        self.session.wialon_api.item_update_admin_field(
            **{
                "itemId": self.id,
                "id": 0,
                "callMode": "create",
                "n": field[0],
                "v": field[1],
            }
        )

    def update_afield(self, field_id: int, field: tuple[str, str]) -> None:
        self.session.wialon_api.item_update_admin_field(
            **{
                "itemId": self.id,
                "id": field_id,
                "callMode": "update",
                "n": field[0],
                "v": field[1],
            }
        )

    def add_cfield(self, field: tuple[str, str]) -> None:
        self.session.wialon_api.item_update_custom_field(
            **{
                "itemId": self.id,
                "id": 0,
                "callMode": "create",
                "n": field[0],
                "v": field[1],
            }
        )

    def update_cfield(self, field_id: int, field: tuple[str, str]) -> None:
        self.session.wialon_api.item_update_custom_field(
            **{
                "itemId": self.id,
                "id": field_id,
                "callMode": "update",
                "n": field[0],
                "v": field[1],
            }
        )

    def add_cproperty(self, field: tuple[str, str]) -> None:
        self.session.wialon_api.item_update_custom_property(
            **{"itemId": self.id, "name": field[0], "value": field[1]}
        )

    def add_profile_field(self, field: tuple[str, str]) -> None:
        self.session.wialon_api.item_update_profile_field(
            **{"itemId": self.id, "n": field[0], "v": field[1]}
        )

    def delete(self) -> None:
        self.session.wialon_api.item_delete_item(**{"itemId": self.id})

    @property
    def cfields(self) -> dict[str, Any]:
        response = self.session.wialon_api.core_search_item(
            **{"id": self.id, "flags": flags.DATAFLAG_UNIT_CUSTOM_FIELDS}
        )
        return response.get("item", {}).get("flds")
