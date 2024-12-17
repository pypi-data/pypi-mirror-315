from __future__ import annotations
import dataclasses
import typing

from hdwallet import HDWallet
from hdwallet.const import PUBLIC_KEY_TYPES
from hdwallet.cryptocurrencies import Bitcoin
from hdwallet.derivations import BIP44Derivation
from hdwallet.entropies import BIP39_ENTROPY_STRENGTHS, BIP39Entropy
from hdwallet.hds import BIP44HD
from hdwallet.mnemonics import BIP39Mnemonic

from ..chain import Chain
from .account import Account, AccountID


CRYPTOCURRENCY = Bitcoin


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class Wallet:
    hdwallet: HDWallet

    @staticmethod
    def create_base() -> HDWallet:
        return HDWallet(
            cryptocurrency=CRYPTOCURRENCY,
            hd=BIP44HD,
            network=CRYPTOCURRENCY.NETWORKS.MAINNET,
            public_key_type=PUBLIC_KEY_TYPES.COMPRESSED,
        )

    @classmethod
    def create(cls) -> Wallet:
        hdwallet = cls.create_base().from_entropy(
            entropy=BIP39Entropy(
                entropy=BIP39Entropy.generate(
                    strength=BIP39_ENTROPY_STRENGTHS.TWO_HUNDRED_FIFTY_SIX
                )
            )
        )

        return cls(hdwallet=hdwallet)

    @classmethod
    def from_mnemonic(cls, mnemonic: str) -> Wallet:
        hdwallet = cls.create_base().from_mnemonic(mnemonic=BIP39Mnemonic(mnemonic))

        return cls(hdwallet=hdwallet)

    @classmethod
    def from_extended_private_key(cls, xprivate_key: str) -> Wallet:
        hdwallet = cls.create_base().from_xprivate_key(xprivate_key=xprivate_key)

        return cls(hdwallet=hdwallet)

    @property
    def mnemonic(self) -> str:
        return typing.cast(str, self.hdwallet.mnemonic())

    @property
    def xprivate_key(self) -> str:
        return typing.cast(str, self.hdwallet.xprivate_key())

    def derive_default(self, chain: Chain) -> HDWallet:
        return self.hdwallet.from_derivation(
            # Notice that we use the base coin type instead of the chain's coin type
            # So ie. BNB will use the same derivation path as Ethereum
            # This is to ensure that as many chains use the same keypair as possible
            derivation=BIP44Derivation(coin_type=chain.base_coin_type())
        )

    def account[ChainType: Chain](self, chain: ChainType) -> Account[ChainType]:
        private_key = self.derive_default(chain).private_key()
        return Account.from_str(chain, private_key)  # type: ignore

    def account_id[ChainType: Chain](self, chain: ChainType) -> AccountID[ChainType]:
        address = self.derive_default(chain)
        return AccountID.from_str(chain, address)  # type: ignore
