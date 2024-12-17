import dataclasses
import typing

from hdwallet.cryptocurrencies import Ethereum

from .chain import Chain


@dataclasses.dataclass(frozen=True, kw_only=True, repr=False, slots=True)
class EthereumChain(Chain):
    chain_id: int

    @staticmethod
    @typing.override
    def base_coin_type() -> int:
        return Ethereum.COIN_TYPE

    @property
    @typing.override
    def namespace(self) -> str:
        return "eip155"

    @property
    @typing.override
    def reference(self) -> str:
        return str(self.chain_id)
