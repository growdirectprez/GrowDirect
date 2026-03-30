---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# WORK ORDER B-029 — Pi Demo Station
*Owner: Will · Side Project · No sprint SLA*

**Created:** February 25, 2026
**Assigned to:** Will
**Priority:** 🟢 LOW — side project, no sprint impact
**TRIAGE ref:** B-029

---

## What You're Building

A self-contained Raspberry Pi demo station. You have everything you need in the box — this work order walks you through putting it together and getting it running. No prior experience required. This is a great first hardware project and you'll learn a lot.

The end goal: a Pi with a touchscreen that boots to a clean desktop, connected to WiFi, and ready to be used as a local demo or kiosk-style display. Down the road this could run a Canary demo interface, but for now: get it alive and usable.

---

## Hardware You Have

| Item | What It Is |
|---|---|
| Raspberry Pi (3B or 4) in official black case | The computer. Already in its case. |
| Power supply (wall adapter) + cables | USB-C or micro-USB power, HDMI cable |
| Kuman MHS 3.5" touch display (X001YFIYOP) | Small SPI touchscreen — mounts directly on GPIO pins |
| 7" Capacitive Touch Screen for Raspberry Pi | Larger HDMI touchscreen — connects via HDMI + USB |
| Freenove Ultimate Starter Kit FNK0020 (sealed) | Sensors, LEDs, breadboard, camera, jumper wires — don't open yet, this is for later |

**Start with the 7" touchscreen** — it connects via HDMI + USB and works out of the box with no driver headaches. The 3.5" Kuman screen requires SPI configuration and is more advanced. Save that for phase 2.

---

## What You Need to Get

Before you start, you need one thing that isn't in the box:

**A microSD card** — 32GB minimum, 64GB recommended. Class 10 / A1 or better. ~$10 on Amazon (Samsung or SanDisk are both fine). This is the "hard drive" for the Pi.

You also need a way to write an OS image to the microSD card. Use another computer (Mac or Windows) for this.

---

## Phase 1 — Flash the OS

1. On another computer, download **Raspberry Pi Imager**: https://www.raspberrypi.com/software/
2. Insert the microSD card into the computer (you may need a USB card reader — ~$8 on Amazon if you don't have one)
3. Open Raspberry Pi Imager:
   - **Choose Device:** Raspberry Pi 4 (or Pi 3 if that's what you have — check the board, it's printed on it)
   - **Choose OS:** Raspberry Pi OS (64-bit) — the full desktop version
   - **Choose Storage:** your microSD card
4. Click the gear icon (⚙️) before writing — this lets you pre-configure:
   - Set a hostname (e.g., `canary-pi`)
   - Set a username and password (write these down)
   - Configure your WiFi network (SSID + password)
   - Enable SSH (check the box)
5. Click **Write** and wait (~5-10 minutes)
6. When done, eject the card safely

---

## Phase 2 — First Boot

1. Insert the microSD card into the Pi (slot is on the underside)
2. Connect the 7" touchscreen:
   - HDMI cable from Pi to screen
   - USB cable from screen's USB port to Pi (powers the touch function)
   - Screen's power adapter if it has one
3. Connect a USB keyboard and mouse (just for first boot — optional later)
4. Plug in the Pi's power supply last

The Pi will boot. First boot takes 2-3 minutes while it expands the filesystem. You'll see the Raspberry Pi desktop appear on the 7" screen.

**If the screen is rotated:** Don't panic. Go to Preferences → Screen Configuration and rotate 180°, or edit `/boot/config.txt` to add `display_rotate=2`.

---

## Phase 3 — Get Connected and Updated

Once you're at the desktop:

1. Connect to WiFi if you didn't pre-configure it (WiFi icon in the top-right)
2. Open Terminal and run:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
   This takes 5-10 minutes. Let it run.
3. Reboot when done:
   ```bash
   sudo reboot
   ```

---

## Phase 4 — Verify and Report Back

Once you're up and running, send ALX (or Jeffe) a photo of the screen showing the desktop and your terminal output from:

```bash
uname -a
hostname -I
```

This confirms: what Pi model you have, what OS version, and the IP address. That's all ALX needs to know it's alive.

---

## What Comes Next (Don't Do This Yet)

Once Phase 4 is done and reported, the options are:

- **Canary kiosk mode:** Configure the Pi to boot directly into a fullscreen browser pointing at a local Canary demo URL
- **3.5" Kuman screen:** Get the smaller screen working for a more compact form factor (requires SPI driver install — Jeremy can help)
- **Freenove Starter Kit:** Learn GPIO, sensors, LEDs — completely separate educational track, fun for its own sake

---

## If You Get Stuck

Common issues and quick fixes:

| Problem | Fix |
|---|---|
| Screen is black | Check HDMI connection, try a different HDMI port on Pi if there are two |
| Pi won't boot (red light, no green blink) | Power supply issue — try a different cable or adapter |
| Pi boots but no WiFi | Check you typed the SSID and password exactly right in Imager (case-sensitive) |
| Touch not working | Make sure the USB cable from the screen is connected to the Pi, not just to power |

If none of those work — ping ALX. Don't spend more than 15 minutes stuck on the same thing.

---

## Notes for ALX

- Pi model needs to be confirmed — check the board label (BCM2711 = Pi 4, BCM2837 = Pi 3B)
- The 7" screen brand is unknown (generic packaging) — confirm it's HDMI+USB touch before Phase 2
- Freenove kit is sealed — leave it until Will has basic Pi working, then it's a great next step
- This is a learning project for Will. Don't rush it. The goal is him being comfortable with the hardware.

---

*Work order written by ALX · February 25, 2026*
