import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import pandas as pd
import streamlit.components.v1 as components


# ---------------------------------------------------------
# NORMALIZE ISSUE TYPES
# ---------------------------------------------------------
def normalize_issue(value):
    if not isinstance(value, str):
        return "Other"

    v = value.lower()

    if "air" in v:
        return "Air"
    if "noise" in v:
        return "Noise"
    if "heat" in v:
        return "Heat"
    if "odor" in v or "odour" in v:
        return "Odour"
    if "cycling" in v or "walking" in v:
        return "Cycling / Walking"
    if "water" in v or "flood" in v or "drain" in v:
        return "Water"

    return "Other"


# ---------------------------------------------------------
# HYDERABAD-SPECIFIC, INTENSITY-AWARE SOLUTIONS
# ---------------------------------------------------------
def generate_solutions(issue, intensity):
    intensity = int(intensity)

    def tier():
        if intensity <= 2:
            return "low"
        elif intensity == 3:
            return "medium"
        else:
            return "high"

    SOLUTIONS = {

        "Air": {
            "low": {
                "primary": "Monitor air quality trends and local traffic conditions.",
                "additional": [
                    "Encourage public transport and carpooling.",
                    "Inspect nearby construction sites for dust control.",
                    "Promote tree plantation along roads.",
                    "Install temporary dust screens near roadworks.",
                    "Conduct vehicle idling awareness campaigns."
                ]
            },
            "medium": {
                "primary": "Reduce vehicular emissions and construction dust.",
                "additional": [
                    "Restrict heavy vehicle entry during peak hours.",
                    "Mandate water sprinkling at construction sites.",
                    "Improve traffic signal coordination.",
                    "Increase roadside green buffers.",
                    "Carry out spot emission testing."
                ]
            },
            "high": {
                "primary": "Enforce strict air pollution control measures immediately.",
                "additional": [
                    "Suspend high-emission construction activities.",
                    "Declare temporary low-emission zones.",
                    "Deploy mobile air quality monitoring units.",
                    "Penalize industries violating emission norms.",
                    "Coordinate inter-departmental emergency response."
                ]
            }
        },

        "Noise": {
            "low": {
                "primary": "Monitor noise levels and issue advisories.",
                "additional": [
                    "Display noise limit signboards.",
                    "Discourage unnecessary honking.",
                    "Educate shop owners and residents.",
                    "Map recurring noise hotspots."
                ]
            },
            "medium": {
                "primary": "Control traffic and construction-related noise.",
                "additional": [
                    "Restrict construction timings.",
                    "Install temporary noise barriers.",
                    "Deploy traffic marshals.",
                    "Issue warnings to repeat offenders."
                ]
            },
            "high": {
                "primary": "Immediate enforcement against excessive noise sources.",
                "additional": [
                    "Confiscate illegal loudspeakers.",
                    "Impose fines on violations.",
                    "Restrict night-time heavy vehicle movement.",
                    "Install permanent noise barriers.",
                    "Revise zoning rules for sensitive areas."
                ]
            }
        },

        "Heat": {
            "low": {
                "primary": "Provide basic heat relief measures.",
                "additional": [
                    "Install temporary shade structures.",
                    "Ensure drinking water availability.",
                    "Display heat awareness signage.",
                    "Adjust maintenance schedules to cooler hours."
                ]
            },
            "medium": {
                "primary": "Reduce heat exposure through urban design.",
                "additional": [
                    "Install shaded bus stops.",
                    "Increase roadside tree cover.",
                    "Apply reflective coatings on pavements.",
                    "Expand green medians."
                ]
            },
            "high": {
                "primary": "Activate heat mitigation infrastructure urgently.",
                "additional": [
                    "Implement the city Heat Action Plan.",
                    "Promote cool-roof programs.",
                    "Create permanent shaded corridors.",
                    "Set up heat relief centers.",
                    "Coordinate emergency health response."
                ]
            }
        },

        "Odour": {
            "low": {
                "primary": "Inspect sanitation conditions and monitor odor occurrence.",
                "additional": [
                    "Increase waste collection frequency.",
                    "Clean nearby drains.",
                    "Educate residents on waste segregation.",
                    "Monitor open dumping sites."
                ]
            },
            "medium": {
                "primary": "Identify and control odor-generating sources.",
                "additional": [
                    "Deploy sanitation teams for deep cleaning.",
                    "Cover open drains temporarily.",
                    "Improve waste transport logistics.",
                    "Issue notices for improper dumping."
                ]
            },
            "high": {
                "primary": "Immediate sanitation intervention required.",
                "additional": [
                    "Seal chronic dumping hotspots.",
                    "Upgrade waste processing infrastructure.",
                    "Penalize repeat violators.",
                    "Install permanent drain covers.",
                    "Deploy odor-neutralizing treatments."
                ]
            }
        },

        "Cycling / Walking": {
            "low": {
                "primary": "Fix minor pedestrian and cycling issues.",
                "additional": [
                    "Repair footpath cracks.",
                    "Improve signage and markings.",
                    "Clear minor obstructions.",
                    "Enhance crossing visibility."
                ]
            },
            "medium": {
                "primary": "Improve pedestrian and cyclist safety.",
                "additional": [
                    "Upgrade footpaths.",
                    "Improve street lighting.",
                    "Introduce traffic calming measures.",
                    "Add pedestrian refuges."
                ]
            },
            "high": {
                "primary": "Redesign streets for non-motorized transport.",
                "additional": [
                    "Build protected cycling lanes.",
                    "Remove permanent encroachments.",
                    "Implement pedestrian-only zones.",
                    "Reduce vehicle speed limits.",
                    "Revise street hierarchy."
                ]
            }
        },

        "Water": {
            "low": {
                "primary": "Inspect drainage systems.",
                "additional": [
                    "Clear minor blockages.",
                    "Monitor water stagnation.",
                    "Educate residents on drain misuse."
                ]
            },
            "medium": {
                "primary": "Restore proper drainage flow.",
                "additional": [
                    "Desilt drains.",
                    "Repair damaged drainage sections.",
                    "Remove encroachments.",
                    "Improve slope alignment."
                ]
            },
            "high": {
                "primary": "Urgent flood mitigation required.",
                "additional": [
                    "Increase drainage capacity.",
                    "Install pumping systems.",
                    "Restore natural water channels.",
                    "Implement flood early-warning systems.",
                    "Coordinate disaster response teams."
                ]
            }
        },

        "Other": {
            "low": {
                "primary": "Monitor the situation.",
                "additional": ["Collect citizen feedback."]
            },
            "medium": {
                "primary": "Conduct a detailed local assessment.",
                "additional": ["Prepare short-term action plan."]
            },
            "high": {
                "primary": "Plan infrastructure-level intervention.",
                "additional": ["Allocate budget and resources."]
            }
        }
    }

    block = SOLUTIONS.get(issue, SOLUTIONS["Other"])[tier()]
    return block["primary"], block["additional"]


# ---------------------------------------------------------
# RESPONSIBLE AUTHORITIES – HYDERABAD
# ---------------------------------------------------------
AUTHORITIES = {
    "Odour": ("GHMC – Sanitation Department", "040-21111111", "sanitation-ghmc@telangana.gov.in"),
    "Air": ("Telangana Pollution Control Board", "040-23887500", "pcb@telangana.gov.in"),
    "Noise": ("Hyderabad Traffic Police", "100", "trafficpolice@hyderabad.gov.in"),
    "Heat": ("GHMC – Environment Wing", "040-21111111", "environment-ghmc@telangana.gov.in"),
    "Cycling / Walking": ("GHMC – Urban Planning", "040-21111111", "planning-ghmc@telangana.gov.in"),
    "Water": ("GHMC – Engineering Department", "040-21111111", "engineering-ghmc@telangana.gov.in"),
    "Other": ("Greater Hyderabad Municipal Corporation", "040-21111111", "info.ghmc@telangana.gov.in"),
}


# ---------------------------------------------------------
# REQUIRED ENTRY POINT (FIX FOR YOUR ERROR)
# ---------------------------------------------------------
def render(df_all: pd.DataFrame):

    st.title("🗺️ Smart Complaint Solution Map – Hyderabad")

    if df_all is None or df_all.empty:
        st.info("No complaint data available.")
        return

    df = df_all.copy()
    df["issue"] = df["issue_type"].apply(normalize_issue)
    df["intensity"] = df["intensity"].fillna(1).astype(int)

    df = df.sort_values("timestamp")
    latest = df.iloc[-1]

    # ---------------- MAP ----------------
    m = folium.Map(
        location=[latest["lat"], latest["lon"]],
        zoom_start=14
    )

    HeatMap(df[["lat", "lon"]].values.tolist(), radius=25, blur=18).add_to(m)

    for idx, row in df.iterrows():
        primary, _ = generate_solutions(row["issue"], row["intensity"])

        popup_html = f"""
        <div style="width:330px;font-family:Arial;">
            <b>Issue:</b> {row['issue']}<br>
            <b>Intensity:</b> {row['intensity']} / 5<br>
            <b>Reported:</b> {row['timestamp']}<br><br>
            <b>Description:</b><br>{row['description'] or '—'}<br><br>
            <b>Suggested action:</b><br>{primary}
        </div>
        """

        color = "red" if row.name == latest.name else "blue"

        folium.Marker(
            [row["lat"], row["lon"]],
            popup=popup_html,
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(m)

    st_folium(m, width=1400, height=650)

    # ---------------- BOTTOM SOLUTION BOX ----------------
    primary, additional = generate_solutions(latest["issue"], latest["intensity"])
    authority = AUTHORITIES.get(latest["issue"], AUTHORITIES["Other"])

    html = f"""
    <div style="border:1px solid #d6d6d6;border-radius:14px;overflow:hidden;font-family:Arial;">

        <div style="background:#e9e9e9;padding:14px 20px;font-size:18px;font-weight:600;">
            📌 Current Reported Solution
        </div>

        <div style="background:white;padding:22px;font-size:15px;color:#222;">
            <b>Reported Issue:</b> {latest['issue']}<br>
            <b>Intensity:</b> {latest['intensity']} / 5<br>
            <b>Reported on:</b> {latest['timestamp']}<br>

            <hr style="margin:18px 0;">

            <b>Primary suggested action</b><br>
            {primary}

            <br><br>

            <b>Additional actions</b>
            <ul>
                {''.join(f"<li>{s}</li>" for s in additional)}
            </ul>

            <hr style="margin:18px 0;">

            <b>Responsible authority</b><br>
            {authority[0]}<br>
            📞 {authority[1]}<br>
            📧 {authority[2]}
        </div>
    </div>
    """

    components.html(html, height=520)