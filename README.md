# DJI FPV Statistics extractor

> This project is still a WIP, I'll update it whenever I want, feel free to contribute

## What is this

Simple python script extracting `MIN`, `MAX` and `AVG` from a .SRT file. Designed for the DJI FPV **headset** data.

Probably works with other drones data, GeoLocation def not supported yet (everything rounds to 2 digits).

> You should be able to find the .SRT file of your fly records together with the videos, on the FPV's headset.

## Usage

> python parse.py -i <yourFile.SRT>

## Example output

```uwu
~$ > python parse.py -i DJIG0000.srt
Analyzed  3436  items, with  12  variables
Showing non-NULL only

---
glsBat
avg :  8.04      .V
min :  7.4       .V
max :  9.1       .V
---

delay
avg :  35.01     ms
min :  25.0      ms
max :  88.0      ms
---

bitrate
avg :  42.71     .Mbps
min :  2.4       .Mbps
max :  50.8      .Mbps
---

Height
avg :  6.56      .m
min :  0.0       .m
max :  79.1      .m
---

Distance
avg :  74.68     .m
min :  0.0       .m
max :  418.5     .m
---

HS
avg :  8.15      .m/s
min :  0.0       .m/s
max :  32.3      .m/s
---

VS
avg :  1.76      .m/s
min :  0.0       .m/s
max :  28.0      .m/s
---

gpsNum
avg :  22.39
min :  13.0
max :  24.0
---
```