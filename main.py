import subprocess
import urwid
import re
import warnings

warnings.filterwarnings("ignore")  # Suppress all warnings

def get_xinput_devices():
    result = subprocess.run(
        ["xinput", "list"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )
    lines = result.stdout.splitlines()
    devices = []
    pattern = re.compile(r"^\s*(?P<name>.+?)\s+id=(?P<id>\d+)")
    for line in lines:
        match = pattern.search(line)
        if match:
            devices.append({
                "name": match.group("name").strip(),
                "id": match.group("id").strip(),
            })
    return devices

def is_device_enabled(device_id: str) -> bool:
    result = subprocess.run(
        ["xinput", "list-props", device_id],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )
    match = re.search(r"Device Enabled \(\d+\):\s+(\d)", result.stdout)
    return match and match.group(1) == "1"

def set_device_enabled(device_id: str, enable: bool):
    subprocess.run(
        ["xinput", "enable" if enable else "disable", device_id],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

class XInputToggler:
    def __init__(self):
        self.devices = get_xinput_devices()
        self.body = urwid.SimpleFocusListWalker([])
        self.listbox = urwid.ListBox(self.body)
        self.build_menu()

        self.main = urwid.Padding(self.listbox, left=2, right=2)
        self.top = urwid.Overlay(
            self.main,
            urwid.SolidFill("\N{MEDIUM SHADE}"),
            align=urwid.CENTER,
            width=(urwid.RELATIVE, 60),
            valign=urwid.MIDDLE,
            height=(urwid.RELATIVE, 60),
            min_width=20,
            min_height=9,
        )
        self.loop = urwid.MainLoop(
            self.top,
            palette=[("reversed", "standout", "")],
            unhandled_input=self.handle_keys
        )

    def build_menu(self):
        self.body.clear()
        self.body.append(urwid.Text("XInput Devices (Y to enable, N to disable, Q to quit)"))
        self.body.append(urwid.Divider())
        for device in self.devices:
            enabled = is_device_enabled(device["id"])
            label = f"[{'X' if enabled else ' '}] {device['name']} (id={device['id']})"
            button = urwid.Button(label)
            urwid.connect_signal(button, "click", self.device_selected, user_args=[device])
            self.body.append(urwid.AttrMap(button, None, focus_map="reversed"))

    def device_selected(self, button, device):
        pass  # No-op for click events

    def handle_keys(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        elif key in ('y', 'Y', 'n', 'N'):
            focus_widget, idx = self.listbox.get_focus()
            if idx is None or idx < 2:
                return  # Ignore header and divider
            device = self.devices[idx - 2]
            set_device_enabled(device["id"], key.lower() == 'y')
            self.build_menu()
            self.listbox.set_focus(idx)

    def run(self):
        self.loop.run()

if __name__ == "__main__":
    XInputToggler().run()
