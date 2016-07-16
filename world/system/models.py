"""
Models specific to the system/deep backend integration of DH3.
"""
class CachingModel(object):
    """
    Caching models are data objects built above normal objects. These data-only objects
    contain a Time-To-Live variable which specifies when this data has become "unreliable".

    Once the TTL has passed, it's important to refresh the data object with new data.
    """
    def __init__(self, ttl=900):
        """
        Initializer for caching model.
        Args:
            ttl: The amount of time the object is valid for.
        """
        self.ttl = ttl