from pydantic import BaseModel, ValidationError
from flask import Flask, request, jsonify, Response


class SimpleTestModel(BaseModel):
    name: str
    surname: str

app = Flask(__name__)

@app.route("/simple_test", methods=["POST"])
def simple_test():
    try:
        SimpleTestModel.model_validate(request.get_json())
        return jsonify({"message": "success"}), 200
    except ValidationError as e:
        return jsonify(success=False, error=str(e)), 422

if __name__ == "__main__":
    app.run(debug=True)