from typing import List

from everfir_metrics.util.metric import exponential_buckets

MetricType = int
MT_COUNTER = 1
MT_GAUGE = 2
MT_HISTOGRAM = 3
MT_SUMMARY = 4

MetricName = str
def metric_name(name: str) -> MetricName:
    return name

class MetricInfo:
    def __init__(
            self, 
            metric_type: MetricType, 
            name: MetricName, 
            help: str = "", 
            labels: List[str] = [], # 自定义标签
            buckets: List[float] = exponential_buckets(1, 2, 10),  # 默认对数桶，范围「1-512」
        ):

        self.metric_type: MetricType = metric_type
        
        self.help: str = help
        self.name: MetricName = name
        self.labels: List[str] = labels
        self.buckets: List[float] = buckets
        pass
