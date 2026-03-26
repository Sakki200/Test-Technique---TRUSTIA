MAX_WIDTH = 100

sentences = {
    "s1": "Le code propre facilite la maintenance",
    "s2": "Tester souvent évite beaucoup d erreurs",
    "s3": "Cette phrase ne doit pas s afficher",
    "s4": "Cette phrase ne doit pas s afficher",
    "s5": "Un bon code doit rester simple et clair",
    "s6": "La simplicité améliore la qualité du code",
    "s7": "Refactoriser améliore la compréhension",
}

blocs = [["s1"], ["s2", "s3"], ["s4", "s5", "s6", "s7"]]

excluded_sentences = {"s3", "s5"}


for bloc in blocs:
    lines = [sentences[s].lower() for s in bloc if s not in excluded_sentences]
    if not lines:
        continue

    width = min(max(len(line) for line in lines) + 4, MAX_WIDTH)
    edge = "-" * width

    print(edge)
    print("\n".join(f"| {line.ljust(width - 4)} |" for line in lines))
    print(edge, "\n") 