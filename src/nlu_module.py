import spacy
import textacy

nlp = spacy.load("en_core_web_trf")


# Mapping between WH word and expected entity/dependency type
WH_MAPPING = {
    "what": ["attr", "dobj", "obj", "pobj", "acomp"],
    "who": ["nsubj", "agent", "nsubjpass"],
    "when": ["npadvmod", "pobj", "obl"],
    "where": ["pobj", "obl", "prep"],
    "which": ["attr", "dobj"],
    "how": ["advmod", "acomp"]
}

ENTITY_MAPPING = {
    "when": ["DATE", "TIME"],
    "where": ["GPE", "LOC", "FAC"],
    "who": ["PERSON", "ORG"]
}

def extract_name(text):
    """
    Extracts a name from a given text
    :param text: The input text from which the name is to be extracted.
    :return: The extracted name if found, or None if no name is identified in the text.
    """
    doc = nlp(text)

    for sent in doc.sents:
        for token in sent:
            # Cases like: "I'm Andrea", "I am Andrea"
            if token.dep_ == "ROOT" and token.lemma_ == "be":
                subj = None
                attr = None
                for child in token.children:
                    if child.dep_ == "nsubj" and child.text.lower() == "i":
                        subj = child
                    elif child.dep_ == "attr":
                        attr = child
                if subj and attr:
                    return attr.text

            # Cases like: "My name is Andrea"
            if token.text.lower() == "name" and token.dep_ == "nsubj":
                parent = token.head
                if parent.lemma_ == "be":
                    for child in parent.children:
                        if child.dep_ == "attr":
                            return child.text

    return None

def extract_person(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text

    return None


def extract_adjectives(text):
    doc = nlp(text)
    adjectives = []
    for token in doc:
        if token.pos_ == "ADJ":
            adjectives.append(token.text)
    return adjectives



def extract_wh_word_answer(question, answer_sentence):
    q_doc = nlp(question["question"])
    a_doc = nlp(answer_sentence)

    # Find WH-word in question
    wh_token = next((t for t in q_doc if t.tag_ in {"WP", "WRB"}), None)
    # print(f"wh token: {wh_token}")
    if not wh_token:
        return None

    wh_word = wh_token.text.lower()
    expected_deps = WH_MAPPING.get(wh_word, [])
    expected_ents = ENTITY_MAPPING.get(wh_word, [])

    # Find main verb in answer
    root = next((t for t in a_doc if t.dep_ == "ROOT"), None)
    # print(f"root: {root}")
    if not root:
        return None

    # Analyze verb children and look for matches
    for child in root.subtree:
        # Match for entities (e.g. DATE, GPE, etc.)
        if any(ent.label_ in expected_ents for ent in a_doc.ents):
            for ent in a_doc.ents:
                if ent.label_ in expected_ents:
                    return ent.text

        # Match for syntactic dependencies  
        if child.dep_ in expected_deps:
            span = a_doc[child.left_edge.i: child.right_edge.i + 1]
            return span.text

    return None




