import datetime
from collections import OrderedDict

from django.shortcuts import render

from spaces.fusioncharts import FusionCharts
from spaces.models import ElectricityConsumption


def build_map(request, space_id=1):
    year = request.GET.get('year', datetime.datetime.now().year - 1)

    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = OrderedDict()
    # The `mapConfig` dict contains key-value pairs data for chart attribute
    mapConfig = OrderedDict()
    mapConfig["caption"] = "Потребление электроэнергии по субъектам РФ"
    mapConfig["subcaption"] = year
    mapConfig["numbersuffix"] = "млн кВт/ч"
    mapConfig["includevalueinlabels"] = "1"
    mapConfig["labelsepchar"] = ":"
    mapConfig['theme'] = "fusion"

    # Map color range data
    colorDataObj = {"minvalue": "0.0", "code": "#87CEEB", "gradient": "1",
                    "color": [
                        {"minValue": "5000.0", "maxValue": "10000.0", "code": "#1E90FF"},
                        {"minValue": "10000.0", "maxValue": "20000.0", "code": "#0000FF"},
                        {"minValue": "20000.0", "maxValue": "40000.0", "code": "#00008B"},
                        {"minValue": "30000.0", "maxValue": "80000.0", "code": "#191970"}
                    ]
                    }

    dataSource["chart"] = mapConfig
    dataSource["colorrange"] = colorDataObj

    dataSource['data'] = []
    dataSource['linkeddata'] = []
    for elem in ElectricityConsumption.objects.filter(year=year, space=space_id):
        data = {'id': elem.region.id, 'value': str(elem.consumption), 'showLabel': '0',
                'link': 'newchart:line-json-' + elem.region.id}
        # Create link for each country when a data plot is clicked.
        dataSource['data'].append(data)

        linkData = {'id': elem.region.id}
        # Inititate the linkData for cities drilldown
        linkedchart = {'chart': {
            "caption": "Динамика потребления электроэнергии по годам - " + elem.region.name,
            "yaxisname": "млн кВт/ч",
            "drawcrossline": "0",
            "plothovereffect": "0",
            "anchorradius": "5",
            "theme": "gammel"
        }, 'data': []}

        # Convert the data in the `City` model into a format that can be consumed by FusionCharts.
        # Filtering the data base on the Country Code
        for elem2 in ElectricityConsumption.objects.filter(region=elem.region, space=space_id).order_by('year'):
            arrData = {'label': elem2.year, 'value': str(elem2.consumption)}
            linkedchart['data'].append(arrData)

        linkData['linkedchart'] = linkedchart
        dataSource['linkeddata'].append(linkData)

    fusionMap = FusionCharts("maps/russia", "ex1", "650", "450", "chart-1", "json", dataSource)

    return fusionMap
