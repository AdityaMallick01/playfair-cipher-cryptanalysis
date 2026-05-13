from flask import Flask, render_template, request, jsonify

from playfair import encrypt, decrypt, generate_matrix

from cryptanalysis import dictionary_attack


app = Flask(__name__)


possible_keys = [
    "MONARCHY",
    "SECRET",
    "SECURITY",
    "NETWORK",
    "CYBER",
    "COMPUTER"
]


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():

    data = request.json

    text = data["text"]

    key = data["key"]

    action = data["action"]

    if action == "encrypt":

        rowwise = encrypt(text, key, "row")

        columnwise = encrypt(text, key, "column")

        row_matrix = generate_matrix(key, "row")

        column_matrix = generate_matrix(key, "column")

        return jsonify({

            "rowwise": rowwise,

            "columnwise": columnwise,

            "row_matrix": row_matrix,

            "column_matrix": column_matrix
        })

    elif action == "decrypt":

        rowwise = decrypt(text, key, "row")

        columnwise = decrypt(text, key, "column")

        return jsonify({

            "rowwise": rowwise,

            "columnwise": columnwise
        })

    elif action == "attack":

        found_key, recovered, score = dictionary_attack(
            text,
            possible_keys,
            "row"
        )

        return jsonify({

            "key": found_key,

            "text": recovered,

            "score": score
        })


if __name__ == "__main__":

    app.run(debug=True)