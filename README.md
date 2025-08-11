# urxinput
#### A command line "front end" for [xinput](https://linux.die.net/man/1/xinput) written in python. 

****************

### Introduction

This mini project all started due to a bug I experienced on my personal laptop. My mouse pointer would jet offscreen unexpectedly. The issue was solved by disabling the touch screen functionality via xinput. This python script is a result of the need to enable or disable the touch screen quickly. It can be used to enable or disable any io device detected by xinput. The user interface resembles [menuconfig](https://en.wikipedia.org/wiki/Menuconfig).

### Usage

You may need to install xinput if you havent already.

*debian/ubuntu
```bash
sudo apt update && sudo apt install xinput
```
Using UV:

```bash
git clone https://github.com/vlshields/UrXinput.git
cd UrXinput
uv sync
uv run main.py
```
You can also install via the released .deb file from this repo.

```bash
sudo apt install ./urxinput_0.1.0_amd64.deb
```
### A note about display protocols

There seems to be minimal support for the wayland protocol, but it might produce unexpected results. This tool is most compatible with x11.


