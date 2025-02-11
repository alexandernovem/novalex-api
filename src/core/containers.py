from dependency_injector import containers, providers
from src.services.conigecko.api import BaseHttpClient, CoingeckoApiService, CoingeckoApiSettings


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["src.controllers.coins"])

    http_client = providers.Factory(BaseHttpClient)
    settings = providers.Factory(CoingeckoApiSettings)
    coingecko_service = providers.Factory(CoingeckoApiService, client=http_client, settings=settings)
