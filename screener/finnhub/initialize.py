import finnhub

from lib.postgres_db import EPortalPGDB
from private.keys import finn_hubb_key

configuration = finnhub.Configuration(
    api_key={
        'token': finn_hubb_key.get('api')
    }
)

finnhub_client = finnhub.DefaultApi(finnhub.ApiClient(configuration))
pg_db = EPortalPGDB.Instance()