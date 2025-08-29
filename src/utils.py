import pickle

import pandas as pd
import spacy
import time
QUESTION_DATASET = pd.read_json("./questions/questions.json")


def exctract_questions(n = 1, difficulty = None, type = None):
    # get the right questions dataframe
    if difficulty and type:
        questions_dataframe = QUESTION_DATASET[
            (QUESTION_DATASET["score"] == difficulty) & (QUESTION_DATASET["type"] == type)]
    elif difficulty:
        questions_dataframe = QUESTION_DATASET[QUESTION_DATASET["score"] == difficulty]
    elif type:
        questions_dataframe = QUESTION_DATASET[QUESTION_DATASET["type"] == type]
    else:
        questions_dataframe = QUESTION_DATASET

    # get n question from dataframe

    if n > len(questions_dataframe):
        n = len(questions_dataframe)

    # get random n questions
    questions_dataframe = questions_dataframe.sample(n=n)


    question_to_return = []
    for index, row in questions_dataframe.iterrows():
        question_to_return.append(row.to_dict())

    return question_to_return


def process_final_result(USER_FRAME):
    memory = pickle.load(open("memory.pkl", "rb"))
    final_result = "" # negative, positive, almost_positive
    if USER_FRAME["score"] > 6 or (memory["correct_answers"] == USER_FRAME["number_of_questions"]):
        final_result = "positive"
    elif USER_FRAME["score"] >= 4:
        final_result = "almost_positive"
    else:
        final_result = "negative"

    return final_result

def loading(duration=1.5):
    frames = [
			"[    ]",
			"[=   ]",
			"[==  ]",
			"[=== ]",
			"[====]",
			"[ ===]",
			"[  ==]",
			"[   =]",
			"[    ]",
			"[   =]",
			"[  ==]",
			"[ ===]",
			"[====]",
			"[=== ]",
			"[==  ]",
			"[=   ]"
		]
    end = time.time() + duration
    idx = 0

    while time.time() < end:
        symbol = frames[idx % len(frames)]
        print(f'\r{symbol}', end='', flush=True)
        time.sleep(0.08)
        idx += 1
    print("", end='\r')