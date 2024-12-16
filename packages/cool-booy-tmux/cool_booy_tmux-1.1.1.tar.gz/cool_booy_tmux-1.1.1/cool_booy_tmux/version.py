# version.py

__version__ = "1.1.1"

def get_version():
    """
    This function returns the version of the cool-booy-tmux tool.
    """
    return __version__

if __name__ == "__main__":

    print(f"cool-booy-tmux version {get_version()}")
