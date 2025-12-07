import os
import re
from collections import Counter, defaultdict

OK_DIR = "./tab_processor/files/validations/ok"
INSIGHTS_DIR = "./tab_processor/files/insights"

STOPWORDS = {
    "el","la","los","las","de","del","y","que","a","en","un","una","con","por",
    "se","no","me","te","lo","le","mi","tu","su","al","es","ya","si","para",
    "como","pero","mas","muy","cuando","donde","sin","sobre","esto","esa","ese",
    "porque","qué","qué","solo","yo","tu","él","ella","ellos","ellas"
}


def clean_text(text):
    """Remove punctuation, lowercase, and split into words."""
    text = text.lower()
    text = re.sub(r"[^a-záéíóúñü\s]", " ", text)
    words = text.split()
    words = [w for w in words if len(w) >= 3 and w not in STOPWORDS]
    return words


def main():

    if not os.path.exists(OK_DIR):
        print("No OK directory found.")
        return

    if not os.path.exists(INSIGHTS_DIR):
        os.makedirs(INSIGHTS_DIR)

    artist_texts = defaultdict(list)

    # --- Read all lyrics OK ---
    for filename in os.listdir(OK_DIR):
        if not filename.endswith("_lyrics.txt"):
            continue
        
        path = os.path.join(OK_DIR, filename)

        # Extract artist
        artist = filename.split("_")[0]

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
            artist_texts[artist].append(text)

    # Global counter
    global_counter = Counter()

    # --- Process each artist ---
    with open(os.path.join(INSIGHTS_DIR, "artist_stats.txt"), "w", encoding="utf-8") as stats_file:

        for artist, texts in artist_texts.items():

            # Merge lyrics
            merged = "\n".join(texts)

            # Save merged file
            merged_path = os.path.join(INSIGHTS_DIR, f"{artist}_merged.txt")
            with open(merged_path, "w", encoding="utf-8") as f:
                f.write(merged)

            # Count words
            words = clean_text(merged)
            counter = Counter(words)

            # Update global stats
            global_counter.update(counter)

            top10 = counter.most_common(10)

            stats_file.write(f"\n=== {artist.upper()} ===\n")
            for word, count in top10:
                stats_file.write(f"{word}: {count}\n")

    # --- Global stats ---
    top20 = global_counter.most_common(20)

    with open(os.path.join(INSIGHTS_DIR, "global_stats.txt"), "w", encoding="utf-8") as f:
        f.write("=== GLOBAL TOP 20 WORDS ===\n")
        for word, count in top20:
            f.write(f"{word}: {count}\n")

    print("Insights completed.")
    

if __name__ == "__main__":
    main()
