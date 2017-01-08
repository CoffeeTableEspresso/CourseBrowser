class ParseException(Exception):
    """Raised when we have trouble parsing Pre-reqs."""
    pass

class ArgumentException(Exception):
    """Raised when allof or oneof is passed more than one keyword argument."""
    pass

class AndOrException(Exception):
    """Raised when Node.andor is given something other than "and" or "or" as
       its value."""
    pass

class MissingException(Exception):
    """Raised when some value to be returned is missing."""
    pass
