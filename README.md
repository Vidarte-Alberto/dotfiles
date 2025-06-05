# 🐧 Debian Rice - Dotfiles

My personal Debian configuration with custom dotfiles for a clean and productive environment.

## 📸 Screenshots

## 🛠️ Components

### Window Manager / Desktop Environment
- **WM/DE**: qtile
- **Compositor**: picom

### Terminal and Shell
- **Terminal**: alacritty
- **Shell**: zsh
- **Prompt**: oh-my-zsh

### Main Applications
- **Editor**: nvim
- **Launcher**: rofi

## 📦 Installation

### Prerequisites
```bash
# Update the system
sudo apt update && sudo apt upgrade -y

# Install git if not already installed
sudo apt install git -y
```

### Manual Installation
```bash
# Backup existing configurations
mkdir -p ~/.config/backup
cp -r ~/.config/* ~/.config/backup/ 2>/dev/null || true

# Copy dotfiles
cp -r .config/* ~/.config/

# Install dependencies
sudo apt install qtile picom alacritty zsh rofi neovim fonts-firacode fonts-font-awesome
```

## 🔧 Post-installation Setup

### Fonts
```bash
# Install necessary fonts
sudo apt install fonts-firacode fonts-font-awesome

# Or download custom fonts
mkdir -p ~/.local/share/fonts
cp fonts/* ~/.local/share/fonts/
fc-cache -fv
```

### Oh My Zsh Installation
```bash
# Install Oh My Zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Change default shell to zsh
chsh -s $(which zsh)
```

### Services and Daemons
```bash
# Enable necessary services
systemctl --user enable picom
systemctl --user start picom
```

## 📁 Repository Structure

```
.
├── .config/
│   ├── alacritty/          # Terminal configuration
│   ├── nvim/               # Neovim configuration
│   ├── rofi/               # Launcher configuration
│   ├── qtile/              # Qtile window manager config
│   └── picom/              # Compositor configuration
├── .zshrc                  # Zsh configuration
├── fonts/                  # Custom fonts
├── wallpapers/             # Wallpapers
├── screenshots/            # Setup screenshots
└── README.md               # This file
```

## 🎨 Customization

### Changing Color Themes
Edit the configuration files in `.config/` to change color palettes:
- Terminal: `.config/alacritty/alacritty.yml`
- Editor: `.config/nvim/init.vim`
- Qtile: `.config/qtile/config.py`

### Keybindings
Main keybindings are defined in:
- Window Manager: `.config/qtile/config.py`
- Shell: `.zshrc`

## 🐛 Troubleshooting

### Common Issues

**Error: Font not found**
```bash
fc-cache -fv
```

**Configuration not applying**
```bash
# Restart session or reload configuration
source ~/.zshrc
```

**Incorrect permissions**
```bash
chmod +x scripts/*.sh
```

**Qtile not starting**
```bash
# Check qtile configuration
qtile check
```

## 🤝 Contributing

Contributions are welcome! If you have improvements or fixes:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Contact

- **GitHub**: [@Vidarte-Alberto](https://github.com/vidarte-alberto)
- **Email**: chekin_vr@hotmail.com

## ⭐ Acknowledgments

- [r/unixporn Community](https://reddit.com/r/unixporn)
- [Darkkal44](https://github.com/Darkkal44/Cozytile/tree/main) - My rice is a fork of Cozytile
- All developers of the tools used

---

**Like my setup?** Give the repository a ⭐!
