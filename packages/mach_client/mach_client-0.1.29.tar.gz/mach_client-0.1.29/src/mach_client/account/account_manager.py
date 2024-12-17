from __future__ import annotations
import abc
from abc import ABC
import typing
from typing import Optional

from ..chain import Chain, EthereumChain, SolanaChain, TronChain
from .account import Account, AccountID
from .hdwallet import Wallet


class AccountIDManager(ABC):
    __slots__ = tuple()

    @abc.abstractmethod
    def get(self, chain: Chain) -> Optional[AccountID]:
        pass

    @abc.abstractmethod
    def __getitem__(self, chain: Chain) -> AccountID:
        pass

    def __contains__(self, chain: Chain) -> bool:
        return self.get(chain) is not None


class AccountIDManagerAdapter(AccountIDManager):
    __slots__ = ("account_manager",)

    def __init__(self, account_manager: AccountManager) -> None:
        self.account_manager = account_manager

    @typing.override
    def get(self, chain: Chain) -> Optional[AccountID]:
        if not (account := self.account_manager.get(chain)):
            return None

        return account.downcast()

    @typing.override
    def __getitem__(self, chain: Chain) -> AccountID:
        return self.account_manager[chain].downcast()


class AccountManager(ABC):
    __slots__ = tuple()

    @abc.abstractmethod
    def get(self, chain: Chain) -> Optional[Account]:
        pass

    @abc.abstractmethod
    def __getitem__(self, chain: Chain) -> Account:
        pass

    def downcast(self) -> AccountIDManager:
        return AccountIDManagerAdapter(self)

    def __contains__(self, chain: Chain) -> bool:
        return self.get(chain) is not None


class SimpleAccountManager(AccountManager):
    __slots__ = ("private_keys",)

    def __init__(
        self,
        *,
        ethereum: Optional[str] = None,
        solana: Optional[str] = None,
        tron: Optional[str] = None,
    ) -> None:
        self.private_keys: dict[type, Optional[str]] = {
            EthereumChain: ethereum,
            SolanaChain: solana,
            TronChain: tron,
        }

    @typing.override
    def get(self, chain: Chain) -> Optional[Account]:
        chain_type = type(chain)

        if not (private_key := self.private_keys.get(chain_type)):
            return None

        return Account.from_str(chain, private_key)

    @typing.override
    def __getitem__(self, chain: Chain) -> Account:
        if not (account := self.get(chain)):
            raise KeyError(f"No private key for {chain}")

        return account


class SimpleAccountIDManager(AccountIDManager):
    __slots__ = ("addresses",)

    @classmethod
    def from_account_id(cls, account_id: AccountID) -> SimpleAccountIDManager:
        chain_type = account_id.chain.coin.NAME.lower()
        return cls(*{chain_type: account_id.address})

    def __init__(
        self,
        *,
        ethereum: Optional[str] = None,
        solana: Optional[str] = None,
        tron: Optional[str] = None,
    ) -> None:
        self.addresses: dict[type, Optional[str]] = {
            EthereumChain: ethereum,
            SolanaChain: solana,
            TronChain: tron,
        }

    @typing.override
    def get(self, chain: Chain) -> Optional[AccountID]:
        chain_type = type(chain)

        if not (address := self.addresses.get(chain_type)):
            return None

        return AccountID.from_str(chain, address)

    @typing.override
    def __getitem__(self, chain: Chain) -> AccountID:
        if not (account_id := self.get(chain)):
            raise KeyError(f"No address for {chain}")

        return account_id


class HDWalletAccountManager(AccountManager):
    __slots__ = ("wallet",)

    def __init__(self, wallet: Wallet) -> None:
        self.wallet = wallet

    @typing.override
    def get(self, chain: Chain) -> Optional[Account]:
        return self[chain]

    @typing.override
    def __getitem__(self, chain: Chain) -> Account:
        return self.wallet.account(chain)
