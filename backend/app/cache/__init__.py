from simple_cache import SimpleCache
from simple_cache.providers import DetaProvider

# full documentation in: https://github.com/AdaiasMagdiel/simple-cache
provider = DetaProvider()
cache = SimpleCache(provider=provider)
