import subprocess


def change_mode(mode):
    if mode == "dark":
        subprocess.call(
            [
                "osascript",
                "-e",
                'tell application "System Events" to tell appearance preferences to set dark mode to true',
            ]
        )
    elif mode == "light":
        subprocess.call(
            [
                "osascript",
                "-e",
                'tell application "System Events" to tell appearance preferences to set dark mode to false',
            ]
        )
    else:
        print("Invalid mode")


def get_current_mode():
    result = subprocess.run(
        [
            "osascript",
            "-e",
            'tell application "System Events" to tell appearance preferences to get dark mode',
        ],
        stdout=subprocess.PIPE,
    )
    current_mode = result.stdout.strip().decode("utf-8")
    return current_mode


if __name__ == "__main__":
    current_mode = get_current_mode()
    if current_mode == "true":
        change_mode("light")
    elif current_mode == "false":
        change_mode("dark")
    else:
        print("Could not determine current mode")
