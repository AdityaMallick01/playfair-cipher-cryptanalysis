from playfair import decrypt


COMMON_WORDS = [
    "THE",
    "HELLO",
    "WORLD",
    "SECRET",
    "MESSAGE",
    "NETWORK",
    "SECURITY"
]


def score_text(text):

    score = 0

    for word in COMMON_WORDS:

        if word in text:
            score += 10

    common_letters = "ETAOIN"

    for ch in text:

        if ch in common_letters:
            score += 1

    return score


def dictionary_attack(ciphertext, possible_keys, mode="traditional"):

    best_score = -1

    best_text = ""

    best_key = ""

    for key in possible_keys:

        try:

            decrypted = decrypt(
                ciphertext,
                key,
                mode
            )

            s = score_text(decrypted)

            if s > best_score:

                best_score = s

                best_text = decrypted

                best_key = key

        except:
            pass

    return best_key, best_text, best_score