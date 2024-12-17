def handle_interrupt(string_or_function):
    def decorator(string, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                if string:
                    print(f"\n{string}")
                else:
                    print(f"\nExiting...")
                exit()
        return wrapper

    if callable(string_or_function):
        string = None
        func = string_or_function
        return lambda: decorator(string, func)()
    else:
        string = string_or_function
        func = None
        return lambda f: decorator(string, f)

