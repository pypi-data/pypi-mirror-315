from __future__ import annotations
import abc
from abc import ABC
import dataclasses
from typing import Any

from hdwallet import cryptocurrencies
from hdwallet.cryptocurrencies import ICryptocurrency


# CAIP-2 Chain
# https://chainagnostic.org/CAIPs/caip-2
# https://chainagnostic.org/CAIPs/caip-288
@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class Chain(ABC):
    @staticmethod
    def from_id(namespace: str, reference: str) -> Chain:
        match namespace:
            case "eip155":
                return EthereumChain(chain_id=int(reference))
            case "solana":
                return SolanaChain(genesis_block_hash=reference)
            case "tron":
                return TronChain(genesis_block_hash=reference)
            case _:
                assert False

    @staticmethod
    def from_str(name: str) -> Chain:
        return constants.NAME_TO_CHAIN[name]

    @staticmethod
    def from_layerzero_id(id: int) -> Chain:
        return constants.LAYERZERO_ID_TO_CHAIN[id]

    # Used to derive accounts from HD wallets
    @staticmethod
    @abc.abstractmethod
    def base_coin_type() -> int:
        pass

    @property
    @abc.abstractmethod
    def namespace(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def reference(self) -> str:
        pass

    # Best effort, doesn't work for a lot of chains (`hdwallet` also doesn't support a bunch of them)
    @property
    def coin(self) -> type[ICryptocurrency]:
        return cryptocurrencies.get_cryptocurrency(str(self))

    @property
    def id(self) -> str:
        return f"{self.namespace}:{self.reference}"

    @property
    def layerzero_id(self) -> int:
        return constants.CHAIN_TO_LAYERZERO_ID[self]

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Chain) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self})"

    def __str__(self) -> str:
        return constants.CHAIN_TO_NAME[self]


# Avoid a circular import
from . import constants  # noqa: E402
from .ethereum import EthereumChain  # noqa: E402
from .solana import SolanaChain  # noqa: E402
from .tron import TronChain  # noqa: E402
