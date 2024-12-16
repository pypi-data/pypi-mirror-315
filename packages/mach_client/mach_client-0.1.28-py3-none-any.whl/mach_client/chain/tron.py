import dataclasses
import typing

from hdwallet.cryptocurrencies import ICryptocurrency, Tron

from .chain import Chain


@dataclasses.dataclass(frozen=True, kw_only=True, repr=False, slots=True)
class TronChain(Chain):
    genesis_block_hash: str

    @staticmethod
    @typing.override
    def base_coin_type() -> int:
        return Tron.COIN_TYPE

    @property
    @typing.override
    def namespace(self) -> str:
        return "tron"

    @property
    @typing.override
    def reference(self) -> str:
        return self.genesis_block_hash

    @property
    @typing.override
    def coin(self) -> type[ICryptocurrency]:
        return Tron
