from flask import abort


def validate_token(req, config):
    """
    @request: flask.request
    @return: bool
    @raise: HTTPException
    """

    token = req.args.get('token')

    try:
        assert token is not None

        if token != config['token']:
            abort(403, description="Bad security token")
        else:
            return True

    except AssertionError:
        abort(403, description="Missing security token")


def validate_request(req, args) -> dict:
    """
    Validates whether the list of required arguments are in the request
    @param req: flask.request
    @param args: dict with argument name and if it is required
    @return: dict with param map
    """

    params = {}
    try:
        for arg in args:
            required_param = req.args.get(arg)
            assert required_param is not None
            params[arg] = required_param

        return params

    except AssertionError:
        abort(400)
