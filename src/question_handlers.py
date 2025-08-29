import pickle

from nlu_module import extract_wh_word_answer, nlp


def handle_question_answer(question, answer_sentence):
    if question["type"] == "true_false":
        return handle_tf_question(question, answer_sentence)
    if question["type"] == "single_wh_answer":
        return handle_wh_question(question, answer_sentence)
    if question["type"] == "multiple_answer":
        return handle_multiple_question(question, answer_sentence)
    return None



def handle_wh_question(question, answer_sentence):
    question_result = {
        "question_id": question["id"],
        "question": question["question"],
        "answer": answer_sentence,
        "score": 0,
        "result": ""
    }

    if len(answer_sentence) < len(question["answer"]):
        question_result["result"] = "ambiguous"
        return question_result

    wh_answer = extract_wh_word_answer(question, answer_sentence)

    if wh_answer is None:
        #print("Using regular expression to extract answer")
        if question["answer"].lower() in answer_sentence.lower():
            question_result["score"] = question["score"]
            question_result["result"] = "correct"
        else:
            # Neither extraction via syntactic dependencies nor extraction via regex were able to extract the answer
            question_result["result"] = "incorrect"
    elif question["answer"].lower() in wh_answer.lower():
        #print("Extracted answer from syntactic dependencies")
        question_result["score"] = question["score"]
        question_result["result"] = "correct"
    else:
        #print("Extracted answer from syntactic dependencies")
        question_result["result"] = "incorrect"

    return question_result

def handle_tf_question(question, answer_sentence):
    tf_answer = extract_tf_answer(question["question"], answer_sentence)
    question_result = {
        "question_id": question["id"],
        "question": question["question"],
        "answer": answer_sentence,
        "score": 0,
        "result": ""
    }

    if tf_answer == "ambiguous" or tf_answer is None:
        # if the answer was not found in the sentence or was both affirmative and negative
        question_result["result"] = "ambiguous"
    elif question["answer"] == tf_answer:
        question_result["score"] = question["score"]
        question_result["result"] = "correct"
    else:
        question_result["result"] = "incorrect"

    return question_result


def extract_tf_answer(question, answer_sentence):
    doc = nlp(answer_sentence.lower())

    # Keywords that indicate affirmation or negation
    affirmative = {"yes", "true", "correct", "right", "sure", "confirmed", "absolutely"}
    negative = {"no", "false", "not true", "incorrect", "wrong", "i don't agree", "i disagree"}

    responce = None

    # Check for keyword-based decisions
    for sent in doc.sents:
        for word in affirmative:
            if word in sent.text.split(" "):
                responce = True
        for word in negative:
            if word in sent.text.split(" "):
                # if the response contains both affirmative and negative words
                if responce == True:
                    responce = "ambiguous"
                    break
                else:
                    responce = False
                    break

    return responce

def handle_multiple_question(question, answer_sentence):
    question_result = {
        "question_id": question["id"],
        "question": question["question"],
        "answer": answer_sentence,
        "score": 0,
        "result": ""
    }

    correct_answers = question["answer"]
    number_of_correct_answers = 0
    user_correct_answers = []
    first_time = True
    # check if there is a previous answer to the same question
    memory = pickle.load(open("memory.pkl", "rb"))
    previus_answer = None
    for i, obj in enumerate(memory["question_results"]):
        # get the previus coprrect numbers
        if obj["question_id"] == question["id"]:
            previus_answer = obj["answer"]
            first_time = False
            break


    if previus_answer is not None:
        number_of_correct_answers = len(previus_answer)
        user_correct_answers = previus_answer

    for answer in correct_answers:
        if answer.lower() in answer_sentence.lower():
            number_of_correct_answers += 1
            user_correct_answers.append(answer)


    if number_of_correct_answers >= (len(correct_answers) * (2/3)):
        question_result["score"] = question["score"]
        question_result["result"] = "correct"
    elif first_time:
        question_result["result"] = "multiple_incomplete"
    else:
        question_result["result"] = "incorrect"


    question_result["answer"] = user_correct_answers
    return question_result
