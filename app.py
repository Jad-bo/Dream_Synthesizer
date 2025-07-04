import streamlit as st
from dream_utils import transcribe_audio, generate_image, analyze_dream, save_dream_entry, load_dream_history
import os
from datetime import datetime
import json

# Configuration de la page
st.set_page_config(
    page_title="Synthétiseur de Rêves", 
    page_icon="🌙",
    layout="wide"
)

# CSS personnalisé pour l'interface
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        margin-bottom: 2rem;
    }
    .dream-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .emotion-tag {
        display: inline-block;
        background: #ff6b6b;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 2px;
    }
    .symbol-tag {
        display: inline-block;
        background: #4ecdc4;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 2px;
    }
</style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown('<h1 class="main-header">🌙 Synthétiseur de Rêves</h1>', unsafe_allow_html=True)

# Sidebar pour navigation
with st.sidebar:
    st.header("🎯 Navigation")
    mode = st.radio(
        "Choisissez votre mode :",
        ["📝 Nouveau rêve", "🎙️ Rêve vocal", "📚 Historique", "📊 Analyses", "🎨 Galerie"]
    )
    
    st.markdown("---")
    st.header("⚙️ Paramètres")
    dream_style = st.selectbox(
        "Style d'image :",
        ["réaliste", "artistique", "surréaliste", "minimaliste", "fantasy"]
    )
    
    image_mood = st.selectbox(
        "Ambiance :",
        ["mystérieuse", "colorée", "sombre", "lumineuse", "onirique"]
    )

# Mode principal : Nouveau rêve (texte)
if mode == "📝 Nouveau rêve":
    st.header("✍️ Racontez votre rêve")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        dream_text = st.text_area(
            "Décrivez votre rêve en détail :",
            height=200,
            placeholder="Cette nuit, j'ai rêvé que..."
        )
        
        dream_title = st.text_input("Titre du rêve (optionnel):")
        
        # Métadonnées
        st.subheader("📋 Informations supplémentaires")
        col_meta1, col_meta2 = st.columns(2)
        
        with col_meta1:
            sleep_quality = st.slider("Qualité du sommeil (1-10):", 1, 10, 7)
            dream_clarity = st.slider("Clarté du rêve (1-10):", 1, 10, 5)
            
        with col_meta2:
            dream_emotions = st.multiselect(
                "Émotions ressenties :",
                ["Joie", "Peur", "Tristesse", "Colère", "Surprise", "Anxiété", "Sérénité", "Confusion"]
            )
            
            dream_type = st.selectbox(
                "Type de rêve :",
                ["Rêve normal", "Cauchemar", "Rêve lucide", "Rêve récurrent", "Rêve prémonitoire"]
            )
    
    with col2:
        st.subheader("🎨 Aperçu")
        if dream_text:
            st.info(f"Mots : {len(dream_text.split())}")
            st.info(f"Style : {dream_style}")
            st.info(f"Ambiance : {image_mood}")
    
    if st.button("🚀 Analyser et générer", type="primary"):
        if dream_text:
            with st.spinner("Analyse du rêve en cours..."):
                # Analyse du rêve
                analysis = analyze_dream(dream_text)
                
                # Génération de l'image avec style
                enhanced_prompt = f"{dream_text}, style {dream_style}, ambiance {image_mood}"
                image_path = generate_image(enhanced_prompt)
                
                # Sauvegarde
                dream_entry = {
                    "title": dream_title or f"Rêve du {datetime.now().strftime('%d/%m/%Y')}",
                    "text": dream_text,
                    "analysis": analysis,
                    "image_path": image_path,
                    "metadata": {
                        "sleep_quality": sleep_quality,
                        "dream_clarity": dream_clarity,
                        "emotions": dream_emotions,
                        "dream_type": dream_type,
                        "style": dream_style,
                        "mood": image_mood
                    },
                    "date": datetime.now().isoformat()
                }
                
                save_dream_entry(dream_entry)
            
            # Affichage des résultats
            st.success("Rêve analysé avec succès !")
            
            col_result1, col_result2 = st.columns(2)
            
            with col_result1:
                st.subheader("📝 Votre rêve")
                st.write(dream_text)
                
                st.subheader("🔍 Analyse psychologique")
                st.write(analysis.get("interpretation", "Analyse non disponible"))
                
                if analysis.get("symbols"):
                    st.subheader("🔮 Symboles identifiés")
                    for symbol in analysis["symbols"]:
                        st.markdown(f'<span class="symbol-tag">{symbol}</span>', unsafe_allow_html=True)
                
                if dream_emotions:
                    st.subheader("💭 Émotions")
                    for emotion in dream_emotions:
                        st.markdown(f'<span class="emotion-tag">{emotion}</span>', unsafe_allow_html=True)
            
            with col_result2:
                st.subheader("🎨 Visualisation")
                st.image(image_path, caption="Interprétation visuelle de votre rêve", use_column_width=True)
        else:
            st.warning("Veuillez saisir votre rêve avant de continuer.")

# Mode vocal
elif mode == "🎙️ Rêve vocal":
    st.header("🎙️ Racontez votre rêve à voix haute")
    
    audio_file = st.file_uploader("Uploadez votre rêve (WAV/MP3)", type=["wav", "mp3"])
    
    if audio_file:
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_file.read())
        
        st.audio("temp_audio.wav")
        
        if st.button("🔄 Transcrire et analyser"):
            with st.spinner("Transcription en cours..."):
                texte_reve = transcribe_audio("temp_audio.wav")
            
            st.subheader("📝 Transcription")
            st.write(texte_reve)
            
            with st.spinner("Analyse et génération..."):
                analysis = analyze_dream(texte_reve)
                enhanced_prompt = f"{texte_reve}, style {dream_style}, ambiance {image_mood}"
                image_path = generate_image(enhanced_prompt)
                
                # Sauvegarde
                dream_entry = {
                    "title": f"Rêve vocal du {datetime.now().strftime('%d/%m/%Y')}",
                    "text": texte_reve,
                    "analysis": analysis,
                    "image_path": image_path,
                    "metadata": {
                        "input_type": "audio",
                        "style": dream_style,
                        "mood": image_mood
                    },
                    "date": datetime.now().isoformat()
                }
                
                save_dream_entry(dream_entry)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🔍 Analyse")
                st.write(analysis.get("interpretation", "Analyse non disponible"))
                
                if analysis.get("symbols"):
                    st.subheader("🔮 Symboles")
                    for symbol in analysis["symbols"]:
                        st.markdown(f'<span class="symbol-tag">{symbol}</span>', unsafe_allow_html=True)
            
            with col2:
                st.subheader("🎨 Visualisation")
                st.image(image_path, caption="Votre rêve visualisé", use_column_width=True)
        
        # Nettoyage du fichier temporaire
        if os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav")

# Historique des rêves
elif mode == "📚 Historique":
    st.header("📚 Historique de vos rêves")
    
    history = load_dream_history()
    
    if history:
        # Filtres
        col_filter1, col_filter2, col_filter3 = st.columns(3)
        
        with col_filter1:
            filter_type = st.selectbox("Type de rêve :", ["Tous"] + list(set([d["metadata"].get("dream_type", "Non spécifié") for d in history])))
        
        with col_filter2:
            filter_emotion = st.selectbox("Émotion :", ["Toutes"] + list(set([e for d in history for e in d["metadata"].get("emotions", [])])))
        
        with col_filter3:
            sort_by = st.selectbox("Trier par :", ["Date (récent)", "Date (ancien)", "Titre"])
        
        # Filtrage
        filtered_history = history
        if filter_type != "Tous":
            filtered_history = [d for d in filtered_history if d["metadata"].get("dream_type") == filter_type]
        if filter_emotion != "Toutes":
            filtered_history = [d for d in filtered_history if filter_emotion in d["metadata"].get("emotions", [])]
        
        # Tri
        if sort_by == "Date (récent)":
            filtered_history.sort(key=lambda x: x["date"], reverse=True)
        elif sort_by == "Date (ancien)":
            filtered_history.sort(key=lambda x: x["date"])
        else:
            filtered_history.sort(key=lambda x: x["title"])
        
        # Affichage
        for i, dream in enumerate(filtered_history):
            with st.expander(f"🌙 {dream['title']} - {datetime.fromisoformat(dream['date']).strftime('%d/%m/%Y %H:%M')}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write("**Rêve :**")
                    st.write(dream["text"])
                    
                    st.write("**Analyse :**")
                    st.write(dream["analysis"].get("interpretation", "Pas d'analyse"))
                    
                    if dream["analysis"].get("symbols"):
                        st.write("**Symboles :**")
                        for symbol in dream["analysis"]["symbols"]:
                            st.markdown(f'<span class="symbol-tag">{symbol}</span>', unsafe_allow_html=True)
                
                with col2:
                    if os.path.exists(dream["image_path"]):
                        st.image(dream["image_path"], caption="Visualisation", use_column_width=True)
                    
                    # Métadonnées
                    metadata = dream["metadata"]
                    if metadata.get("sleep_quality"):
                        st.metric("Qualité sommeil", f"{metadata['sleep_quality']}/10")
                    if metadata.get("dream_clarity"):
                        st.metric("Clarté", f"{metadata['dream_clarity']}/10")
                    if metadata.get("emotions"):
                        st.write("**Émotions :**")
                        for emotion in metadata["emotions"]:
                            st.markdown(f'<span class="emotion-tag">{emotion}</span>', unsafe_allow_html=True)
    else:
        st.info("Aucun rêve enregistré pour le moment. Commencez par raconter votre premier rêve !")

# Analyses et statistiques
elif mode == "📊 Analyses":
    st.header("📊 Analyses de vos rêves")
    
    history = load_dream_history()
    
    if history:
        # Statistiques générales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total des rêves", len(history))
        
        with col2:
            avg_quality = sum([d["metadata"].get("sleep_quality", 0) for d in history]) / len(history)
            st.metric("Qualité moyenne", f"{avg_quality:.1f}/10")
        
        with col3:
            avg_clarity = sum([d["metadata"].get("dream_clarity", 0) for d in history]) / len(history)
            st.metric("Clarté moyenne", f"{avg_clarity:.1f}/10")
        
        with col4:
            dream_types = [d["metadata"].get("dream_type", "Normal") for d in history]
            most_common = max(set(dream_types), key=dream_types.count) if dream_types else "Aucun"
            st.metric("Type le plus fréquent", most_common)
        
        # Graphiques
        st.subheader("📈 Tendances")
        
        # Émotions les plus fréquentes
        all_emotions = [e for d in history for e in d["metadata"].get("emotions", [])]
        if all_emotions:
            emotion_counts = {}
            for emotion in all_emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            st.bar_chart(emotion_counts)
        
        # Mots-clés les plus fréquents
        st.subheader("🔤 Mots-clés récurrents")
        all_text = " ".join([d["text"] for d in history])
        words = all_text.lower().split()
        # Filtrer les mots courants
        common_words = {"le", "la", "les", "de", "des", "du", "un", "une", "et", "ou", "mais", "donc", "car", "ni", "je", "tu", "il", "elle", "nous", "vous", "ils", "elles", "que", "qui", "dont", "où", "dans", "sur", "avec", "sans", "pour", "par", "à", "au", "aux", "ce", "cette", "ces", "mon", "ma", "mes", "ton", "ta", "tes", "son", "sa", "ses", "notre", "votre", "leur", "leurs"}
        filtered_words = [w for w in words if len(w) > 3 and w not in common_words]
        
        if filtered_words:
            word_counts = {}
            for word in filtered_words:
                word_counts[word] = word_counts.get(word, 0) + 1
            
            # Top 10 des mots
            sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            word_dict = dict(sorted_words)
            
            st.bar_chart(word_dict)
    else:
        st.info("Pas assez de données pour générer des analyses.")

# Galerie d'images
elif mode == "🎨 Galerie":
    st.header("🎨 Galerie de vos rêves")
    
    history = load_dream_history()
    
    if history:
        # Grille d'images
        cols = st.columns(3)
        
        for i, dream in enumerate(history):
            with cols[i % 3]:
                if os.path.exists(dream["image_path"]):
                    st.image(dream["image_path"], caption=dream["title"], use_column_width=True)
                    
                    if st.button(f"Voir détails", key=f"detail_{i}"):
                        st.session_state[f"show_detail_{i}"] = not st.session_state.get(f"show_detail_{i}", False)
                    
                    if st.session_state.get(f"show_detail_{i}", False):
                        st.write(f"**Date :** {datetime.fromisoformat(dream['date']).strftime('%d/%m/%Y')}")
                        st.write(f"**Résumé :** {dream['text'][:100]}...")
                        if dream["analysis"].get("symbols"):
                            st.write("**Symboles :**")
                            for symbol in dream["analysis"]["symbols"][:3]:
                                st.markdown(f'<span class="symbol-tag">{symbol}</span>', unsafe_allow_html=True)
    else:
        st.info("Aucune image générée pour le moment.")

# Footer
st.markdown("---")
st.markdown("🌙 **Synthétiseur de Rêves** - Explorez votre inconscient à travers l'IA")