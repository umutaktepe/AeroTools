![alt text](https://raw.githubusercontent.com/umutaktepe/AeroTools/master/icons/AeroToolsHeader.png "AeroTools")

# AeroTools

[![Pyup Status](https://pyup.io/repos/github/umutaktepe/AeroTools/shield.svg?t=1572373789737)](https://pyup.io/account/repos/github/umutaktepe/AeroTools/) [![GitHub issues](https://img.shields.io/github/issues/umutaktepe/AeroTools)](https://github.com/umutaktepe/AeroTools/issues) [![Known Vulnerabilities](https://snyk.io/test/github/umutaktepe/AeroTools/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/umutaktepe/AeroTools?targetFile=requirements.txt) [![GitHub license](https://img.shields.io/github/license/umutaktepe/AeroTools)](https://github.com/umutaktepe/AeroTools/blob/master/LICENSE)

AeroTools is a toolset written in Python. It allows you to:

  - Calculate some complex aerodynamics related equations
  - Plot certain performance graphs

#### What can you calculate?
  - Takeoff and landing speeds
  - Takeoff and landing distances
  - Thrust and power required in certain velocities
  - Wing loading and aspect ratio
  - Breguet Range and Endurance for Propeller and Jet-Engine aircrafts

#### What can you plot?
  - Lift coefficient vs Velocity graph
  - Thrust required vs Velocity graph
  - Power required vs Velocity graph
  - Drag vs Velocity graph
  - Lift-to-drag ratio vs Velocity graph
  - Thrust available vs Thrust required graph
  
AeroTools can also be used for performance calculations of scaled and model UAVs as well. It provides reliable data based on the equations provided in aerospace industry.

#### Usage

AeroTools requires Python 3+ and the packages which are specified in [requirements file.](/requirements.txt "Required Python Packages")

1. To install the necessary packages:

```sh
$ pip3 install PyQt5
$ pip3 install numpy
$ pip3 install XlsxWriter
$ pip3 install matplotlib
$ pip3 install xlrd
$ pip3 install xlwt
```
**or you can use your own IDE to install the packages.*

2. Get clone in Linux terminal:

```sh
$ git clone https://github.com/umutaktepe/AeroTools.git
```

3. Go to the directory:

```sh
$ cd AeroTools
```

4. Run AeroTools.py:

```sh
$ python3 AeroTools.py
```

5. Enjoy it!


#### Todos

 - Add more graphs to plot
 - Translate in Turkish

License
----

GNU General Public License v3.0

**Enjoy your free software. If you want to develop it, it will be appreciated :)**
