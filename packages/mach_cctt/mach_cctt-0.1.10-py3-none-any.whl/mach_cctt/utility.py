from decimal import Decimal
import itertools

from mach_client import AccountIDManager, AssetServer, Chain, Token
from mach_client.client.asset_server.types import UserAssetData


NEGATIVE_INFINITY = Decimal("-inf")


async def choose_source_token(
    client: AssetServer,
    token_choices: dict[Chain, set[Token]],
    accounts: AccountIDManager,
) -> Token:
    raw_balances = await client.get_all_raw_token_balances(accounts)

    balances = [
        balances for chain, balances in raw_balances.items() if chain in token_choices
    ]

    def key(data: UserAssetData) -> Decimal:
        chain = data.chain.to_chain()

        if data.address == "native":
            return NEGATIVE_INFINITY

        token = Token.try_lookup_address(chain, data.address)

        if token not in token_choices[chain] or not data.price:
            return NEGATIVE_INFINITY

        return token.to_coins(data.balance) * data.price

    max_value = max(itertools.chain(*balances), key=key)

    return Token.lookup_address(max_value.chain.to_chain(), max_value.address)
