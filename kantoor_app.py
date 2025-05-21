import streamlit as st
import random
import datetime

# App titel en configuratie
st.set_page_config(page_title="Pion & Partners App", layout="wide")

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

# Initialiseer session state voor eerst gebruik
if 'history' not in st.session_state:
    st.session_state.history = []
    
# Initialiseer session state voor de klachten functionaliteit
if 'klacht_stage' not in st.session_state:
    st.session_state.klacht_stage = 0

# Functie om de slide waarden te resetten voor de CAPTCHA
def reset_other_slider(changed_slider):
    if changed_slider == 1 and st.session_state.slider1 == 100:
        # Als slider 1 op 100 wordt gezet
        if st.session_state.slider2 == 100:
            st.session_state.slider2 = 0
        if st.session_state.slider3 == 100:
            st.session_state.slider3 = 0
    elif changed_slider == 2 and st.session_state.slider2 == 100:
        # Als slider 2 op 100 wordt gezet
        if st.session_state.slider1 == 100:
            st.session_state.slider1 = 0
        if st.session_state.slider3 == 100:
            st.session_state.slider3 = 0
    elif changed_slider == 3 and st.session_state.slider3 == 100:
        # Als slider 3 op 100 wordt gezet
        if st.session_state.slider1 == 100:
            st.session_state.slider1 = 0
        if st.session_state.slider2 == 100:
            st.session_state.slider2 = 0

# Standaard antwoorden (kan later aangepast worden)
vrij_antwoorden = ["A", "B", "C", "D", "E", "F", "G", "H"]
opslag_antwoorden = ["A", "B", "C", "D", "E", "F", "G", "H"]
feedback_antwoorden = ["A", "B", "C", "D", "E", "F", "G", "H"]

# Header
st.title("📝 Pion & Partners")
st.subheader("Welkom bij het digitale kantoor")

# Tabbladen voor verschillende functies
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Vrij aanvragen", "Opslag aanvragen", "Klacht indienen", "Feedback geven", "Geschiedenis"])

# Tab 1: Vrij aanvragen
with tab1:
    st.header("Verlof aanvragen")
    st.write("Vul hier je verzoek in om vrij te krijgen (minimaal 15 woorden)")
    
    vrij_verzoek = st.text_area("Waarom wilt u vrij?", height=150, key="vrij_text")
    submit_vrij = st.button("Indienen", key="submit_vrij")
    
    if submit_vrij:
        # Controleer of het verzoek minimaal 15 woorden bevat
        if len(vrij_verzoek.split()) < 15:
            st.error("Je verzoek is te kort. Gebruik minimaal 15 woorden om je verzoek in te dienen.")
        else:
            # Kies willekeurig antwoord
            antwoord = random.choice(vrij_antwoorden)
            
            # Toon het antwoord
            st.success(f"Je verzoek is ingediend! Reactie van je manager: {antwoord}")
            
            # Toevoegen aan geschiedenis
            st.session_state.history.append({
                "type": "Verlof aanvraag",
                "verzoek": vrij_verzoek,
                "antwoord": antwoord,
            })

# Tab 2: Opslag aanvragen
with tab2:
    st.header("Opslag aanvragen")
    st.write("Vul hier je verzoek voor een opslag in (minimaal 15 woorden)")
    
    opslag_verzoek = st.text_area("Waarom verdien je een opslag?", height=150, key="opslag_text")
    submit_opslag = st.button("Indienen", key="submit_opslag")
    
    if submit_opslag:
        # Controleer of het verzoek minimaal 15 woorden bevat
        if len(opslag_verzoek.split()) < 15:
            st.error("Je verzoek is te kort. Gebruik minimaal 15 woorden om je verzoek in te dienen.")
        else:
            # Kies willekeurig antwoord
            antwoord = random.choice(opslag_antwoorden)
            
            # Toon het antwoord
            st.success(f"Je opslag verzoek is ingediend! Reactie van je manager: {antwoord}")
            
            # Toevoegen aan geschiedenis
            st.session_state.history.append({
                "type": "Opslag aanvraag",
                "verzoek": opslag_verzoek,
                "antwoord": antwoord,
            })

# Tab 3: Klacht indienen
with tab3:
    st.header("Klacht indienen")
    
    if st.session_state.klacht_stage == 0:
        st.write("Vul het formulier in om een klacht in te dienen")
        
        # Klachten formulier
        with st.form("klacht_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                naam = st.text_input("Naam", key="naam_klacht")
                achternaam = st.text_input("Achternaam", key="achternaam_klacht")
                functie = st.text_input("Functie", key="functie_klacht")
                salaris = st.number_input("Salaris (€)", min_value=0, key="salaris_klacht")
            
            with col2:
                fav_kampleiding = st.text_input("Favoriete kampleiding", key="fav_kampleiding_klacht")
                # Gewijzigd: geboortedatum verder terug in de tijd kunnen selecteren
                geboortedatum = st.date_input("Geboortedatum", min_value=datetime.date(1900, 1, 1), key="geboortedatum_klacht")
                fav_spel = st.text_input("Je favoriete spel", key="fav_spel_klacht")
                som = st.number_input("9 + 10 =", key="som_klacht")
                thema = st.text_input("Wat denk je dat het thema wordt dit jaar?", key="thema_klacht")
            
            submit_klacht = st.form_submit_button("Verzenden")
            
            if submit_klacht:
                # Valideer alle velden
                all_filled = all([naam, achternaam, functie, salaris > 0, fav_kampleiding,
                                fav_spel, som, thema])
                
                if not all_filled:
                    st.error("Alle velden zijn verplicht!")
                elif fav_kampleiding.lower() != "hajo":
                    st.error("Je hebt je vergist bij je favoriete kampleiding. Het moet 'Hajo' zijn.")
                # Gewijzigd: 9 + 10 = 21 in plaats van 19
                elif som != 21:
                    st.error("9 + 10 = 21. Probeer het opnieuw.")
                else:
                    # Ga naar de volgende stap
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
                    st.rerun()
    
    elif st.session_state.klacht_stage == 1:
        st.write("Bevestig je identiteit")
        
        # Bevestiging formulier
        with st.form("confirm_form_klacht"):
            bevestig_naam = st.text_input("Volledige naam", key="bevestig_naam_klacht")
            vandaag = st.date_input("Datum van vandaag", datetime.date.today(), key="vandaag_klacht")
            
            confirm_button = st.form_submit_button("Bevestigen")
            
            if confirm_button:
                if not bevestig_naam or vandaag != datetime.date.today():
                    st.error("Vul je naam in en selecteer de huidige datum")
                else:
                    # Ga naar CAPTCHA
                    st.session_state.klacht_stage = 2
                    st.session_state.bevestiging = {
                        "naam": bevestig_naam,
                        "datum": vandaag
                    }
                    st.rerun()
    
    elif st.session_state.klacht_stage == 2:
        st.write("CAPTCHA Verificatie")
        st.warning("Sleep één van de drie sliders helemaal naar rechts om je klacht te verzenden")
        
        # Initialiseer slider waarden als ze nog niet bestaan
        if 'slider1' not in st.session_state:
            st.session_state.slider1 = 0
        if 'slider2' not in st.session_state:
            st.session_state.slider2 = 0
        if 'slider3' not in st.session_state:
            st.session_state.slider3 = 0
        
        # Eerste slider
        slider1 = st.slider("Beweeg naar rechts (1)", 
                           min_value=0, 
                           max_value=100, 
                           value=st.session_state.slider1,
                           key="slider1",
                           on_change=reset_other_slider,
                           args=(1,))
        
        # Tweede slider
        slider2 = st.slider("Beweeg naar rechts (2)", 
                           min_value=0, 
                           max_value=100, 
                           value=st.session_state.slider2,
                           key="slider2",
                           on_change=reset_other_slider,
                           args=(2,))
        
        # Derde slider
        slider3 = st.slider("Beweeg naar rechts (3)", 
                           min_value=0, 
                           max_value=100, 
                           value=st.session_state.slider3,
                           key="slider3",
                           on_change=reset_other_slider,
                           args=(3,))

# Tab 4: Feedback geven
with tab4:
    st.header("Feedback geven aan het kantoor")
    st.write("Vul hier je feedback in (minimaal 15 woorden)")
    
    feedback_verzoek = st.text_area("Wat is je feedback?", height=150, key="feedback_text")
    submit_feedback = st.button("Indienen", key="submit_feedback")
    
    if submit_feedback:
        # Controleer of het verzoek minimaal 15 woorden bevat
        if len(feedback_verzoek.split()) < 15:
            st.error("Je feedback is te kort. Gebruik minimaal 15 woorden om je feedback in te dienen.")
        else:
            # Kies willekeurig antwoord
            antwoord = random.choice(feedback_antwoorden)
            
            # Toon het antwoord
            st.success(f"Je feedback is ingediend! Reactie van het kantoor: {antwoord}")
            
            # Toevoegen aan geschiedenis
            st.session_state.history.append({
                "type": "Feedback",
                "verzoek": feedback_verzoek,
                "antwoord": antwoord,
            })

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
st.markdown("© 2025 Pion & Partners app - een prettige werkdag gewenst!📎")
