![alt text](https://raw.githubusercontent.com/umutaktepe/AeroTools/master/icons/AeroToolsHeader.png "AeroTools")

# AeroTools

[![Pyup Status](https://pyup.io/repos/github/umutaktepe/AeroTools/shield.svg?t=1572373789737)](https://pyup.io/account/repos/github/umutaktepe/AeroTools/) [![GitHub issues](https://img.shields.io/github/issues/umutaktepe/AeroTools)](https://github.com/umutaktepe/AeroTools/issues) [![Known Vulnerabilities](https://snyk.io/test/github/umutaktepe/AeroTools/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/umutaktepe/AeroTools?targetFile=requirements.txt) [![GitHub license](https://img.shields.io/github/license/umutaktepe/AeroTools)](https://github.com/umutaktepe/AeroTools/blob/master/LICENSE)

AeroTools is a modular Python toolset designed for aerodynamic calculations and performance analysis. It allows you to:

  - Calculate complex aerodynamics equations
  - Plot performance graphs / charts
  - Export data to Excel

#### Capabilities

**Calculations:**
  - Takeoff and landing speeds
  - Takeoff and landing distances
  - Thrust and power required at specific velocities
  - Wing loading and aspect ratio

**Plotting:**
  - Lift coefficient vs Velocity
  - Thrust required vs Velocity
  - Power required vs Velocity
  - Drag vs Velocity
  - Lift-to-drag ratio vs Velocity
  - Thrust available vs Thrust required

AeroTools allows for performance calculations of scaled and model UAVs, providing reliable data based on standard aerospace industry equations.

#### Usage

AeroTools requires Python 3+ and the packages specified in `requirements.txt`.

1. **Install Dependencies:**

```sh
pip install -r requirements.txt
```

Alternatively, install packages manually:
```sh
pip install PyQt5 numpy XlsxWriter matplotlib xlrd xlwt
```

2. **Clone the Repository:**

```sh
git clone https://github.com/umutaktepe/AeroTools.git
cd AeroTools
```

3. **Run the Application:**

```sh
python main.py
```

4. **Enjoy!**

#### Todos

 - Add more graphs to plot
 - Translate to Turkish
 - Add unit tests

License
----

GNU General Public License v3.0

**Enjoy your free software. If you want to develop it, contributions are appreciated! :)**
