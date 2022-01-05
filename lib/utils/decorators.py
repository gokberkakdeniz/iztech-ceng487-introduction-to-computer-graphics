# CENG 487 Assignment7 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021


def with_exec_count(start, end):
    frame = start

    def decorator(fn):
        def wrapped(*args, **kwargs):
            nonlocal frame

            frame = ((frame-start+1) % (end-start)) + start

            new_args = (args[0], frame, *args[1:])

            return fn(*new_args, **kwargs)

        return wrapped

    return decorator
