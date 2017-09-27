def application(env, start_res):
    start_res("200 OK", [("Content-Type", "text/html")])
    return [b"Hello uwsgi!"]
