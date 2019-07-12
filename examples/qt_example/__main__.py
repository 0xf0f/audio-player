if __name__ == '__main__':
    from examples.qt_example import qt
    from examples.qt_example.audio_player_window import AudioPlayerWindow

    import sys
    from pathlib import Path

    cd: Path = Path(__file__).parent
    sys.path.append(str(cd))
    # sys.path.append(str(cd.parent))
    sys.path.append(str(cd.parent.parent))

    # from quicklogger.templates import DefaultLoggingTemplate
    # lg = DefaultLoggingTemplate()
    # lg.intercept_except_hook()
    # lg.outs = (
    #     open('log.txt', 'a'),
    #     sys.stderr
    # )

    app = qt.QApplication(sys.argv)

    audio_player_window = AudioPlayerWindow()
    audio_player_window.show()

    app.exec()
