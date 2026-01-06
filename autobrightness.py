#!/usr/bin/python
import dbus
import math
import glob
import os
import json
import time
from datetime import datetime

CONFIG_PATH = "/etc/autobrightness.conf"
LOG_PATH = "/var/log/autobrightness.log"

# Defaults
BACKLIGHT_DEVICE = "acpi_video0"
EMA_ALPHA = 0.05
MIN_BRIGHTNESS = 0.25
MAX_LUX = 500
ALS_INTERVAL = 0.2         # seconds between ALS reads
MAX_CHANGE_PER_SEC = 0.15  # max brightness delta per second


def log(msg):
    try:
        with open(LOG_PATH, "a") as f:
            f.write(f"{datetime.now().isoformat()} {msg}\n")
    except:
        pass


def load_config():
    global BACKLIGHT_DEVICE, EMA_ALPHA, MIN_BRIGHTNESS, MAX_LUX
    try:
        with open(CONFIG_PATH, "r") as f:
            cfg = json.load(f)
            BACKLIGHT_DEVICE = cfg.get("backlight_device", BACKLIGHT_DEVICE)
            EMA_ALPHA = cfg.get("ema_alpha", EMA_ALPHA)
            MIN_BRIGHTNESS = cfg.get("min_brightness", MIN_BRIGHTNESS)
            MAX_LUX = cfg.get("max_lux", MAX_LUX)
    except:
        log("Using default config")


def lux_to_brightness(lux):
    lux = max(1, min(lux, MAX_LUX))
    return MIN_BRIGHTNESS + (1 - MIN_BRIGHTNESS) * (math.log10(lux) / math.log10(MAX_LUX))


def detect_max_brightness(device):
    try:
        with open(f"/sys/class/backlight/{device}/max_brightness", "r") as f:
            return int(f.read().strip())
    except:
        return 100


def set_brightness(device, max_brightness, value):
    percent = int(value * max_brightness)
    try:
        with open(f"/sys/class/backlight/{device}/brightness", "w") as f:
            f.write(str(percent))
    except Exception as e:
        log(f"Error setting brightness: {e}")


def get_lux_gnome():
    try:
        bus = dbus.SystemBus()
        proxy = bus.get_object("net.hadess.SensorProxy", "/net/hadess/SensorProxy")
        sensor = dbus.Interface(proxy, "net.hadess.SensorProxy")
        sensor.ClaimLight()
        iface = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")
        return iface.Get("net.hadess.SensorProxy", "LightLevel")
    except:
        return None


def get_lux_kde():
    try:
        for path in glob.glob("/sys/bus/iio/devices/iio:device*/in_illuminance*"):
            if os.path.isfile(path):
                with open(path, "r") as f:
                    return float(f.read().strip())
    except:
        pass
    return None


def get_lux():
    lux = get_lux_gnome()
    if lux is not None:
        return lux

    lux = get_lux_kde()
    if lux is not None:
        return lux

    return 100


def main():
    load_config()
    max_brightness = detect_max_brightness(BACKLIGHT_DEVICE)
    log(f"Detected max brightness: {max_brightness}")

    ema = None
    target = None

    last_als_time = 0
    last_time = time.time()

    while True:
        now = time.time()
        dt = now - last_time
        last_time = now

        # Read ALS only every ALS_INTERVAL seconds
        if now - last_als_time >= ALS_INTERVAL:
            lux = get_lux()
            target = lux_to_brightness(lux)
            last_als_time = now

        if ema is None:
            ema = target

        # EMA smoothing
        ema = EMA_ALPHA * target + (1 - EMA_ALPHA) * ema

        # Rate limit brightness change per second
        max_step = MAX_CHANGE_PER_SEC * dt
        delta = ema - target
        if abs(delta) > max_step:
            ema = ema - max_step if delta > 0 else ema + max_step

        # Apply brightness
        set_brightness(BACKLIGHT_DEVICE, max_brightness, ema)

        # No sleep → smooth continuous loop


if __name__ == "__main__":
    main()
