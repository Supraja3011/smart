import streamlit as st

def render():
    st.markdown(
        """
        <style>
        .about-container { max-width: 900px; width: 100%; padding: 20px 18px; margin:auto; }
        .section {
            background: #ffffff;
            border: 1px solid #e6eef5;
            padding: 18px 22px;
            border-radius: 12px;
            margin-bottom: 18px;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
        }
        .title { font-size: 1.25rem; font-weight: 700; color: #0b4f8a; margin-bottom: 8px; }
        .lead { font-size: 1rem; color:#1f2937; line-height: 1.55; }
        .tag {
            background:#eef6ff; color:#083e73; padding:6px 10px; border-radius:8px;
            margin:6px 6px 6px 0; font-size:0.86rem; display:inline-block;
        }
        .cta {
            background: linear-gradient(90deg,#0b6bd6,#06b6d4);
            color:white !important; padding:12px 20px; border-radius:10px;
            text-decoration:none; font-weight:600;
            display:inline-block;
        }
        .footer { color:#6b7280; text-align:center; margin-top:12px; font-size:0.92rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="about-container">', unsafe_allow_html=True)

    st.header("ℹ️ About the Project")

    # Overview
    st.markdown(
        """
        <div class="section">
            <div class="title">Project Overview</div>
            <div class="lead">
                This platform is a citizen-centric initiative designed for the city of <strong>Hyderabad, India</strong>. 
                Our mission is to bridge the gap between residents and urban management.
                <br><br>
                The project provides an <strong>interactive map</strong> where Hyderabadis can share everyday 
                urban challenges, such as air quality issues, noise pollution, excessive heat, 
                or unsafe walking and cycling infrastructure.
                <br><br>
                Our goal is to leverage citizen-powered data to visualize neighborhood-level 
                experiences and highlight exactly where the city needs attention.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Purpose
    st.markdown(
        """
        <div class="section">
            <div class="title">Purpose</div>
            <div class="lead">
                Hyderabad is a rapidly growing metropolis. Many localized issues—like 
                micro-heat islands or specific traffic noise corridors—often go unnoticed 
                by large-scale sensors.
                <br><br>
                This tool makes it easy for anyone in Hyderabad to:
            </div>
            <ul class="lead">
                <li>Report environmental issues directly from their location</li>
                <li>Mark the exact spot on the Hyderabad map</li>
                <li>View trending issues reported by fellow citizens</li>
                <li>Generate automated emails to relevant city authorities</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Categories
    st.markdown(
        """
        <div class="section">
            <div class="title">Issue Categories</div>
            <div class="lead">Reports are organized to help identify patterns across the GHMC area:</div>
            <br>
            <span class="tag">Air Quality</span>
            <span class="tag">Noise</span>
            <span class="tag">Heat</span>
            <span class="tag">Cycling / Walking</span>
            <span class="tag">Odor</span>
            <span class="tag">Other</span>
            <br><br>
            <div class="lead">
                These categories help authorities and urban planners see which areas of Hyderabad 
                benefit most from greening, noise barriers, or better sanitation.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Technologies
    st.markdown(
        """
        <div class="section">
            <div class="title">Technologies Used</div>
            <div class="lead">
                Built with a modern, lightweight stack:
            </div>
            <ul class="lead">
                <li><strong>Streamlit</strong> for the responsive interface</li>
                <li><strong>Folium</strong> for the Hyderabad-centered map</li>
                <li><strong>SQLite</strong> for secure report storage</li>
                <li><strong>Nominatim API</strong> for Hyderabad address searches</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Data Expander
    with st.expander("Data & Map Details"):
        st.write(
            """
            • Each report is timestamped and geotagged within Hyderabad city limits.
            • We use clustering to group reports in dense areas like Ameerpet, Hitech City, or Secunderabad.
            • Heatmaps are generated to show 'hotspots' of specific complaints.
            • All data is used to help citizens visualize the health of their local environment.
            """
        )

    st.markdown("<hr />", unsafe_allow_html=True)

    # CTA
    st.markdown(
        """
        <div style="text-align:center; margin-top:14px;">
            <a href="/" target="_self" class="cta"> Go to the Map & Report an Issue</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<p class="footer">© 2024 | Hyderabad Smart Complaint Map Initiative</p>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)