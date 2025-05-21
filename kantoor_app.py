import streamlit as st
import random
import datetime

# App titel en configuratie
st.set_page_config(page_title="Kantoor Zomerkamp App", layout="wide")

# CSS voor een kantoor-achtige look
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
        padding: 20px;
    }
    h1, h2, h3 {
        color: #0d47a1;
    }
    .stButton>button {
        background-color: #0d47a1;
        color: white;
        border-radius: 5px;
        padding: 8px 16px;
    }
    .stTextArea>div>div>textarea {
        border: 1px solid #0d47a1;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialiseer session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'klacht_stage' not in st.session_state:
    st.session_state.klacht_stage = 0

# Slider-resetfunctie voor CAPTCHA
def reset_other_slider(changed_slider):
    if changed_slider == 1 and st.session_state.slider2 > 0:
        st.session_state.slider2 = 0
    elif changed_slider == 2 and st.session_state.slider1 > 0:
        st.session_state.slider1 = 0

# Standaard antwoorden
vrij_antwoorden = ["A", "B", "C", "D", "E", "F", "G", "H"]
opslag_antwoorden = ["A", "B", "C", "D", "E", "F", "G", "H"]
feedback_antwoorden = ["A", "B", "C", "D", "E", "F", "G", "H"]

# Verwerkingsfunctie

def verwerk_verzoek(tekst, antwoordenlijst, type_aanvraag):
    if len(tekst.split()) < 15:
        st.error("Gebruik minimaal 15 woorden.")
    else:
        antwoord = random.choice(antwoordenlijst)
        st.success(f"Ingediend! Reactie: {antwoord}")
        st.session_state.history.append({
            "type": type_aanvraag,
            "verzoek": tekst,
            "antwoord": antwoord,
        })

# Header
st.title("📝 Kantoor App")
st.subheader("Welkom bij het digitale kantoor")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Vrij aanvragen", "Opslag aanvragen", "Klacht indienen", "Feedback geven", "Geschiedenis"])

# Tab 1: Vrij aanvragen
with tab1:
    st.header("Verlof aanvragen")
    vrij_verzoek = st.text_area("Waarom wilt u vrij?", height=150, key="vrij_text")
    if st.button("Indienen", key="submit_vrij"):
        verwerk_verzoek(vrij_verzoek, vrij_antwoorden, "Verlof aanvraag")

# Tab 2: Opslag aanvragen
with tab2:
    st.header("Opslag aanvragen")
    opslag_verzoek = st.text_area("Waarom verdien je een opslag?", height=150, key="opslag_text")
    if st.button("Indienen", key="submit_opslag"):
        verwerk_verzoek(opslag_verzoek, opslag_antwoorden, "Opslag aanvraag")

# Tab 3: Klacht indienen
with tab3:
    st.header("Klacht indienen")
    if st.session_state.klacht_stage == 0:
        st.write("Vul het formulier in om een klacht in te dienen")
        with st.form("klacht_form"):
            col1, col2 = st.columns(2)
            with col1:
                naam = st.text_input("Naam", key="naam_klacht")
                achternaam = st.text_input("Achternaam", key="achternaam_klacht")
                functie = st.text_input("Functie", key="functie_klacht")
                salaris = st.number_input("Salaris (€)", min_value=0, key="salaris_klacht")
            with col2:
                fav_kampleiding = st.text_input("Favoriete kampleiding", key="fav_kampleiding_klacht")
                geboortedatum = st.date_input("Geboortedatum", key="geboortedatum_klacht")
                fav_spel = st.text_input("Je favoriete spel", key="fav_spel_klacht")
                som = st.number_input("9 + 10 =", key="som_klacht")
                thema = st.text_input("Wat denk je dat het thema wordt dit jaar?", key="thema_klacht")
            if st.form_submit_button("Verzenden"):
                all_filled = all([naam, achternaam, functie, salaris > 0, fav_kampleiding, fav_spel, som, thema])
                if not all_filled:
                    st.error("Alle velden zijn verplicht!")
                elif fav_kampleiding.lower() != "hajo":
                    st.error("Je hebt je vergist bij je favoriete kampleiding. Het moet 'Hajo' zijn.")
                elif som != 19:
                    st.error("9 + 10 = 19. Probeer het opnieuw.")
                else:
                    st.session_state.klacht_stage = 1
                    st.session_state.form_data = {
                        "naam": naam,
                        "achternaam": achternaam,
                        "functie": functie,
                        "salaris": salaris,
                        "fav_kampleiding": fav_kampleiding,
                        "geboortedatum": geboortedatum,
                        "fav_spel": fav_spel,
                        "som": som,
                        "thema": thema
                    }
                    st.experimental_rerun()
    elif st.session_state.klacht_stage == 1:
        st.write("Bevestig je identiteit")
        with st.form("confirm_form_klacht"):
            bevestig_naam = st.text_input("Volledige naam", key="bevestig_naam_klacht")
            vandaag = st.date_input("Datum van vandaag", datetime.date.today(), key="vandaag_klacht")
            if st.form_submit_button("Bevestigen"):
                if not bevestig_naam or vandaag != datetime.date.today():
                    st.error("Vul je naam in en selecteer de huidige datum")
                else:
                    st.session_state.klacht_stage = 2
                    st.session_state.bevestiging = {
                        "naam": bevestig_naam,
                        "datum": vandaag
                    }
                    st.experimental_rerun()
    elif st.session_state.klacht_stage == 2:
        st.write("CAPTCHA Verificatie")
        st.warning("Sleep beide sliders helemaal naar rechts om je klacht te verzenden")
        if 'slider1' not in st.session_state:
            st.session_state.slider1 = 0
        if 'slider2' not in st.session_state:
            st.session_state.slider2 = 0
        st.slider("Beweeg naar rechts (1)", 0, 100, value=st.session_state.slider1, key="slider1", on_change=reset_other_slider, args=(1,))
        st.slider("Beweeg naar rechts (2)", 0, 100, value=st.session_state.slider2, key="slider2", on_change=reset_other_slider, args=(2,))
        if st.button("Klacht toch verzenden (dit is eigenlijk onmogelijk)"):
            st.success("Klacht succesvol verzonden! (maar eigenlijk is dit onmogelijk)")
            st.session_state.history.append({
                "type": "Klacht",
                "verzoek": f"Klacht van {st.session_state.form_data['naam']} {st.session_state.form_data['achternaam']}",
                "antwoord": "Klacht ontvangen en zal worden verwerkt."
            })
            st.session_state.klacht_stage = 0
            st.experimental_rerun()
        if st.button("Annuleren"):
            st.session_state.klacht_stage = 0
            st.experimental_rerun()

# Tab 4: Feedback geven
with tab4:
    st.header("Feedback geven aan het kantoor")
    feedback_verzoek = st.text_area("Wat is je feedback?", height=150, key="feedback_text")
    if st.button("Indienen", key="submit_feedback"):
        verwerk_verzoek(feedback_verzoek, feedback_antwoorden, "Feedback")

# Tab 5: Geschiedenis
with tab5:
    st.header("Geschiedenis van aanvragen")
    if not st.session_state.history:
        st.info("Je hebt nog geen aanvragen of klachten ingediend.")
    else:
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"{item['type']} #{len(st.session_state.history) - i}"):
                st.write(f"**Verzoek/Klacht:** {item['verzoek']}")
                st.write(f"**Antwoord:** {item['antwoord']}")
                st.write("---")

# Footer
st.markdown("---")
st.markdown("© 2025 Kantoor Zomerkamp App - Een prettige werkdag gewenst! 📎")
