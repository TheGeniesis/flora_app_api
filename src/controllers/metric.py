from src.services.domain.prometheus.measure_summary import set_measure_summary

from prometheus_client import CollectorRegistry, generate_latest


def index():
    registry = CollectorRegistry()
    set_measure_summary(registry)

    return generate_latest(registry)
