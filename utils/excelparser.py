import json
import os

from pyexcel_xls import get_data as xls_get

from minenergo.settings import BASE_DIR
from spaces.models import Region, ElectricityConsumption, Space


def parse_excel_into_consumption_objects(file, request, space_id=None):
    space = Space.objects.get(pk=space_id)
    data = list(xls_get(file).items())[0][1]
    regions = Region.objects.all()

    with open(os.path.join(BASE_DIR, 'static', "utils/regions_ids.json"), encoding='utf-8') as json_file:
        regions_ids = json.load(json_file)

    substrings = ["область", "республика", "г.", "край", "автономный округ", "федеральный округ"]
    for rownum in range(len(data)):
        if len(data[rownum]) > 1:
            if any([substring in data[rownum][0].lower() for substring in substrings]):
                if data[rownum][0] not in regions.values_list('name', flat=True):
                    try:
                        region = Region.objects.create(
                            id=regions_ids[data[rownum][0]],
                            name=data[rownum][0]
                        )
                    except KeyError:
                        continue
                else:
                    for reg in regions:
                        if reg.name == data[rownum][0]:
                            region = reg
                for colnum in range(len(data[rownum])):
                    if isinstance(data[3][colnum], int):
                        year = data[3][colnum]
                        if isinstance(data[rownum][colnum], float) or isinstance(data[rownum][colnum], int):
                            consumption = data[rownum][colnum]
                        else:
                            continue
                        _, created = ElectricityConsumption.objects.update_or_create(
                            year=year,
                            region=region,
                            space=space,
                            defaults={"consumption": consumption, "created_by": request.user}
                        )