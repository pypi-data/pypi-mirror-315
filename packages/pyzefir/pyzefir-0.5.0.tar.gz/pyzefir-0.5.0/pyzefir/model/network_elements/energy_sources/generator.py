from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING

from pyzefir.model.exceptions import (
    NetworkValidatorException,
    NetworkValidatorExceptionGroup,
)
from pyzefir.model.network_elements import EnergySource, GeneratorType

if TYPE_CHECKING:
    from pyzefir.model.network import Network

_logger = logging.getLogger(__name__)


class GeneratorValidatorExceptionGroup(NetworkValidatorExceptionGroup):
    pass


@dataclass(kw_only=True)
class Generator(EnergySource):
    """
    Represents a Generator element within the network structure.

    This class extends the EnergySource class to include specific attributes
    and validation procedures for generators, including emission fees and
    bus connections. Generators can be attached to multiple buses and
    have associated energy types and conversion rates.
    """

    emission_fee: set[str] = field(default_factory=set)
    """
    Emission fee assigned to a given generator.
    """
    bus: InitVar[str | set[str]] = None
    """
    Bus name to which the Generator is attached. One generator may be attached to multiple buses.
    """
    buses: set[str] = field(init=False)
    """
    Collection of all buses attached to the generator.
    """
    generator_binding: str | None = None
    """
    Identifier of the generator binding.
    """

    def _validate_buses_energy_types(
        self, exception_list: list[NetworkValidatorException], network: Network
    ) -> None:
        """
        Validation procedure checking:
        - if each bus has a name
        - if the buses have the same energy type

        Args:
            - exception_list (list[NetworkValidatorException]): list of exceptions
        """
        bus_energy_type_dict = defaultdict(list)
        for bus_name in self.buses:
            if (bus := network.buses.get(bus_name)) is not None:
                bus_energy_type_dict[bus.energy_type].append(bus.name)
        for et, et_buses in bus_energy_type_dict.items():
            if len(et_buses) > 1:
                exception_list.append(
                    NetworkValidatorException(
                        f"Buses {sorted(et_buses)} have the same energy_type {et} which is not allowed"
                    )
                )

    def _validate_buses(
        self,
        exception_list: list[NetworkValidatorException],
        network: Network,
        generator_type: GeneratorType,
    ) -> None:
        """
        Validation procedure checking:
        - Validates if bus name existing in network
        - Validates if bus.energy_type match with generator energy types and inbound energy type
        - Validates if buses attr of Generator is set or contains strings
        - Validates if generator has conversion_rate for energy types

        Args:
            - exception_list (NetworkValidatorException): list of raised exceptions.
            - network (Network): network to which self is to be added.
            - generator_type (GeneratorType): GeneratorType object
        """
        should_check_conversion_rate = True
        if not all(isinstance(item, str) for item in self.buses):
            exception_list.append(
                NetworkValidatorException(
                    "Generator attribute 'buses' must contain only strings"
                )
            )
        self._validate_attribute_type(
            attr="buses", attr_type=set, exception_list=exception_list
        )

        self._validate_buses_energy_types(
            exception_list=exception_list, network=network
        )
        for bus_name in self.buses:
            if bus_name not in network.buses:
                exception_list.append(
                    NetworkValidatorException(
                        f"Cannot attach generator to a bus {bus_name} - bus does not exist in the network"
                    )
                )
                should_check_conversion_rate = False
            elif (
                network.buses[bus_name].energy_type
                not in generator_type.energy_types | generator_type.inbound_energy_type
            ):
                gen_en_types = sorted(
                    list(
                        generator_type.energy_types | generator_type.inbound_energy_type
                    )
                )
                exception_list.append(
                    NetworkValidatorException(
                        f"Unable to attach generator to a bus {bus_name}. "
                        f"Bus energy type ({network.buses[bus_name].energy_type}) "
                        f"and generator energy types ({gen_en_types}) do not match"
                    )
                )
                should_check_conversion_rate = False

        if should_check_conversion_rate and (
            diff := (
                set(generator_type.conversion_rate.keys())
                - set([network.buses.get(bus).energy_type for bus in self.buses])
            )
        ):
            exception_list.append(
                NetworkValidatorException(
                    f"Conversion_rate for energy types: "
                    f"{sorted(list(diff))} which are not in connected buses energy types"
                )
            )
        _logger.debug("Validate buses: OK")

    def _validate_generator_type(
        self,
        exception_list: list[NetworkValidatorException],
        network: Network,
        generator_type: GeneratorType,
    ) -> None:
        """
        Validate GeneratorType.
            - Validates if generator_type is type of GeneratorType
            - Validates if generator_type energy types are compliant with the network

        Args:
            - exception_list (list[NetworkValidatorException]): List of exceptions
                to which new exceptions will be added
            - network (Network): Network object to which this object belongs
            - generator_type (GeneratorType): GeneratorType object associated with this Generator
        """
        if generator_type is None:
            exception_list.append(
                NetworkValidatorException("Network does not contain generator type")
            )
            return
        if not isinstance(generator_type, GeneratorType):
            exception_list.append(
                NetworkValidatorException(
                    f"Generator type must be of type GeneratorType, but it is {type(generator_type)} instead."
                )
            )
            return
        gen_energy_types = [en_t for en_t in generator_type.energy_types]
        if not generator_type.energy_types.issubset(network.energy_types):
            exception_list.append(
                NetworkValidatorException(
                    f"Gen energy types: {gen_energy_types}"
                    " are not compliant with the network"
                    f" energy types: {sorted(network.energy_types)}"
                )
            )
        _logger.debug("Validate generator type: OK")

    def _validate_emission_fee(
        self, network: Network, exception_list: list[NetworkValidatorException]
    ) -> None:
        """
        Validation procedure checking:
        - Validates emission_fee in network
        - Validates emission_fee.emission_type are unique for given gen

        Args:
            - exception_list (NetworkValidatorException): list of raised exceptions.
            - network (Network): network to which self is to be added.
        """
        emission_fee_types: set[str] = set()
        network_emissions = network.emission_fees
        for fee in self.emission_fee:
            if fee not in network_emissions:
                exception_list.append(
                    NetworkValidatorException(
                        f"Network does not contain Emission Fee: {fee} in its structure"
                    )
                )
                continue
            emission_type = network_emissions[fee].emission_type
            if (
                emission_type not in emission_fee_types
                and len(
                    duplicated_fees := {
                        em
                        for em in self.emission_fee
                        if network_emissions[em].emission_type == emission_type
                    }
                )
                > 1
            ):
                exception_list.append(
                    NetworkValidatorException(
                        f"There are fees: {sorted(list(duplicated_fees))} which"
                        f" apply to the same type of emission: {emission_type}"
                    )
                )
                emission_fee_types.add(emission_type)
        _logger.debug("Validate emission fee: OK")

    def validate(self, network: Network) -> None:
        """
        Validation procedure checking:
        - if network doesn't contain any generator type and generator type is None
        - correctness of Generator object
        - whether the Generator energy_type is in the energy_type of the network

        Method validate runs following validate methods:
        - _validate_base_energy_source
        - _validate_generator_type
        - _validate_buses

        Args:
            - network (Network): Network to which Generator is to be added.

        Raises:
            - NetworkValidatorExceptionGroup: If Generator is invalid.
        """
        _logger.debug("Validating generator object: %s...", self.name)
        exception_list: list[NetworkValidatorException] = []
        self._validate_base_energy_source(
            network=network, exception_list=exception_list
        )
        generator_type = network.generator_types.get(self.energy_source_type)
        self._validate_generator_type(
            exception_list=exception_list,
            network=network,
            generator_type=generator_type,
        )
        if isinstance(generator_type, GeneratorType):
            self._validate_buses(
                exception_list=exception_list,
                network=network,
                generator_type=generator_type,
            )
        self._validate_emission_fee(network=network, exception_list=exception_list)
        if exception_list:
            _logger.debug("Got error validating generator: %s", exception_list)
            raise GeneratorValidatorExceptionGroup(
                f"While adding Generator {self.name} with type {self.energy_source_type} following errors occurred: ",
                exception_list,
            )
        _logger.debug("Generator %s validation: Done", self.name)

    def __post_init__(self, bus: str | set[str]) -> None:
        if bus is None:
            self.buses = set()
        else:
            self.buses = {bus} if isinstance(bus, str) else bus
