# FM-Transfer

![PyPI - Status](https://img.shields.io/pypi/status/fm-transfer)
![PyPI - License](https://img.shields.io/pypi/l/fm-transfer?color=blue)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fm-transfer)

## A graphical front-end to send/receive binary by audio

![Main Window](doc/window.png "FM-Transfer Main Window")
![Main Window Sending](doc/window2.png "FM-Transfer Main Window Sending")

`fm-transfer` is a graphical front-end written in Python that allows you to send and receive files through a transceiver.
It is designed to directly control the push-to-talk button of devices via a serial port (not mandatory).

The `PTT` control happens via a serial interface, by raising/lowering the `DSR` or the 
`RTS` serial signals. A simple circuit can read the status of one of these signals and trigger the `PTT`.

This hardware is **NOT** mandatory, so you can use this tool without any transceiver: it can be used to 
send/receive data through an audio interface (es. via a cable connecting default sound port output to default 
sound input, or using one instance on a first PC which plays the sound and a second instance on another PC which listens
with a microphone).

Transmission and reception are performed using two other python packages:
1) `gg-transfer` (https://github.com/matteotenca/gg-transfer) which uses `C/C++` library
[ggwave](https://github.com/ggerganov/ggwave/) (using `pip`, a fork of mine is required/installed, [ggwave-wheels](https://github.com/matteotenca/ggwave-wheels/))
2) `quiet-transfer` (https://github.com/matteotenca/quiet-transfer), 
which uses `C/C++` library [quiet-lib](https://github.com/quiet/quiet)

The former implements FSK modulation, the latter implements a lot of modulation algorithms, including GMSK and QAM.

Please see the related repositories for more information about those tools.

### Installation

The simplest way to install `fm-transfer` and all the needed tools is via `pip`:

```bash
$> pip install fm-transfer
```

`fm-transfer` is pure-python, but its dependencies may need a compiler. See [gg-transfer](https://github.com/matteotenca/gg-transfer) 
and [quiet-transfer](https://github.com/matteotenca/quiet-transfer) repos for more info. 

### Usage

#### *Tool* and *Send protocol* boxes

This radio buttons allows you to switch between `gg-transfer` and `quiet-transfer` commands to send/receive data. Each
utility supports different protocols.

For FM transmission, `gg-transfer` mode is way more robust but way slower. In good conditions, `quiet-lib` mode and 
`audible` protocol will provide much faster speed. `quiet-lib` needs some bandwidth, 20 Khz should be ok. When using a 
direct audio cable connection, `quiet-lib` in `cable-64k` mode will provide the highest speed. 

The `zlib compression` is available in `quiet-lib` mode only and enables the compression/decompression of the data. 
**Note**: This breaks the progress bar indications. 

#### Buttons
- `Choose a serial port...` allows to select a serial device to handle the `PTT` (see below). It is not mandatory to
select a serial device to use the application.
- `Check signal` button is available if a valid serial port is chosen. When pressed, the current status of `DSR` and `DTR` 
serial signals are read and printed.
- `Rechck Serial Ports` button forces a rescan of the available serial ports. It is useful if you connect a USB-to-serial
adapter and you want it to appear in the serial device list to choose from.
- `Choose send file` and `Send file` are self-explanatory.
- `Choose recv file` and `Receive file` are self-explanatory too, but note that the chosen file will be overwritten and
that the reception process may time out if no valid data is received in a while. 
- `Receive` and `Send` buttons on the bottom can be used to receive/send a short (144 chars max) text message. 
`gg-transfer` mode is enforced. The received message is written in the console, not in the output file.

#### *PTT* management

**Note**: A serial device is NOT mandatory to use the application.

If you want to manage the `PTT` of your radio from the application, you will need:

1) a serial device
2) a simple circuit with a transistor or rele
3) a proper cable to connect the latter to the transceiver.

It all works by rising or lowering the `DTR` or the `DSR` signal (selectable from the `Signal` box) of the serial device, 
which in turn make the transistor/rele to close or open the contact which triggers the `PTT`.

Circuit's and connector's schematics will be provided soon.

Usually, when set to high from software, a serial device's `DTR` or `DSR` signal's voltage goes up to `3.5v` or `5v`. 
Sometimes the opposite happens, i.e. setting the signal to high lowers the voltage to zero. Since this behaviour is not 
predictable, the `Reverse logic` checkbox comes in hand, inverting the high state with the low state. If the radio starts 
transmitting as soon as you start the application with `Unpressed` selected, try to activate this checkbox and/or change 
the signal.
