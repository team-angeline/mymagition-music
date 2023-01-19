from flask import Response


def make_file_response(
        data: bytes,
        mimetype: str,
        filename: str,
        content_type: str = 'aapplication/octet-stream') -> Response:

    response = Response(response=data,
                        mimetype=mimetype,
                        content_type=content_type)
    response.headers['Content-Diposition'] = f'attachment; filename={filename}'
    return response