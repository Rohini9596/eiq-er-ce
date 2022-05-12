# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

from polylogyx.utils.compat import with_metaclass


class AbstractAlerterPlugin(with_metaclass(ABCMeta)):
    """
    AbstractAlerterPlugin is the base class for all alerters in PolyLogyx. It
    defines the interface that an alerter should implement in order to support
    sending an alert.
    """

    @abstractmethod
    def handle_alert(self, node, match, intel_match):
        raise NotImplementedError()  # pragma: no cover
