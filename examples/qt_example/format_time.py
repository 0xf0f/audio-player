def format_time(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    result = f'{minutes:02}:{seconds:02}.{milliseconds:03}'
    if hours:
        result = f'{hours:02}:{result}'

    return result
