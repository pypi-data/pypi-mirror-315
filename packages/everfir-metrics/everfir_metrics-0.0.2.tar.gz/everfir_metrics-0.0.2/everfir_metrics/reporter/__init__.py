from everfir_metrics.config.metric_config import Config, RT_COLLECTOR, RT_PUSHGATEWAY
from everfir_metrics.reporter import abstract
from everfir_metrics.reporter import collecotr_reporter
from everfir_metrics.reporter import push_gateway_reporter

def NewReporter(metrics_registry: collecotr_reporter.CollectorRegistry, conf: Config) -> abstract.Reporter:
    if conf.report_type == RT_COLLECTOR:
        return collecotr_reporter.CollectorReporter(metrics_registry, conf)
    elif conf.report_type == RT_PUSHGATEWAY:
        return push_gateway_reporter.PushGatewayReporter(metrics_registry, conf)