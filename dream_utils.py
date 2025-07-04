import whisper
import requests
import os
import json
import re
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, List, Any

load_dotenv()

# Configuration des modèles
whisper_model = whisper.load_model("base")

# Fichier de stockage des rêves
DREAMS_FILE = "dreams_history.json"

def transcribe_audio(audio_path: str) -> str:
    """Transcrit un fichier audio en texte"""
    try:
        result = whisper_model.transcribe(audio_path, language="fr")
        return result["text"]
    except Exception as e:
        raise Exception(f"Erreur lors de la transcription : {str(e)}")

def generate_image(prompt: str) -> str:
    """Génère une image à partir d'un prompt"""
    api_key = os.getenv("CLIPDROP_API_KEY")
    if not api_key:
        raise Exception("La clé API Clipdrop n'est pas définie dans .env")
    
    # Amélioration du prompt pour de meilleures images
    enhanced_prompt = f"dream interpretation, surreal, mystical, {prompt}, high quality, detailed, artistic"
    
    url = "https://clipdrop-api.co/text-to-image/v1"
    
    try:
        response = requests.post(
            url,
            headers={"x-api-key": api_key},
            json={
                "prompt": enhanced_prompt,
                
            }
        )
        
        if response.status_code == 200:
            # Nom de fichier unique
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dream_image_{timestamp}.png"
            
            with open(filename, "wb") as f:
                f.write(response.content)
            return filename
        else:
            raise Exception(f"Erreur génération image : {response.status_code}, {response.text}")
    except Exception as e:
        raise Exception(f"Erreur lors de la génération d'image : {str(e)}")

def analyze_dream(dream_text: str) -> Dict[str, Any]:
    """Analyse un rêve et retourne une interprétation complète"""
    
    # Dictionnaire étendu des symboles de rêve
    dream_symbols = {
        "eau": "émotions, inconscient, purification, fluidité",
        "feu": "passion, transformation, énergie, destruction créatrice",
        "voler": "liberté, évasion, aspiration, dépassement de soi",
        "chute": "perte de contrôle, anxiété, peur de l'échec",
        "animal": "instincts, nature primitive, aspects refoulés",
        "maison": "soi, psyché, sécurité, intimité",
        "mort": "transformation, fin d'un cycle, renaissance",
        "enfant": "innocence, nouveau départ, potentiel",
        "serpent": "transformation, sagesse cachée, guérison",
        "chat": "indépendance, mystère, intuition féminine",
        "chien": "loyauté, amitié, protection, fidélité",
        "arbre": "croissance, stabilité, connexion terre-ciel",
        "montagne": "défi, objectif, élévation spirituelle",
        "océan": "inconscient collectif, immensité, émotions profondes",
        "lumière": "connaissance, espoir, révélation, clarté",
        "obscurité": "inconnu, peur, mystère, potentiel caché",
        "pont": "transition, connexion, passage",
        "escalier": "progression, évolution, ascension",
        "miroir": "introspection, vérité, conscience de soi",
        "clé": "solution, accès, révélation, pouvoir",
        "porte": "opportunité, passage, choix, seuil",
        "voiture": "contrôle, direction de vie, autonomie",
        "avion": "ambitions élevées, perspective, voyage spirituel",
        "école": "apprentissage, évaluation, retour au passé",
        "hôpital": "guérison, vulnérabilité, besoin de soins",
        "nourriture": "besoins fondamentaux, nourriture spirituelle",
        "argent": "valeur personnelle, sécurité, pouvoir",
        "bijoux": "valeur cachée, beauté intérieure, préciosité",
        "livre": "connaissance, sagesse, recherche de vérité",
        "téléphone": "communication, besoin de connexion",
        "bébé": "nouveau projet, vulnérabilité, responsabilité"
    }
    
    # Analyse des symboles présents
    symbols_found = []
    dream_lower = dream_text.lower()
    
    for symbol, meaning in dream_symbols.items():
        if symbol in dream_lower:
            symbols_found.append(symbol)
    
    # Analyse des émotions étendues
    emotion_words = {
        "peur": ["peur", "effrayé", "terrifié", "anxieux", "angoissé", "inquiet", "paniqué"],
        "joie": ["heureux", "joyeux", "content", "ravi", "euphorie", "délice", "bonheur"],
        "tristesse": ["triste", "mélancolique", "déprimé", "chagrin", "peine", "mélancolie"],
        "colère": ["colère", "furieux", "irrité", "rage", "énervé", "agacé", "indigné"],
        "surprise": ["surpris", "étonné", "choqué", "stupéfait", "sidéré", "ébahi"],
        "sérénité": ["calme", "paisible", "serein", "tranquille", "apaisé", "zen"],
        "amour": ["amour", "tendresse", "affection", "passion", "attachement"],
        "nostalgie": ["nostalgie", "mélancolie", "regret", "souvenir", "passé"],
        "confusion": ["confus", "perdu", "déboussolé", "désorienté", "trouble"],
        "excitation": ["excité", "stimulé", "enthousiaste", "fébrile", "survolté"]
    }
    
    emotions_detected = []
    for emotion, words in emotion_words.items():
        if any(word in dream_lower for word in words):
            emotions_detected.append(emotion)
    
    # Génération d'une interprétation riche
    interpretation = generate_comprehensive_interpretation(dream_text, symbols_found, emotions_detected)
    
    return {
        "interpretation": interpretation,
        "symbols": symbols_found,
        "emotions": emotions_detected,
        "word_count": len(dream_text.split()),
        "complexity_score": calculate_complexity_score(dream_text),
        "themes": identify_dream_themes(dream_text, symbols_found),
        "psychological_insights": generate_psychological_insights(symbols_found, emotions_detected)
    }

def generate_comprehensive_interpretation(dream_text: str, symbols: List[str], emotions: List[str]) -> str:
    """Génère une interprétation complète et riche du rêve"""
    
    interpretation_parts = []
    
    # Introduction personnalisée
    if emotions:
        dominant_emotion = emotions[0]
        if dominant_emotion == "peur":
            interpretation_parts.append("Votre rêve semble refléter des préoccupations ou anxiétés actuelles.")
        elif dominant_emotion == "joie":
            interpretation_parts.append("Ce rêve révèle un état d'esprit positif et optimiste.")
        elif dominant_emotion == "tristesse":
            interpretation_parts.append("Votre rêve exprime peut-être un besoin de guérison émotionnelle.")
        else:
            interpretation_parts.append("Votre rêve révèle une riche palette d'émotions à explorer.")
    else:
        interpretation_parts.append("Votre rêve offre des insights fascinants sur votre monde intérieur.")
    
    # Analyse approfondie des symboles
    if symbols:
        interpretation_parts.append(f"\n🔮 **Symboles identifiés** : {', '.join(symbols)}")
        
        # Analyse spécifique par symbole
        for symbol in symbols[:3]:  # Limiter aux 3 premiers pour éviter la surcharge
            if symbol == "eau":
                interpretation_parts.append("• L'eau représente vos émotions profondes et votre capacité d'adaptation. Elle peut indiquer un besoin de purification ou de renouveau émotionnel.")
            elif symbol == "voler":
                interpretation_parts.append("• Le vol symbolise votre désir de liberté et d'évasion. Vous aspirez peut-être à dépasser vos limitations actuelles.")
            elif symbol == "maison":
                interpretation_parts.append("• La maison reflète votre état psychologique intime. Elle peut révéler comment vous vous sentez en sécurité ou non dans votre vie.")
            elif symbol == "animal":
                interpretation_parts.append("• Les animaux dans vos rêves représentent vos instincts naturels et vos aspects les plus authentiques.")
            elif symbol == "mort":
                interpretation_parts.append("• La mort symbolise une transformation profonde, la fin d'une période et le début d'une nouvelle phase de vie.")
            elif symbol == "lumière":
                interpretation_parts.append("• La lumière représente la connaissance, l'espoir et la clarté qui émergent dans votre conscience.")
            elif symbol == "obscurité":
                interpretation_parts.append("• L'obscurité peut symboliser l'inconnu qui vous intrigue ou des aspects de vous-même à explorer.")
    
    # Analyse des émotions
    if emotions:
        interpretation_parts.append(f"\n💭 **Climat émotionnel** : {', '.join(emotions)}")
        
        if "peur" in emotions and "joie" in emotions:
            interpretation_parts.append("• Le mélange de peur et de joie suggère une période de transition où excitation et appréhension coexistent.")
        elif "peur" in emotions:
            interpretation_parts.append("• La peur présente peut refléter des anxiétés actuelles ou anticiper des défis à venir.")
        elif "joie" in emotions:
            interpretation_parts.append("• Les sentiments positifs indiquent un alignement avec vos valeurs profondes et vos aspirations.")
        elif "tristesse" in emotions:
            interpretation_parts.append("• La tristesse peut signaler un besoin de guérison ou d'acceptation d'une perte.")
        
        if "sérénité" in emotions:
            interpretation_parts.append("• La sérénité suggère que vous trouvez un équilibre intérieur malgré les défis.")
    
    # Analyse des patterns narratifs
    dream_lower = dream_text.lower()
    
    # Analyse du mouvement dans le rêve
    if any(word in dream_lower for word in ["course", "courir", "fuite", "poursuivre"]):
        interpretation_parts.append("\n🏃 **Dynamique de mouvement** : Le thème de la course ou de la fuite suggère un désir d'échapper à une situation ou au contraire de poursuivre un objectif.")
    
    if any(word in dream_lower for word in ["chute", "tomber", "glisser"]):
        interpretation_parts.append("\n⬇️ **Dynamique de chute** : La chute peut représenter une perte de contrôle ou la peur d'échouer dans un domaine important.")
    
    # Analyse des relations dans le rêve
    if any(word in dream_lower for word in ["famille", "mère", "père", "enfant", "frère", "sœur"]):
        interpretation_parts.append("\n👨‍👩‍👧‍👦 **Dimension familiale** : La présence de la famille suggère des questions liées à vos racines, votre identité ou vos relations proches.")
    
    if any(word in dream_lower for word in ["ami", "amour", "couple", "partenaire"]):
        interpretation_parts.append("\n💕 **Dimension relationnelle** : Les relations dans votre rêve reflètent vos besoins de connexion et d'intimité.")
    
    # Conseils et perspectives
    interpretation_parts.append("\n✨ **Perspectives** :")
    
    if symbols and emotions:
        if "eau" in symbols and "sérénité" in emotions:
            interpretation_parts.append("• Votre rêve suggère une période propice à l'introspection et à la guérison émotionnelle.")
        elif "voler" in symbols and "joie" in emotions:
            interpretation_parts.append("• C'est peut-être le moment d'oser prendre des risques créatifs ou professionnels.")
        elif "maison" in symbols and "peur" in emotions:
            interpretation_parts.append("• Explorez ce qui vous fait vous sentir en sécurité ou vulnérable dans votre environnement actuel.")
        else:
            interpretation_parts.append("• Considérez ce rêve comme une invitation à explorer les aspects de votre vie qu'il met en lumière.")
    
    interpretation_parts.append("• Gardez un journal de vos rêves pour identifier des patterns récurrents.")
    interpretation_parts.append("• Méditez sur les émotions ressenties pour mieux comprendre leurs messages.")
    
    return "\n".join(interpretation_parts)

def identify_dream_themes(dream_text: str, symbols: List[str]) -> List[str]:
    """Identifie les thèmes principaux du rêve"""
    
    themes = []
    dream_lower = dream_text.lower()
    
    # Thèmes basés sur les symboles
    transformation_symbols = ["mort", "serpent", "feu", "eau", "papillon"]
    if any(symbol in symbols for symbol in transformation_symbols):
        themes.append("Transformation")
    
    freedom_symbols = ["voler", "oiseau", "ciel", "montagne"]
    if any(symbol in symbols for symbol in freedom_symbols):
        themes.append("Liberté")
    
    security_symbols = ["maison", "famille", "enfant", "cocon"]
    if any(symbol in symbols for symbol in security_symbols):
        themes.append("Sécurité")
    
    # Thèmes basés sur le contenu textuel
    if any(word in dream_lower for word in ["travail", "bureau", "collègue", "patron"]):
        themes.append("Vie professionnelle")
    
    if any(word in dream_lower for word in ["amour", "couple", "mariage", "baiser"]):
        themes.append("Relations amoureuses")
    
    if any(word in dream_lower for word in ["école", "examen", "étude", "apprendre"]):
        themes.append("Apprentissage")
    
    if any(word in dream_lower for word in ["voyage", "partir", "route", "destination"]):
        themes.append("Voyage/Quête")
    
    if any(word in dream_lower for word in ["passé", "enfance", "souvenir", "nostalgie"]):
        themes.append("Passé/Mémoire")
    
    return themes

def generate_psychological_insights(symbols: List[str], emotions: List[str]) -> List[str]:
    """Génère des insights psychologiques basés sur les symboles et émotions"""
    
    insights = []
    
    # Insights basés sur les combinaisons symboles/émotions
    if "eau" in symbols and "peur" in emotions:
        insights.append("Possible anxiété face à vos émotions profondes")
    
    if "voler" in symbols and "joie" in emotions:
        insights.append("Forte aspiration à la liberté et à l'accomplissement")
    
    if "maison" in symbols and "sérénité" in emotions:
        insights.append("Sentiment de sécurité intérieure bien établi")
    
    if "mort" in symbols and "tristesse" in emotions:
        insights.append("Processus de deuil ou acceptation d'un changement")
    
    # Insights basés sur les émotions multiples
    if len(emotions) > 2:
        insights.append("Richesse émotionnelle complexe nécessitant de l'attention")
    
    if "peur" in emotions and "joie" in emotions:
        insights.append("Ambivalence face à une situation de changement")
    
    # Insights basés sur les symboles
    if len(symbols) > 3:
        insights.append("Rêve riche en symboles indiquant une période de transformation")
    
    if "lumière" in symbols and "obscurité" in symbols:
        insights.append("Processus d'intégration entre conscient et inconscient")
    
    return insights

def calculate_complexity_score(dream_text: str) -> float:
    """Calcule un score de complexité du rêve"""
    
    # Facteurs de complexité
    word_count = len(dream_text.split())
    sentence_count = len(re.split(r'[.!?]+', dream_text))
    
    # Présence de mots complexes
    complex_words = ["transformation", "métamorphose", "symbolique", "mystérieux", "surréaliste"]
    complex_word_count = sum(1 for word in complex_words if word in dream_text.lower())
    
    # Score basé sur différents critères
    length_score = min(word_count / 100, 1.0)  # Normalisé sur 100 mots
    structure_score = min(sentence_count / 10, 1.0)  # Normalisé sur 10 phrases
    complexity_word_score = min(complex_word_count / 5, 1.0)  # Normalisé sur 5 mots complexes
    
    final_score = (length_score + structure_score + complexity_word_score) / 3
    return round(final_score * 10, 1)  # Score sur 10

def save_dream_entry(dream_entry: Dict[str, Any]):
    """Sauvegarde une entrée de rêve dans le fichier JSON"""
    
    # Charger l'historique existant
    history = load_dream_history()
    
    # Ajouter la nouvelle entrée
    history.append(dream_entry)
    
    # Sauvegarder
    try:
        with open(DREAMS_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        raise Exception(f"Erreur lors de la sauvegarde : {str(e)}")

def load_dream_history() -> List[Dict[str, Any]]:
    """Charge l'historique des rêves depuis le fichier JSON"""
    
    if not os.path.exists(DREAMS_FILE):
        return []
    
    try:
        with open(DREAMS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement de l'historique : {str(e)}")
        return []

def get_dream_statistics() -> Dict[str, Any]:
    """Calcule des statistiques sur les rêves enregistrés"""
    
    history = load_dream_history()
    
    if not history:
        return {}
    
    # Statistiques de base
    total_dreams = len(history)
    
    # Qualité moyenne du sommeil
    sleep_qualities = [d["metadata"].get("sleep_quality", 0) for d in history if d["metadata"].get("sleep_quality")]
    avg_sleep_quality = sum(sleep_qualities) / len(sleep_qualities) if sleep_qualities else 0
    
    # Clarté moyenne des rêves
    dream_clarities = [d["metadata"].get("dream_clarity", 0) for d in history if d["metadata"].get("dream_clarity")]
    avg_dream_clarity = sum(dream_clarities) / len(dream_clarities) if dream_clarities else 0
    
    # Types de rêves les plus fréquents
    dream_types = [d["metadata"].get("dream_type", "Non spécifié") for d in history]
    type_counts = {}
    for dream_type in dream_types:
        type_counts[dream_type] = type_counts.get(dream_type, 0) + 1
    
    # Émotions les plus fréquentes
    all_emotions = []
    for d in history:
        all_emotions.extend(d["metadata"].get("emotions", []))
    
    emotion_counts = {}
    for emotion in all_emotions:
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    
    # Symboles les plus fréquents
    all_symbols = []
    for d in history:
        all_symbols.extend(d["analysis"].get("symbols", []))
    
    symbol_counts = {}
    for symbol in all_symbols:
        symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1
    
    # Évolution dans le temps
    dates = [datetime.fromisoformat(d["date"]) for d in history]
    first_dream = min(dates) if dates else None
    last_dream = max(dates) if dates else None
    
    # Score de complexité moyen
    complexity_scores = [d["analysis"].get("complexity_score", 0) for d in history]
    avg_complexity = sum(complexity_scores) / len(complexity_scores) if complexity_scores else 0
    
    return {
        "total_dreams": total_dreams,
        "avg_sleep_quality": round(avg_sleep_quality, 1),
        "avg_dream_clarity": round(avg_dream_clarity, 1),
        "avg_complexity": round(avg_complexity, 1),
        "dream_type_distribution": type_counts,
        "emotion_distribution": emotion_counts,
        "symbol_distribution": symbol_counts,
        "first_dream_date": first_dream.isoformat() if first_dream else None,
        "last_dream_date": last_dream.isoformat() if last_dream else None,
        "dream_frequency": calculate_dream_frequency(dates) if dates else 0
    }

def calculate_dream_frequency(dates: List[datetime]) -> float:
    """Calcule la fréquence des rêves (rêves par semaine)"""
    if len(dates) < 2:
        return 0
    
    # Calculer la période entre le premier et le dernier rêve
    period_days = (max(dates) - min(dates)).days
    
    if period_days == 0:
        return len(dates)  # Tous les rêves le même jour
    
    # Convertir en semaines et calculer la fréquence
    period_weeks = period_days / 7
    return round(len(dates) / period_weeks, 1)

def search_dreams(query: str, dream_history: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Recherche dans l'historique des rêves"""
    
    if dream_history is None:
        dream_history = load_dream_history()
    
    if not query.strip():
        return dream_history
    
    query_lower = query.lower()
    results = []
    
    for dream in dream_history:
        # Recherche dans le titre
        if query_lower in dream.get("title", "").lower():
            results.append(dream)
            continue
        
        # Recherche dans le texte du rêve
        if query_lower in dream.get("text", "").lower():
            results.append(dream)
            continue
        
        # Recherche dans les symboles
        symbols = dream.get("analysis", {}).get("symbols", [])
        if any(query_lower in symbol.lower() for symbol in symbols):
            results.append(dream)
            continue
        
        # Recherche dans les émotions
        emotions = dream.get("metadata", {}).get("emotions", [])
        if any(query_lower in emotion.lower() for emotion in emotions):
            results.append(dream)
            continue
    
    return results

def export_dreams_to_json(filename: str = None) -> str:
    """Exporte tous les rêves vers un fichier JSON"""
    
    if filename is None:
        filename = f"dreams_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    history = load_dream_history()
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        return filename
    except Exception as e:
        raise Exception(f"Erreur lors de l'export : {str(e)}")

def import_dreams_from_json(filename: str) -> int:
    """Importe des rêves depuis un fichier JSON"""
    
    if not os.path.exists(filename):
        raise Exception(f"Le fichier {filename} n'existe pas")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            imported_dreams = json.load(f)
        
        # Valider la structure des données
        if not isinstance(imported_dreams, list):
            raise Exception("Le fichier doit contenir une liste de rêves")
        
        # Charger l'historique existant
        existing_history = load_dream_history()
        
        # Éviter les doublons basés sur la date et le texte
        existing_keys = set()
        for dream in existing_history:
            key = (dream.get("date", ""), dream.get("text", "")[:50])
            existing_keys.add(key)
        
        # Ajouter les nouveaux rêves
        new_dreams = []
        for dream in imported_dreams:
            key = (dream.get("date", ""), dream.get("text", "")[:50])
            if key not in existing_keys:
                new_dreams.append(dream)
                existing_keys.add(key)
        
        # Sauvegarder l'historique mis à jour
        updated_history = existing_history + new_dreams
        
        with open(DREAMS_FILE, 'w', encoding='utf-8') as f:
            json.dump(updated_history, f, ensure_ascii=False, indent=2)
        
        return len(new_dreams)
        
    except Exception as e:
        raise Exception(f"Erreur lors de l'import : {str(e)}")

def delete_dream(dream_index: int) -> bool:
    """Supprime un rêve de l'historique"""
    
    history = load_dream_history()
    
    if 0 <= dream_index < len(history):
        # Supprimer le fichier image associé si il existe
        dream = history[dream_index]
        image_path = dream.get("image_path", "")
        if image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
            except:
                pass  # Ignorer les erreurs de suppression d'image
        
        # Supprimer l'entrée
        history.pop(dream_index)
        
        # Sauvegarder
        try:
            with open(DREAMS_FILE, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            raise Exception(f"Erreur lors de la suppression : {str(e)}")
    
    return False

def cleanup_old_images(days_old: int = 30):
    """Nettoie les images anciennes pour libérer de l'espace"""
    
    cutoff_date = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
    
    # Lister tous les fichiers d'images de rêves
    image_files = []
    for filename in os.listdir('.'):
        if filename.startswith('dream_image_') and filename.endswith('.png'):
            image_files.append(filename)
    
    deleted_count = 0
    
    for image_file in image_files:
        try:
            # Vérifier la date de création
            file_time = os.path.getctime(image_file)
            if file_time < cutoff_date:
                os.remove(image_file)
                deleted_count += 1
        except:
            continue  # Ignorer les erreurs
    
    return deleted_count

def get_dream_insights(dream_history: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Génère des insights avancés sur les rêves"""
    
    if dream_history is None:
        dream_history = load_dream_history()
    
    if not dream_history:
        return {}
    
    insights = {}
    
    # Analyse des patterns temporels
    dates = [datetime.fromisoformat(d["date"]) for d in dream_history]
    
    # Jour de la semaine le plus fréquent
    weekdays = [d.weekday() for d in dates]
    weekday_names = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    weekday_counts = {}
    for weekday in weekdays:
        weekday_counts[weekday_names[weekday]] = weekday_counts.get(weekday_names[weekday], 0) + 1
    
    most_common_weekday = max(weekday_counts, key=weekday_counts.get) if weekday_counts else None
    
    # Heure la plus fréquente (si disponible)
    hours = [d.hour for d in dates]
    hour_counts = {}
    for hour in hours:
        hour_counts[hour] = hour_counts.get(hour, 0) + 1
    
    most_common_hour = max(hour_counts, key=hour_counts.get) if hour_counts else None
    
    # Corrélation entre qualité du sommeil et clarté des rêves
    sleep_clarity_pairs = []
    for d in dream_history:
        sleep_q = d["metadata"].get("sleep_quality")
        dream_c = d["metadata"].get("dream_clarity")
        if sleep_q and dream_c:
            sleep_clarity_pairs.append((sleep_q, dream_c))
    
    correlation = 0
    if len(sleep_clarity_pairs) > 1:
        # Calcul simple de corrélation
        n = len(sleep_clarity_pairs)
        sum_x = sum(pair[0] for pair in sleep_clarity_pairs)
        sum_y = sum(pair[1] for pair in sleep_clarity_pairs)
        sum_xy = sum(pair[0] * pair[1] for pair in sleep_clarity_pairs)
        sum_x2 = sum(pair[0] ** 2 for pair in sleep_clarity_pairs)
        sum_y2 = sum(pair[1] ** 2 for pair in sleep_clarity_pairs)
        
        numerator = n * sum_xy - sum_x * sum_y
        denominator = ((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2)) ** 0.5
        
        if denominator != 0:
            correlation = numerator / denominator
    
    # Évolution des émotions dans le temps
    emotion_evolution = {}
    for d in dream_history:
        date_str = d["date"][:10]  # YYYY-MM-DD
        emotions = d["metadata"].get("emotions", [])
        
        if date_str not in emotion_evolution:
            emotion_evolution[date_str] = {}
        
        for emotion in emotions:
            emotion_evolution[date_str][emotion] = emotion_evolution[date_str].get(emotion, 0) + 1
    
    insights = {
        "most_common_weekday": most_common_weekday,
        "most_common_hour": most_common_hour,
        "sleep_clarity_correlation": round(correlation, 3),
        "emotion_evolution": emotion_evolution,
        "total_analysis_period_days": (max(dates) - min(dates)).days if len(dates) > 1 else 0,
        "average_dreams_per_week": calculate_dream_frequency(dates)
    }
    
    return insights

# Fonction utilitaire pour nettoyer les fichiers temporaires
def cleanup_temp_files():
    """Nettoie les fichiers temporaires"""
    temp_files = ["temp_audio.wav"]
    
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass