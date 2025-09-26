from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/get-ranking/<user_id>")
def get_ranking(user_id):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("select uid, score, rank() over(order by score desc) rank from main")
    result = cursor.fetchone()

    if result is None:
        return jsonify({"error": "No user"}), 200

    data = {
        "user_id": user_id,
        "score": result[1],
        "rank": result[2], 
    }

    conn.close()
    return jsonify(data), 200 

@app.route("/set-ranking/<user_id>")
def set_ranking(user_id):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    score = request.args.get("score")

    try:
        cursor.execute(
            "INSERT OR REPLACE INTO main (uid, score) VALUES (?, ?)", 
            (user_id, score)
        )
        conn.commit()
    except Exception as e:
        return jsonify({"error": str(e), "score": score, "user_id": user_id}), 200
    finally:
        conn.close()

    return jsonify({"status":"OK"}), 200 

if __name__ == "__main__":
    app.run(debug=True)