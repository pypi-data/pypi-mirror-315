WEB_APP_ROOT = "https://app.cocos.capital"
API_ROOT = "https://api.cocos.capital/api"

# URLs categorizadas
WEB_APP_URLS = {
    "login": f"{WEB_APP_ROOT}/login",
    "portfolio": f"{WEB_APP_ROOT}/capital-portfolio",
    "dashboard": f"{WEB_APP_ROOT}/",
    "orders": f"{WEB_APP_ROOT}/orders",
    "movements": f"{WEB_APP_ROOT}/movements",
    "market_bonds_corp": f"{WEB_APP_ROOT}/market/BONOS_CORP",
    "market_bonds_public": f"{WEB_APP_ROOT}/market/BONOS_PUBLICOS",
    "market_stocks": f"{WEB_APP_ROOT}/market/ACCIONES",
    "market_cedears": f"{WEB_APP_ROOT}/market/CEDEARS",
    "market_letters": f"{WEB_APP_ROOT}/market/LETRAS",
    "market_caucion": f"{WEB_APP_ROOT}/market/CAUCION",
    "market_fci": f"{WEB_APP_ROOT}/market/FCI",
    "market_favorites": f"{WEB_APP_ROOT}/market/Favoritos"
}

API_URLS = {
    "portfolio_balance": f"{API_ROOT}/portfolio/balance?currency=ARS&period=MAX",
    "mep_prices": f"{API_ROOT}/v1/public/mep-prices",
    "user_data": f"{API_ROOT}/v1/users/me"
}
