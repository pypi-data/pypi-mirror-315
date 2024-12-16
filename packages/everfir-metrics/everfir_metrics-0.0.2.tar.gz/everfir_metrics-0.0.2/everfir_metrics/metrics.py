from typing import Optional, List


import everfir_metrics.config.metric_config as metric_config
import everfir_metrics.config.option as option
from everfir_metrics.metrics_manager.metrics import MetricsManager
from everfir_metrics.metrics_manager.metric_info import MetricInfo, MetricName

def init(opts: List[option.Option] = []) -> Optional[Exception]:
    return _metrics_init(opts)

def close():
    global _global_metrics_manager
    _global_metrics_manager = None
    pass

def register(metrics_info: MetricInfo):
    if not _global_metrics_manager:
        return   

    _global_metrics_manager.register(metrics_info)
    pass

def report(metric_name: MetricName, value: float, labels: dict = {}):
    if not _global_metrics_manager:
        return

    _global_metrics_manager.report(metric_name, value, labels)
    pass


_global_metrics_manager: Optional[MetricsManager] = None


def _metrics_init(opts: List[option.Option]) -> Optional[Exception]:
    err: Optional[Exception] = None

    conf:metric_config.Config = metric_config.GetConfig()
    for opt in opts:
        opt(conf)

    err = conf.validate()
    if not err:
        return err

    global _global_metrics_manager
    _global_metrics_manager = MetricsManager(conf)

    return None