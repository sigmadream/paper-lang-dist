"""Reusable RTT experiments, versioned profiles and offline analysis.

Extensions register metrics, policies, aggregators or providers before loading
the experiment configuration. Importing this package never contacts a model.
"""

from .metrics import Metric, MetricContext, register_metric
from .profiles import load_profile
from .profiles import register_profile
from .policies import DecisionPolicy, register_policy
from .aggregation import Aggregator, register_aggregator
from rttdist.providers import register_provider

__all__ = ["Metric", "MetricContext", "register_metric", "load_profile", "register_profile",
           "DecisionPolicy", "register_policy", "Aggregator", "register_aggregator", "register_provider"]
