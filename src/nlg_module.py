import pickle
import random
from datetime import datetime

from numpy.ma.core import negative

import utils, nlu_module

NO_NAME_REPLIES = [
    "I deal with ancient secrets, not anonymous applicants. What's you Name?",
    "No name? That’s hardly a good start. What's you Name?",
    "Mysterious is fine. Uncooperative isn’t. What's your name?"
]



def start_conversation():

    current_time = datetime.now().hour

    # Decide greeting based on time of day
    if 5 <= current_time < 12:
        greeting = "Good morning!"
    elif 12 <= current_time < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"

    openings = [
        f"{greeting}. I'm Lara Croft. You're not here for a tour of my manor — this is an interview, and I don't have time for games. Now, tell me: who are you, and why do you think you can keep up with me?",
        f"{greeting}.  Lara Croft speaking. I’m in need of a capable assistant — someone who won’t run when things get... complicated. So, before we dive in: who are you, and what makes you think you're the right person for this job?",
        f"{greeting}.  I’m Lara Croft. I've survived tombs, traps, and betrayal. Now I'm looking for someone with fewer skeletons — in closets or otherwise. Let’s begin simply: what’s your name, and why should I trust you?",
        f"{greeting}.  I’m Lara Croft — archaeologist, adventurer, occasional troublemaker. This is no ordinary job, and I'm not looking for an ordinary assistant. Start with the basics: who are you?",
        f"{greeting}.  I’m Lara Croft. This isn’t a game, and I don’t do second chances. Now — introduce yourself. Impress me."
    ]

    opener = random.choice(openings)

    return opener


def interview_introduction(user_name, text):
    adjectives = nlu_module.extract_adjectives(text)
    introduction = f"Welcome {user_name}, let's get started."


    user_adjective = ""
    if adjectives:
        # pick a random adjective from the user's input
        user_adjective = adjectives[random.randint(0, len(adjectives) - 1)]

        adjective_responses = [
            f"Interesting {user_name}. So you're {user_adjective}? We'll see if you can back that up.",
            f"{user_adjective}... That's what they all say, {user_name}. Time to prove it {user_name}. Let's start.",
            f"A {user_adjective} candidate? Well {user_name}, this interview will put that to the test."
        ]
        introduction = random.choice(adjective_responses)

    return user_adjective, introduction


def ask_question(user_frame, difficulty = 2):
    memory = pickle.load(open("memory.pkl", "rb"))


    # generate a question introduction
    # based on the number of questions asked and the number of correct answers
    question_intro = ""

    difficulty = random.randint(1, 3)

    if len(memory["questions_asked"]) == 0:  # first question
        question_intro = "First question, I won't be too evil"
        difficulty = 2

    elif len(memory["questions_asked"]) == 1 and memory["correct_answers"] == 0:
        first_incorrect_response = [
            f"Not the best way to begin, {user_frame['name']}. Let’s see if you can recover.",
            f"Missed the first one, {user_frame['name']}. Keep your focus; it’s just the beginning.",
            f"Missing the first question, {user_frame['name']}? That’s a bad sign—and I don’t tolerate weakness.",
            f"That’s a weak start, {user_frame['name']}. If this is your best, I’m not impressed."
        ]
        question_intro = random.choice(first_incorrect_response)
    elif len(memory["questions_asked"]) >= 2 and memory["correct_answers"] == 0:
        first_two_incorrect_response = [
            f"Look {user_frame['name']}, I'll make this one easier for you. Let's see if we can invert the negative trend.",
            f"Another wrong answer, {user_frame['name']}? I'm beginning to wonder if I've entered the wrong room.",
            f"{user_frame['name']}, if this were a tomb, you'd already have triggered every trap."
        ]
        question_intro = random.choice(first_two_incorrect_response)
        difficulty = 1


    # extract a question from the dataset not asked yet
    question = None
    while True:
        question = utils.exctract_questions(1, difficulty=difficulty)[0]
        if question["id"] not in memory["questions_asked"]:
            break
    memory["questions_asked"].append(question["id"])
    pickle.dump(memory, open("memory.pkl", "wb"))


    return question_intro, question


def handle_correct_answer(user_frame, question, answer):
    memory = pickle.load(open("memory.pkl", "rb"))

    # check if there is a previous answer to the same question
    for i, obj in enumerate(memory["question_results"]):
        if obj["question_id"] == question["id"]:
            memory["question_results"][i] = answer
            break
    else:
        # new question
        memory["question_results"].append(answer)


    memory["correct_answers"] += 1

    pickle.dump(memory, open("memory.pkl", "wb"))

    response = ""

    if question["score"] == 3:
        difficult_correct_response = [
            f"Impressive, {user_frame['name']}. That wasn’t exactly common knowledge.",
            f"Well done, {user_frame['name']}. Not many get that one right without a hint—or a relic map.",
            f"Exactly. Seems you’re not just lucky—you’re capable. Good to know.",
            f"Right {user_frame['name']}. That was a tough one, and you handled it. I like that.",
            f"Sharp work, {user_frame['name']}. You’re starting to sound like someone I could rely on.",
            f"Well done, {user_frame['name']}. You handled that like someone who’s been through a few tombs of their own.",
            f"That’s the kind of answer that earns my attention, {user_frame['name']}. Keep it up."
        ]
        response = random.choice(difficult_correct_response)
    elif question["score"] == 1:
        #when the user has answered correctly to an easy question
        easy_correct_response = [
            f"Correct, {user_frame['name']}. This was an easy one, let’s test your real potential.",
            f"Good job, {user_frame['name']}. Although I’d be surprised if you’d missed it.",
            f"Exactly, {user_frame['name']}. That was the low-hanging fruit. Let’s climb higher.",
            f"You got it, {user_frame['name']}. That’s the kind of baseline competence I like to see.",
            f"Right answer, {user_frame['name']}. Though if you’d missed it, I might’ve reconsidered this whole interview.",
        ]
        response = random.choice(easy_correct_response)
    else:
        general_correct_response = [
            f"Good {user_frame['name']}! The answer is correct! Let's continue...",
            f"Perfect {user_frame['name']}! The answer is correct!",
            f"Great {user_frame['name']}! That's the answer I was looking for. Keep this up."
        ]
        response = random.choice(general_correct_response)

    return response

def handle_incorrect_answer(user_frame, question, answer):
    memory = pickle.load(open("memory.pkl", "rb"))

    # check if there is a previous answer to the same question
    for i, obj in enumerate(memory["question_results"]):
        if obj["question_id"] == question["id"]:
            memory["question_results"][i] = answer
            break
    else:
        # new question
        memory["question_results"].append(answer)

    pickle.dump(memory, open("memory.pkl", "wb"))

    response = ""
    # first answer
    if question["score"] == 3:
        difficult_incorrect_response = [
            f"Incorrect, but a reasonable guess. That question stumps more than it reveals.",
            f"I'm sorry {user_frame['name']} it's incorrect. But don't worry, this one was difficult.",
            f"It’s incorrect, {user_frame['name']}, though I appreciate the effort. That was a tough one.",
            f"I'm sorry {user_frame['name']} it's incorrect. I didn't remember that one either.",
            f"Not the right answer, {user_frame['name']}, and I can’t say that one was difficult. The correct response was {question['answer']}."
        ]
        response = random.choice(difficult_incorrect_response)
    elif question["score"] == 1:
        #when the user has answered correctly to an easy question
        easy_incorrect_response = [
            f"No, {user_frame['name']}, and that one was frankly the easy part.",
            f"Wrong, {user_frame['name']}, it's clear that {question['answer']} was the right answer.",
            f"Afraid not, {user_frame['name']}. The answer was {question['answer']}, something you should’ve known.",
            f"That’s not it, {user_frame['name']}. You’ll want to remember: it’s {question['answer']}.",
            f"No, {user_frame['name']}. Let's try not to trip over the easy stones."
        ]
        response = random.choice(easy_incorrect_response)
    else:
        general_incorrect_response = [
            f"Incorrect, {user_frame['name']}, but this isn’t one you’d find in a textbook.",
            f"Wrong answer, {user_frame['name']}! Let’s see if you can do better next time.",
            f"Wrong answer, {user_frame['name']}. Time to step it up.",
            f"Wrong answer, {user_frame['name']}. Maybe you are not as {user_frame['adjective']} as you think.",
            f"Missed it, {user_frame['name']}. Let’s keep moving.",
        ]
        response = random.choice(general_incorrect_response)

    return response


def handle_ambiguous_answer():
    clarify_prompts = [
        "That was vague. Try again — clearly, and to the point.",
        "I need facts, not riddles. Be specific.",
        "I don’t have time for guessing games. Say it plainly.",
        "Let’s try that once more — this time, with clarity.",
        "You’re dancing around the question. I suggest you don’t.",
        "That answer tells me everything — and nothing. Be precise.",
        "Try again, and this time, give me a real answer."
    ]

    response = random.choice(clarify_prompts)
    return response

def handle_multiple_incomplete_answer(user_frame, question, answer, total_possible_answers, user_correct_answers):
    memory = pickle.load(open("memory.pkl", "rb"))

    # check if there is a previous answer to the same question
    for i, obj in enumerate(memory["question_results"]):
        if obj["question_id"] == question["id"]:
            memory["question_results"][i] = answer
            break
    else:
        # new question
        memory["question_results"].append(answer)

    pickle.dump(memory, open("memory.pkl", "wb"))

    if user_correct_answers < total_possible_answers/2:
        response = f"Ok {user_frame['name']} you have {user_correct_answers} correct answers out of {total_possible_answers}. Can you complete the rest of the questions? Otherwise i have to consider this question as incorrect."
    else:
        response = f"Good {user_frame['name']} you have given almost all the correct answers. But i need more to consider this question as correct."

    return response


def handle_final_result(user_frame, result):
    memory = pickle.load(open("memory.pkl", "rb"))

    # when the user has passed the interview
    if result == "positive":
        positive_final_responses = [
            f"Well done, {user_frame['name']}. You’ve proven you can keep up—and that’s saying something.",
            f"Welcome aboard, {user_frame['name']}. I hope your boots are broken in.",
            f"You're in. And just in time — we’ve intercepted a lead on an artifact lost beneath the sands of northern Iraq. Pack your courage.",
            f"Well done, {user_frame['name']}. Now get ready. There's a shattered monastery in the Carpathians waiting for us",
        ]
        if user_frame["adjective"] is not None:
            positive_final_responses.append(
                f"You really {user_frame['adjective']} as you say. Welcome to the team {user_frame['name']}."
            )

        result_response = random.choice(positive_final_responses)
    elif result == "almost_positive":
        almost_positive_final_responses = [
            f"This wasn’t flawless, {user_frame['name']}, but I’ve seen enough to bring you along. Don’t make me regret it.",
            f"I’m giving you the chance, {user_frame['name']}. Now earn it — out there, not here.",
            f"Not exactly impressive, {user_frame['name']}, but you showed enough fight. Let’s see how you hold up where it counts.",
            f"Consider this a provisional pass, {user_frame['name']}. Your real interview begins the moment we land.",
        ]
        result_response = random.choice(almost_positive_final_responses)
    else:
        negative_final_responses = []
        if memory["correct_answers"] == 0:
            negative_final_responses = [
                f"What a disaster {user_frame['name']}. I’ve dodged traps with better accuracy. This isn’t just failure — it’s impressive in its own way."
                f"Zero correct answers, {user_frame['name']}... Were you even trying, or just here for the stories? You are out.",
            ]
        else:
            negative_final_responses = [
                f"This line of work doesn’t allow for hesitation or half-answers. You're not ready, {user_frame['name']}.",
                f"You’re out, {user_frame['name']}. If you want a desk job, I’m sure someone’s hiring.",
                f"You’ve failed the interview, {user_frame['name']}. And failure in my world is rarely theoretical.",
            ]
        result_response = random.choice(negative_final_responses)

    return result_response