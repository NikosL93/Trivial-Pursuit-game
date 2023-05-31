import requests


class Question:  # Κλάση για τη δημιουργία του format της κάθε ερώτησης

    def __init__(self, q_text, q_answer):
        self.text = q_text
        self.answer = q_answer


def get_data(difficulty, category):  # Συνάρτηση για τη δημιουργία της λίστας των ερωτήσεων
    parameters = {
        "amount": 9,
        "type": "boolean",
        "difficulty": difficulty,
        "category": category
    }

    response = requests.get("https://opentdb.com/api.php", params=parameters)
    response.raise_for_status()  # Raise an exception if the HTTP response status code indicates an error
    data = response.json()  # εξαγωγή σε μορφή json τα δεδομένα του api
    question_data = data["results"]
    print("Length of question_data:", len(question_data))
    print("question_data:", question_data)
    question_bank = []  # Η λίστα των ερωτήσεων
    for question in question_data:
        question_text = question["question"]  # Ανάθεση στη μεταβλητή την ερώτηση (κείμενο) απο το κλειδί "question"
        question_answer = question["correct_answer"]  # Ανάθεση στη μεταβλητή τη σωστή απάντηση απο το κλειδί "correct_answer"
        new_question = Question(question_text, question_answer)  # δημιουργεί αντικείμενο κλάσης Question
        question_bank.append(new_question)  # Εισαγωγή στη λίστα της μεταβλητής new_question (με παραμέτρους την ερώτηση και την απάντηση)
    return question_bank





