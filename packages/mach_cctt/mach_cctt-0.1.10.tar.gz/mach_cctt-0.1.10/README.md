# Cross Chain Trade Test (CCTT)

Test automated trades between multiple chains on Mach.

[PyPI](https://pypi.org/project/mach-cctt/)

[Test PyPI](https://test.pypi.org/project/mach-cctt/)

## Overview

Test automated trades on Mach. Specify a start chain and symbol, and a destination policy determining how the destination token will be chosen. In each trade, the test wallet's entire balance of the source token will be sold for the destination token, and then the destination token becomes the new source token for the next trade. This continues until the script is killed by the user, or there are no more tokens yielded by the destination policy.

## Usage

1. Install

    ```bash
    # If using pip
    python -m pip install mach-cctt
    # If using uv
    uv pip install mach-cctt
    ```

1. Usage

    ```bash
    cctt --help
    ```

1. Example

    ```bash
    # The script will create log files. Recommended to create a directory for it.
    mkdir cctt/ && cd cctt/

    # Fill in this config file according to the template. Make sure you fill in the accounts section with your private keys.
    touch config.yaml
    export CONFIG_PATH=config.yaml

    # Show balances of all your accounts
    cctt balances

    # Test trading USDC between random chains, starting from Optimism-USDC
    cctt run --source Optimism-USDC --destination-policy fixed:USDC

    # Test trading USDC on only Arbitrum and Optimism, but fund the test by selling your Polygon-USDC balance
    cctt run --source Polygon-USDC --destination-policy cheap:USDC

    # Trade between random tokens on random chains, starting from Arbitrum-USDT
    cctt run --source Arbitrum-USDT --destination-policy random
    
    # If the --source is made explicitly empty, then whatever token has the highest value balance in your accounts is automatically chosen as the source
    cctt run  --destination-policy random

    # Once you're done, you can set withdrawal addresses in the config file and withdraw the funds from the test accounts into the withdraw addresses. Note that gas is not withdrawn.
    cctt withdraw
    ```

    Notes:

    - You need to have a gas on every chain, or a gas of exactly 0 on chains that you do not wish the testing script to trade on, which will cause those chains to be disabled.

## Destination Policies

| **CLI Flag**                    | **Example**                                          | **Name in Code**                | **Description**                                                                                                                                                                            |
|---------------------------------|------------------------------------------------------|---------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--destination fixed:<SYMBOL>`  | `--destination fixed:USDC`                           | `RandomChainFixedSymbolPolicy`  | Trade the token with symbol `<SYMBOL>` on random chains in a random order                                                                                                                  |
| `--destination cheap:<SYMBOL>`  | `--destination cheap:WETH`                           | `CheapChainFixedSymbolPolicy`   | Trade the token with symbol `<SYMBOL>` on only chains with "cheap" gas. Currently hardcoded to only Arbitrum and Optimism.                                                                            |
| `--destination random`          | `--destination random`                               | `RandomTokenPolicy` | Trade completely random tokens in a random order                                                                                                                                           |
| N/A                             | N/A                                                  | `TokenIteratorPolicy`           | Takes a sequence of tokens and trades exactly those tokens in that order                                                                                                                   |
| `--destination chains:<CHAINS>` | `--destination chains:Arbitrum,Optimism,Base,Solana` | `SingleChainPolicy`             | Trades all tokens in the given list of chains `<CHAINS>`. Trades all tokens on one chain in a random order, and trades between chains in a random order. Used to test single-chain trades. |
