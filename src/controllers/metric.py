from src.services.domain.prometheus.measure_summary import set_measure_summary
from flask import Response
from prometheus_client import CollectorRegistry, generate_latest


def index():
    graphs = set_measure_summary()
    res = []
    for k, v in graphs.items():
        res.append(generate_latest(v))

    return Response(res, mimetype="text/plain")
