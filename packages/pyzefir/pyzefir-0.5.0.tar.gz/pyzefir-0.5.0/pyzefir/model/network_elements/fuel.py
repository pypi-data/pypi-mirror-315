from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

import pandas as pd

from pyzefir.model.exceptions import (
    NetworkValidatorException,
    NetworkValidatorExceptionGroup,
)
from pyzefir.model.network_element import NetworkElement
from pyzefir.model.utils import validate_dict_type, validate_series

if TYPE_CHECKING:
    from pyzefir.model.network import Network

_logger = logging.getLogger(__name__)


class FuelValidatorExceptionGroup(NetworkValidatorExceptionGroup):
    pass


@dataclass
class Fuel(NetworkElement):
    """
    A class that represents the Fuel in the network structure which may used by dispatchable generators
    """

    emission: dict[str, float]
    """
    Emission per one unit of used fuel
    """
    availability: pd.Series | None
    """
    Maximal amount of fuel availability in each year
    """
    cost: pd.Series
    """
    Cost of 1 unit of fuel in each year [$/1 unit of fuel]
    """
    energy_per_unit: float
    """
    Energy obtained from burning one unit of fuel
    """

    def _validate_attributes(
        self,
        network: Network,
        exception_list: list[NetworkValidatorException],
    ) -> None:
        if self.availability is not None:
            validate_series(
                name="Availability",
                series=self.availability,
                length=network.constants.n_years,
                exception_list=exception_list,
            )
        validate_series(
            name="Cost",
            series=self.cost,
            length=network.constants.n_years,
            exception_list=exception_list,
        )
        if not isinstance(self.energy_per_unit, float | int):
            exception_list.append(
                NetworkValidatorException("Energy per unit must be of float type")
            )

        validate_dict_type(
            dict_to_validate=self.emission,
            key_type=str,
            value_type=float | int,
            parameter_name="Emission mapping",
            key_parameter_name="Emission type",
            value_parameter_name="Emission per unit",
            exception_list=exception_list,
        )
        _logger.debug("Validate attributes: OK")

    def _validate_emission(
        self,
        network: Network,
        exception_list: list[NetworkValidatorException],
    ) -> None:
        for emission_type in self.emission:
            if emission_type not in network.emission_types:
                exception_list.append(
                    NetworkValidatorException(
                        f"Emission type {emission_type} not found in network"
                    )
                )
        _logger.debug("Validate emission: OK")

    def validate(self, network: Network) -> None:
        """
        Validate Fuel element.
            - Validate attribute types
            - Validate if all emission in self.emission are defined in the Network

        Args:
            network (Network): Network to which Fuel is to be added.

        Raises:
            NetworkValidatorExceptionGroup: If Fuel is invalid.
        """
        _logger.debug("Validating fuel element object: %s...", self.name)
        exception_list: list[NetworkValidatorException] = []
        self._validate_name_type(exception_list)
        self._validate_attributes(network, exception_list)

        if isinstance(self.emission, dict):
            self._validate_emission(network, exception_list)

        if exception_list:
            _logger.exception("Got error validating fuel: %s", exception_list)
            raise FuelValidatorExceptionGroup(
                f"While adding Fuel {self.name} following errors occurred: ",
                exception_list,
            )
        _logger.debug("Fuel element %s validation: Done", self.name)
