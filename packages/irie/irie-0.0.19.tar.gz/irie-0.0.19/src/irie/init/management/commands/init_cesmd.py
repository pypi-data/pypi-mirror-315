import irie
import numpy as np
from irie.apps.inventory.models  import Asset
from pathlib import Path
from django.core.management.base import BaseCommand
import json

DATA = Path(irie.__file__).parents[0]/"init"/"data"

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(DATA/"cgs-stations.json") as f:
            stations = json.load(f)

        for station in stations["features"]:
            loc = station["geometry"]["coordinates"]
            loc = [loc[1], loc[0]]
            for asset in Asset.objects.all():
                if np.allclose(loc, list(asset.coordinates), rtol=1e-8, atol=1e-03):
                    props = station["properties"]
                    cesmd = f"{props['network']}{props['code']}"

                    print(asset, cesmd)
                    continue

