"""
Author: Samuel Lehmann
Network with him at: https://www.linkedin.com/in/samuellehmann/
"""

import pandas as pd
from dataclasses import make_dataclass

field = make_dataclass("Category", [("Text", str), ("Graphable", bool)])

FIELDS = pd.DataFrame([field("Category", False), field("Type", False), field("Subcategory", False),
                       field("Sub-Subcategory", False) , field("Mechanical Property Data Source(s)", False),
                       field("Name", False), field("Treatment or Temper", False),
                       field("Treatment Temperature (F)", True),field("Treatment Temperature (C)", True),
                       field("Minimum Ultimate Tensile Strength (psi)", True),
                       field("Maximum Ultimate Tensile Strength (psi)", True),
                       field("Ultimate Tensile Strength (psi)", True), field("Minimum Yield Strength (psi)", True),
                       field("Maximum Yield Strength (psi)", True), field("Yield Strength (psi)", True),
                       field("Minimum Ultimate Tensile Strength (MPa)", True),
                       field("Maximum Ultimate Tensile Strength (MPa)", True),
                       field("Ultimate Tensile Strength (MPa)", True), field("Minimum Yield Strength (MPa)", True),
                       field("Maximum Yield Strength (MPa)", True), field("Yield Strength (MPa)", True),
                       field("Minimum Elongation (%)", True), field("Maximum Elongation (%)", True),
                       field("Elongation (%)", True), field("Reduction in Cross Sectional Area (%)", True),
                       field("Brinell Hardness", True), field("Rockwell Hardness", False),
                       field("Izod Impact Strength (Ft-lb)", True), field("Izod Impact Strength (N-m)", True),
                       field("Water Quenched?", False), field("Ultimate Shearing Strength (ksi)", True),
                       field("Ultimate Shearing Strength (Mpa)", True), field("Endurance limit (ksi)", True),
                       field("Endurance limit (MPa)", True)])

TEXT = ("Category", "Type", "Subcategory", "Sub-Subcategory", "Mechanical Property Data Source(s)", "Name",
        "Treatment or Temper", "Treatment Temperature (F)", "Treatment Temperature (C)",
        "Minimum Ultimate Tensile Strength (psi)", "Maximum Ultimate Tensile Strength (psi)",
        "Ultimate Tensile Strength (psi)", "Minimum Yield Strength (psi)", "Maximum Yield Strength (psi)",
        "Yield Strength (psi)", "Minimum Ultimate Tensile Strength (MPa)", "Maximum Ultimate Tensile Strength (MPa)",
        "Ultimate Tensile Strength (MPa)", "Minimum Yield Strength (MPa)", "Maximum Yield Strength (MPa)",
        "Yield Strength (MPa)", "Minimum Elongation (%)", "Maximum Elongation (%)", "Elongation (%)",
        "Reduction in Cross Sectional Area (%)", "Brinell Hardness", "Rockwell Hardness",
        "Izod Impact Stength (Ft-lb)", "Izod Impact Stength (N-m)", "Water Quenched?",
        "Ultimate Shearing Strength (ksi)", "Ultimate Shearing Strength (Mpa)", "Endurance limit (ksi)",
        "Endurance limit (MPa)")

CATEGORY = 0
TYPE = 1
SUBCATEGORY = 2
SUB_SUBCATEGORY = 3
DATA_SOURCE = 4
NAME = 5
TREATMENT = 6
TREATMENT_TEMP_F = 7
TREATMENT_TEMP_C = 8
MIN_UTS_PSI = 9
MAX_UTS_PSI = 10
UTS_PSI = 11
MIN_YS_PSI = 12
MAX_YS_PSI = 13
YS_PSI = 14
MIN_UTS_MPA = 15
MAX_UTS_MPA = 16
UTS_MPA = 17
MIN_YS_MPA = 18
MAX_YS_MPA = 19
YS_MPA = 20
MIN_ELONGATION = 21
MAX_ELONGATION = 22
ELONGATION = 23
CSA_REDUCTION = 24
BRINELL_HARDNESS = 25
ROCKWELL_HARDNESS = 26
IZOD_IMPACT_FTLB = 27
IZOD_IMPACT_NM = 28
QUENCHED = 29
ULT_SHEAR_PSI = 30
ULT_SHEAR_MPA = 31
ENDURANCE_LIMIT_KSI = 32
ENDURANCE_LIMIT_MPA = 33


def get_text(enum_val):
    return FIELDS['Text'][enum_val]
