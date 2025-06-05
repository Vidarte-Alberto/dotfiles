# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, qtile, hook, widget
from libqtile.config import Click, Drag, Group, Key, Match, hook, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.widget import backlight

mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("sh -c ~/.config/rofi/scripts/launcher"), desc="Spawn a command using a prompt widget"),
    Key([mod], "p", lazy.spawn("sh -c ~/.config/rofi/scripts/power"), desc="Spawn a command using a prompt widget"),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s +15%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 15%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%"), desc="Aumentar volumen"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%"), desc="Disminuir volumen"),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc="Mutear/desmutear volumen"),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Reproducir/Pausar medios"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Siguiente pista de medios"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Pista anterior de medios"),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop"), desc="Detener reproducción de medios"),
    Key([], "Print", lazy.spawn("flameshot gui"), desc="Launch Flameshot GUI for screenshot"),
    Key([mod], "Print", lazy.spawn("flameshot full -p ~/Pictures/Screenshots/$(date +%Y-%m-%d-%H-%M-%S).png"), desc="Capture full screen with Flameshot and save"),
    Key([mod, "shift"], "Print", lazy.spawn("flameshot full -p ~/Pictures/Screenshots/$(date +%Y-%m-%d-%H-%M-%S).png --active"), desc="Capture active window with Flameshot and save"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

lay_config = {
    "border_width": 0,
    "margin": 9,
    "border_focus": "3b4252",
    "border_normal": "3b4252",
    "font": "FiraCode Nerd Font",
    "grow_amount": 2,
}

layouts = [
    # layout.MonadWide(**lay_config),
    layout.Bsp(**lay_config, fair=False, border_on_single=True),
    layout.Columns(
        **lay_config,
        border_on_single=True,
        num_columns=2,
        split=False,
    ),
    # Plasma(lay_config, border_normal_fixed='#3b4252', border_focus_fixed='#3b4252', border_width_single=3),
    # layout.RatioTile(**lay_config),
    # layout.VerticalTile(**lay_config),
    # layout.Matrix(**lay_config, columns=3),
    # layout.Zoomy(**lay_config),
    # layout.Slice(**lay_config, width=1920, fallback=layout.TreeTab(), match=Match(wm_class="joplin"), side="right"),
    # layout.MonadTall(**lay_config),
    # layout.Tile(shift_windows=True, **lay_config),
    # layout.Stack(num_stacks=2, **lay_config),
    layout.Floating(**lay_config),
    layout.Max(**lay_config),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

def search():
    qtile.spawn("rofi -show drun")

def power():
    qtile.spawn("sh -c ~/.config/rofi/scripts/power")

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.Spacer(length=15,
                    background='#282738',
                ),

                widget.Image(
                    filename='~/.config/qtile/Assets/launch_Icon.png',
                    margin=2,
                    background='#282738',
                    mouse_callbacks={"Button1": power},
                ),
                widget.Image(
                    filename='~/.config/qtile/Assets/6.png',
                ),
                widget.GroupBox(
                    font="JetBrainsMono Nerd Font",
                    fontsize=24,
                    borderwidth=3,
                    highlight_method='block',
                    active='#CAA9E0',
                    block_highlight_text_color="#91B1F0",
                    highlight_color='#353446',
                    inactive='#282738',
                    foreground='#4B427E',
                    background='#353446',
                    this_current_screen_border='#353446',
                    this_screen_border='#353446',
                    other_current_screen_border='#353446',
                    other_screen_border='#353446',
                    urgent_border='#353446',
                    rounded=True,
                    disable_drag=True,
                ),

                widget.Spacer(
                    length=8,
                    background='#353446',
                ),

                widget.Image(
                    filename='~/.config/qtile/Assets/1.png',
                ),
                widget.CurrentLayoutIcon(
                    custom_icon_paths=["~/.config/qtile/Assets/layout"],
                    background='#353446',
                    scale=0.50,
                ),
                widget.Image(
                    filename='~/.config/qtile/Assets/5.png',
                ),

                widget.TextBox(
                    text=" ",
                    font="Font Awesome 6 Free Solid",
                    fontsize=13,
                    background='#282738',
                    foreground='#CAA9E0',
                    mouse_callbacks={"Button1": search},
                ),

                widget.TextBox(
                    fmt='Search',
                    background='#282738',
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                    foreground='#CAA9E0',
                    mouse_callbacks={"Button1": search},
                ),

                widget.Image(
                    filename='~/.config/qtile/Assets/4.png',
                ),

                widget.WindowName(
                    background='#353446',
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                    empty_group_string="Desktop",
                    max_chars=130,
                    foreground='#CAA9E0',
                ),

                widget.Image(
                    filename='~/.config/qtile/Assets/3.png',
                ),

                widget.Systray(
                    background='#282738',
                    fontsize=2,
                ),

                widget.TextBox(
                    text=' ',
                    background='#282738',
                ),

                widget.Image(
                    filename='~/.config/qtile/Assets/6.png',
                    background='#353446',
                ),
                widget.Battery(
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                    background='#353446',
                    foreground='#CAA9E0',
                    format='{percent:2.0%}',
                ),
                widget.Image(
                    filename='~/.config/qtile/Assets/2.png',
                ),

                widget.Spacer(
                    length=8,
                    background='#353446',
                ),

                widget.TextBox(
                    text=" ",
                    font="Font Awesome 6 Free Solid",
                    fontsize=13,
                    background='#353446',
                    foreground='#CAA9E0',
                ),

                widget.Volume(
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                    background='#353446',
                    foreground='#CAA9E0',
                ),

                widget.Image(
                    filename='~/.config/qtile/Assets/5.png',
                    background='#353446',
                ),

                widget.TextBox(
                    text=" ",
                    font="Font Awesome 6 Free Solid",
                    fontsize=13,
                    background='#282738',
                    foreground='#CAA9E0',
                ),

                widget.Clock(
                    format='%I:%M %p',
                    background='#282738',
                    foreground='#CAA9E0',
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                ),

                widget.Spacer(
                    length=18,
                    background='#282738',
                ),
            ],
            30,
            border_color='#282738',
            border_width=[0,0,0,0],
            margin=[15,60,6,60],

        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
	border_focus='#1F1D2E',
	border_normal='#1F1D2E',
	border_width=0,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)


import os
import subprocess
# stuff
@hook.subscribe.startup_once
def autostart():
    subprocess.call([os.path.expanduser('.config/qtile/autostart_once.sh')])

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
