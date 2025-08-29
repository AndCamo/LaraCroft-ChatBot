import random
import nlg_module, nlu_module
import question_handlers
from utils import loading, process_final_result
import pickle


USER_FRAME = {
    "name" : None,
    "score" : 0,
    "number_of_questions" : 3,
}

MEMORY = {
    "questions_asked": [],
    "question_results" : [],
    "correct_answers" : 0
}

pickle.dump(MEMORY, open("memory.pkl", "wb"))


# --- Start conversation ---
loading()
print(nlg_module.start_conversation())


# --- Extract User Info from the text ---
response = input()
loading()
user_name = nlu_module.extract_name(response)

# --- If the user doesn't provide a name, ask for it ---
while user_name is None:
    print(random.choice(nlg_module.NO_NAME_REPLIES))
    response = input()
    user_name = nlu_module.extract_person(response)

USER_FRAME["name"] = user_name

# --- interview introduction ---
adjective, introduction = nlg_module.interview_introduction(USER_FRAME["name"], response)
USER_FRAME["adjective"] = adjective

print(introduction)



# --- interview question answering ---
for index in range(USER_FRAME["number_of_questions"]):
    loading()

    # extract the first question
    question_intro, question = nlg_module.ask_question(USER_FRAME)

    print(question_intro)
    print(question["question"])
    input_text = input()

    question_result = question_handlers.handle_question_answer(question, input_text)

    # when the user answer is correct
    if question_result['result'] == 'correct':
        USER_FRAME['score'] += question_result["score"]
        # print a response for a correct answer
        print(nlg_module.handle_correct_answer(USER_FRAME, question, question_result))

    # when the user answer is NOT correct
    elif question_result['result'] == 'incorrect':
        # print a response for an incorrect answer
        print(nlg_module.handle_incorrect_answer(USER_FRAME, question, question_result))

    # when the user answer is ambiguos (answer empty, not clear, etc.)
    elif question_result['result'] == 'ambiguous':

        # ask the user to repeat the answer
        print(f"Sorry {USER_FRAME['name']}, I did not understand what you mean. Can you repeat it more clearly?")
        input_text = input()
        question_result = question_handlers.handle_question_answer(question, input_text)

        #check again the answet text
        if question_result['result'] == 'correct':
            USER_FRAME['score'] += question_result["score"]
            print(nlg_module.handle_correct_answer(USER_FRAME, question, question_result))
        elif question_result['result'] == 'incorrect':
            print(nlg_module.handle_incorrect_answer(USER_FRAME, question, question_result))
        elif question_result['result'] == 'ambiguous':
            print(f"{USER_FRAME['name']}, I am not here to be made fun of, I will take this behaviour into consideration.")
            USER_FRAME['score'] -= question_result["score"]

    # when the user has provided an incomplete answer to a "multiple_answer" question.
    elif question_result['result'] == 'multiple_incomplete':
        total_possible_answers = len(question["answer"])
        user_correct_answers = len(question_result["answer"])
        print(nlg_module.handle_multiple_incomplete_answer(USER_FRAME, question, question_result, total_possible_answers, user_correct_answers))

        # get the ramaining aswers
        input_text = input()
        question_result = question_handlers.handle_question_answer(question, input_text)
        if question_result['result'] == 'correct':
            USER_FRAME['score'] += question_result["score"]
            print(nlg_module.handle_correct_answer(USER_FRAME, question, question_result))
        elif question_result['result'] == 'incorrect':
            print(nlg_module.handle_incorrect_answer(USER_FRAME, question, question_result))

endings = [
    "That’s it for today. Give some time to think about your future.",
    "Ok, we finished. Let me think for a moment"
]
print(random.choice(endings))
loading()
result = process_final_result(USER_FRAME)
print(nlg_module.handle_final_result(USER_FRAME, result))