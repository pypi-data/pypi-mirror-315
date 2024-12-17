import asyncio
import logging
import sys
from dataclasses import dataclass
from typing import List, Optional, TypedDict

from python_ifconfig_me.core.ipretriever import DEFAULT_IP_RETRIEVERS
from python_ifconfig_me.utils.async_ import run_async

if sys.version_info >= (3, 11):
    from typing import Unpack
else:
    from typing_extensions import Unpack

import aiohttp

from python_ifconfig_me.core.ipretriever.ipRetriever import (
    IPResultObject,
    IPRetriever,
    IPRetrieverContext,
)
from python_ifconfig_me.core.vote.votingStrategy import (
    SimpleVotingStrategy,
    VotingResult,
    VotingStrategyContext,
)

logger = logging.getLogger(__name__)
rootLogger = logging.getLogger(__name__.split(".")[0])
rootLogger.setLevel(logging.ERROR)


@dataclass
class GetPublicIPOptions:
    return_statistics: bool = False
    ipv6: bool = False
    ipv4: bool = False
    prefer_ipv6: bool = False
    timeout: int = 5


class RetrieveIPsAsyncKwargs(TypedDict):
    timeout: int


async def retrieveIPsAsync(
    ipRetrievers: List[IPRetriever],
    **kwargs: Unpack[RetrieveIPsAsyncKwargs],
) -> List[IPResultObject]:
    timeout = kwargs.get("timeout", 5)
    context = IPRetrieverContext(session=aiohttp.ClientSession(), timeout=timeout)
    async with context.session:
        tasks = [ipRetriever.getIPAsync(context) for ipRetriever in ipRetrievers]
        results = await asyncio.gather(*tasks)

    return results


async def getPublicIPAsync(
    options: Optional[GetPublicIPOptions] = None,
    ipRetrievers: Optional[List[IPRetriever]] = None,
    votingStrategy: Optional[SimpleVotingStrategy] = None,
) -> Optional[VotingResult]:
    if options is None:
        options = GetPublicIPOptions()
    if ipRetrievers is None:
        ipRetrievers = DEFAULT_IP_RETRIEVERS
    ipResults = await retrieveIPsAsync(ipRetrievers, timeout=options.timeout)
    context = VotingStrategyContext(
        prefer_ipv6=options.prefer_ipv6,
        ipv4=options.ipv4,
        ipv6=options.ipv6,
        return_statistics=options.return_statistics,
    )
    if votingStrategy is None:
        votingStrategy = SimpleVotingStrategy()
    votingResult = votingStrategy.vote(ipResults, context)
    return votingResult


def getPublicIP(*args, **kwargs):
    return run_async(getPublicIPAsync, *args, **kwargs)
