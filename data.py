import requests
from question_model import Question

def get_data(difficulty):
    parameters = {
        "amount": 3,
        "type": "boolean",
        "difficulty": difficulty
    }

    response = requests.get("https://opentdb.com/api.php", params=parameters)
    response.raise_for_status()
    data = response.json() # εξαγωγή σε μορφή json τα δεδομένα του api
    question_data = data["results"]
    question_bank = []
    for question in question_data:
        question_text = question["question"]
        question_answer = question["correct_answer"]
        new_question = Question(question_text, question_answer) #δημιουργεί αντικείμενο κλάσσης Question
        question_bank.append(new_question)

    return question_bank
