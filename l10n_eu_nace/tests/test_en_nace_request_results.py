# Copyright 2024 Moduon Team S.L. <info@moduon.team>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
import json
from functools import reduce

from requests.models import Response

NACE_COMMON = [
    {
        "code": {
            "type": "typed-literal",
            "datatype": "http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral",
            "value": "01",
        },
        "parentCode": {
            "type": "typed-literal",
            "datatype": "http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral",
            "value": "A",
        },
    },
    {
        "code": {
            "type": "typed-literal",
            "datatype": "http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral",
            "value": "01.1",
        },
        "parentCode": {
            "type": "typed-literal",
            "datatype": "http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral",
            "value": "01",
        },
    },
    {
        "code": {
            "type": "typed-literal",
            "datatype": "http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral",
            "value": "01.11",
        },
        "parentCode": {
            "type": "typed-literal",
            "datatype": "http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral",
            "value": "01.1",
        },
    },
    {
        "code": {
            "type": "typed-literal",
            "datatype": "http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral",
            "value": "02",
        },
        "parentCode": {
            "type": "typed-literal",
            "datatype": "http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral",
            "value": "A",
        },
    },
    {
        "code": {
            "type": "typed-literal",
            "datatype": "http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral",
            "value": "A",
        }
    },
]

NACE_ES = [
    {
        "ES": {
            "type": "literal",
            "value": "01 Agricultura, ganadería, caza y servicios relacionados\
                  con las mismas",
        }
    },
    {"ES": {"type": "literal", "value": "01.1 Cultivos no perennes"}},
    {
        "ES": {
            "type": "literal",
            "value": "01.11 Cultivo de cereales (excepto arroz), \
                leguminosas y semillas oleaginosas",
        }
    },
    {
        "ES": {
            "type": "literal",
            "value": "02 Silvicultura y explotación \
            forestal",
        }
    },
]

NACE_EN = [
    {
        "EN": {
            "type": "literal",
            "value": "01 Crop and animal production, hunting and related \
                service activities",
        }
    },
    {"EN": {"type": "literal", "value": "01.1 Growing of non-perennial crops"}},
    {
        "EN": {
            "type": "literal",
            "value": "01.11 Growing of cereals (except rice), leguminous crops \
                and oil seeds",
        }
    },
    {"EN": {"type": "literal", "value": "02 Forestry and logging"}},
]

NACE_FR = [
    {
        "FR": {
            "type": "literal",
            "value": "01 Culture et production animale, chasse et services \
                annexes",
        }
    },
    {"FR": {"type": "literal", "value": "01.1 Cultures non permanentes"}},
    {
        "FR": {
            "type": "literal",
            "value": "01.11 Culture de céréales (à l'exception du riz), de \
                légumineuses et de graines oléagineuses",
        }
    },
    {
        "FR": {
            "type": "literal",
            "value": "02 Sylviculture et exploitation \
            forestière",
        }
    },
]


def create_response(*lists):
    response = Response()
    response.code = "200"
    response.status_code = 200
    merged_lists = list(zip(*lists))
    bindings = [reduce(lambda acc, new: {**acc, **new}, item) for item in merged_lists]
    content = {
        "head": {},
        "results": {"distinct": False, "ordered": True, "bindings": bindings},
    }
    response._content = json.dumps(content).encode()
    return response
