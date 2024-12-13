from typing import List, Union, TYPE_CHECKING
from uuid import UUID
from hydroserverpy.core.endpoints.base import HydroServerEndpoint, expand_docstring
from hydroserverpy.core.schemas import Unit

if TYPE_CHECKING:
    from hydroserverpy.core.service import HydroServer


class UnitEndpoint(HydroServerEndpoint):
    """
    An endpoint for interacting with unit entities in the HydroServer service.

    :ivar _model: The model class associated with this endpoint, set to `Unit`.
    :ivar _api_route: The base route of the API, derived from the service.
    :ivar _endpoint_route: The specific route of the endpoint, set to `'units'`.
    """

    def __init__(self, service: "HydroServer"):
        """
        Initialize the UnitEndpoint.

        :param service: The HydroServer service instance to use for requests.
        :type service: HydroServer
        """

        super().__init__(service)
        self._model = Unit
        self._api_route = self._service.api_route
        self._endpoint_route = "units"

    def list(
        self,
        include_owned: bool = True,
        include_unowned: bool = True,
        include_templates: bool = True,
    ) -> List[Unit]:
        """
        Retrieve a collection of units.

        :param include_owned: Whether to include owned observed properties.
        :param include_unowned: Whether to include unowned observed properties.
        :param include_templates: Whether to include template observed properties.
        """

        if (
            include_owned is True
            and include_unowned is True
            and include_templates is True
        ):
            owner = "anyUserOrNoUser"
        elif (
            include_owned is True
            and include_unowned is True
            and include_templates is False
        ):
            owner = "anyUser"
        elif (
            include_owned is True
            and include_unowned is False
            and include_templates is True
        ):
            owner = "currentUserOrNoUser"
        elif (
            include_owned is True
            and include_unowned is False
            and include_templates is False
        ):
            owner = "currentUser"
        elif (
            include_owned is False
            and include_unowned is False
            and include_templates is True
        ):
            owner = "noUser"
        else:
            return []

        return super()._get(params={"owner": owner})

    @expand_docstring(include_uid=True)
    def get(self, uid: Union[UUID, str]) -> Unit:
        """
        Retrieve a unit owned by the logged-in user.
        """

        return super()._get(uid)

    @expand_docstring(model=Unit)
    def create(self, **kwargs) -> Unit:
        """
        Create a new unit in HydroServer.
        """

        return super()._post(**kwargs)

    @expand_docstring(model=Unit, include_uid=True)
    def update(self, uid: Union[UUID, str], **kwargs) -> Unit:
        """
        Update an existing unit in HydroServer.
        """

        return super()._patch(uid=uid, **kwargs)

    @expand_docstring(include_uid=True)
    def delete(self, uid: Union[UUID, str]) -> None:
        """
        Delete an existing unit in HydroServer.
        """

        super()._delete(uid=uid)
