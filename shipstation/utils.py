def require_type(item, required_type, message=""):
    if item is None:
        return
    if not isinstance(item, required_type):
        if message:
            raise AttributeError(message)
        raise AttributeError("must be of type {}".format(required_type))
