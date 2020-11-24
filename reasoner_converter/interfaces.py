"""TRAPI interface conversions."""
from functools import wraps

from .downgrading import downgrade_Message, downgrade_Query
from .upgrading import upgrade_Query, upgrade_Message


def downgrade_reasoner(fcn):
    """Make a 1.0.0 reasoner look like a 0.9.2 reasoner.
    
    fcn is a 1.0.0 interface
    data is a 0.9.2 paylod
    """
    @wraps(fcn)
    def wrapped(data):
        return downgrade_Message(fcn(upgrade_Query(data))["message"])
    return wrapped


def upgrade_reasoner(fcn):
    """Make a 0.9.2 reasoner look like a 1.0.0 reasoner.
    
    fcn is a 0.9.2 interface
    data is a 1.0.0 paylod
    """
    @wraps(fcn)
    def wrapped(data):
        return {"message": upgrade_Message(fcn(downgrade_Query(data)))}
    return wrapped
