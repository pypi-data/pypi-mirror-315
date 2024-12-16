import dataclasses
import typing

from hdwallet.cryptocurrencies import ICryptocurrency, Solana

from .chain import Chain


@dataclasses.dataclass(frozen=True, kw_only=True, repr=False, slots=True)
class SolanaChain(Chain):
    genesis_block_hash: str

    @staticmethod
    @typing.override
    def base_coin_type() -> int:
        return Solana.COIN_TYPE

    @property
    @typing.override
    def namespace(self) -> str:
        return "solana"

    @property
    @typing.override
    def reference(self) -> str:
        return self.genesis_block_hash

    @property
    @typing.override
    def coin(self) -> type[ICryptocurrency]:
        return Solana
