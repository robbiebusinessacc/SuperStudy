import subprocess


def open_spotify():
    subprocess.run(["open", "-a", "Spotify"])


if __name__ == '__main__':
    open_spotify()
