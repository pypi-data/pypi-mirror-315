import os
import subprocess

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

    print("\033[38;5;12m🎉 Tmux Configuration Setup Complete..! 🎉\n🌟 SL Android Official ™\n💻 Package Developed by IM COOL BOOY 🌟\033[0m")
    print("Tmux setup has been successfully configured!")
