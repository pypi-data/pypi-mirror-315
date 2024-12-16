import subprocess
import os
import sys
from colorama import init, Fore

init(autoreset=True)

def print_help():
    print(Fore.CYAN + """
Usage: cool-booy-tmux [options]

Options:
  -h, --help         Show this help message
  -s, --setup        Set up the tmux configuration
  -v, --version      Show the version of the tool

Example:
  cool-booy-tmux -s   # To set up tmux configuration
  cool-booy-tmux -v   # To view the version
    """)

def create_tmux_config():
    tmux_conf = os.path.expanduser('~/.tmux.conf')

    if not os.path.exists(tmux_conf):
        with open(tmux_conf, 'w') as f:
            f.write('set -g status-bg "#2E3440"\n')
            f.write('set -g status-fg "#E5E9F0"\n')
            f.write('set -g status-interval 1\n')
            f.write('set -g status-left-length 50\n')
            f.write('set -g status-right-length 50\n')
            f.write('set -g status-left "#[fg=#81A1C1]📅 #[fg=#7F00FF]%Y-%m-%d #[fg=#008000]%A #[fg=#E0115F]%H:%M:%S"\n')
            f.write('set -g status-right "#[fg=#A3BE8C]🔋#[fg=#E5E9F0] #(battery_percentage) #[fg=#2AAA8A]Load: #[fg=#FFC000]#(uptime)#[fg=#88C0D0] ⚙️"\n')

    with open(os.path.expanduser('~/.bashrc'), 'a') as f:
        f.write('if [ -z "$TMUX" ]; then\n')
        f.write('  tmux\n')
        f.write('fi\n')

    subprocess.run(['source', os.path.expanduser('~/.bashrc')], shell=True)

    print(Fore.GREEN + "\033[38;5;12m🎉 Tmux Configuration Setup Complete..! 🎉\n🌟 SL Android Official ™\n💻 Package Developed by IM COOL BOOY 🌟\033[0m")
    print(Fore.YELLOW + "Tmux setup has been successfully configured!")

def main():
    if len(sys.argv) == 1:
        print_help()
        return

    if sys.argv[1] in ('-h', '--help'):
        print_help()
    elif sys.argv[1] in ('-s', '--setup'):
        create_tmux_config()
    elif sys.argv[1] in ('-v', '--version'):
        print(Fore.CYAN + "cool-booy-tmux version 1.1.1")
    else:
        print(Fore.RED + "Invalid option. Use '-h' for help.")

if __name__ == "__main__":
    main()
