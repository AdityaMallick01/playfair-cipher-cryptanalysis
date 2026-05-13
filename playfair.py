ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"


def prepare_key(key):

    key = key.upper().replace("J", "I")

    result = ""

    for ch in key:

        if ch in ALPHABET and ch not in result:

            result += ch

    for ch in ALPHABET:

        if ch not in result:

            result += ch

    return result


def generate_matrix(key, mode="row"):

    key = prepare_key(key)

    matrix = []

    if mode == "row":

        for i in range(0, 25, 5):

            row = list(key[i:i + 5])

            # reverse alternate rows
            if (i // 5) % 2 == 1:

                row.reverse()

            matrix.append(row)

    elif mode == "column":

        matrix = [['' for _ in range(5)]
                  for _ in range(5)]

        idx = 0

        for col in range(5):

            for row in range(5):

                matrix[row][col] = key[idx]

                idx += 1

    return matrix


def find_position(matrix, char):

    for i in range(5):

        for j in range(5):

            if matrix[i][j] == char:

                return i, j

    return None


def prepare_text(text):

    text = text.upper().replace("J", "I")

    text = ''.join(filter(str.isalpha, text))

    prepared = ""

    i = 0

    while i < len(text):

        a = text[i]

        if i + 1 < len(text):

            b = text[i + 1]

            if a == b:

                prepared += a + "X"

                i += 1

            else:

                prepared += a + b

                i += 2

        else:

            prepared += a + "X"

            i += 1

    return prepared


def encrypt_pair(matrix, a, b):

    r1, c1 = find_position(matrix, a)

    r2, c2 = find_position(matrix, b)

    # Same row
    if r1 == r2:

        return (
            matrix[r1][(c1 + 1) % 5] +
            matrix[r2][(c2 + 1) % 5]
        )

    # Same column
    elif c1 == c2:

        return (
            matrix[(r1 + 1) % 5][c1] +
            matrix[(r2 + 1) % 5][c2]
        )

    # Rectangle rule
    else:

        return (
            matrix[r1][c2] +
            matrix[r2][c1]
        )


def decrypt_pair(matrix, a, b):

    r1, c1 = find_position(matrix, a)

    r2, c2 = find_position(matrix, b)

    # Same row
    if r1 == r2:

        return (
            matrix[r1][(c1 - 1) % 5] +
            matrix[r2][(c2 - 1) % 5]
        )

    # Same column
    elif c1 == c2:

        return (
            matrix[(r1 - 1) % 5][c1] +
            matrix[(r2 - 1) % 5][c2]
        )

    # Rectangle rule
    else:

        return (
            matrix[r1][c2] +
            matrix[r2][c1]
        )


def encrypt(text, key, mode="row"):

    matrix = generate_matrix(key, mode)

    text = prepare_text(text)

    cipher = ""

    for i in range(0, len(text), 2):

        cipher += encrypt_pair(
            matrix,
            text[i],
            text[i + 1]
        )

    return cipher


def decrypt(cipher, key, mode="row"):

    matrix = generate_matrix(key, mode)

    cipher = cipher.upper()

    plain = ""

    for i in range(0, len(cipher), 2):

        plain += decrypt_pair(
            matrix,
            cipher[i],
            cipher[i + 1]
        )

    return clean_plaintext(plain)


def clean_plaintext(text):

    cleaned = ""

    i = 0

    while i < len(text):

        # remove inserted X
        if (
            i > 0 and
            i < len(text) - 1 and
            text[i] == "X" and
            text[i - 1] == text[i + 1]
        ):

            i += 1

        else:

            cleaned += text[i]

            i += 1

    # remove trailing X
    if cleaned.endswith("X"):

        cleaned = cleaned[:-1]

    return cleaned