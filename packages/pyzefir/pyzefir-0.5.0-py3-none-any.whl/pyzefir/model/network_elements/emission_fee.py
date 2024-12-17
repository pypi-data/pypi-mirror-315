from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from pyzefir.model.exceptions import (
    NetworkValidatorException,
    NetworkValidatorExceptionGroup,
)
from pyzefir.model.network_element import NetworkElement
from pyzefir.model.utils import validate_series

if TYPE_CHECKING:
    from pyzefir.model.network import Network

_logger = logging.getLogger(name=__name__)


class EmissionFeeValidatorExceptionGroup(NetworkValidatorExceptionGroup):
    pass


@dataclass(kw_only=True)
class EmissionFee(NetworkElement):
    """
    A class that represents the Emission Fee element in the network structure
    """

    emission_type: str
    """ Name of the emission type """
    price: pd.Series
    """ Amount of a given emission fee in particular years"""

    def validate(self, network: Network) -> None:
        """
        Validation procedure checking:
            - if emission_type is in the network
            - if the price is a correct pd.Series

        Args:
            network (Network): Network to which EmissionFee is to be added.

        Raises:
            NetworkValidatorExceptionGroup: If any of the validations fails.
        """
        _logger.debug("Validating emission fee element object: %s...", self.name)
        exception_list: list[NetworkValidatorException] = []

        if self.emission_type not in network.emission_types:
            exception_list.append(
                NetworkValidatorException(
                    f"Emission type: {self.emission_type} does not exist in the network"
                )
            )

        validate_series(
            name="EmissionFee",
            series=self.price,
            length=network.constants.n_years,
            exception_list=exception_list,
            index_type=np.integer,
            values_type=np.floating,
            allow_null=False,
        )

        if exception_list:
            _logger.debug("Got error validating emission fee: %s", exception_list)
            raise EmissionFeeValidatorExceptionGroup(
                f"While adding EmissionFee {self.name} following errors occurred: ",
                exception_list,
            )
        _logger.debug("Emission fee element %s validation: Done", self.name)
