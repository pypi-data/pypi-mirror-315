from spacy.pipeline.spancat import preset_spans_suggester

from RFML.core.Conversation import Context
from RFML.core.Interaction import Interaction
from RFML.interface.IPromptValidator import IPromptValidator
from RFML.prompt.PromptCash import PromptCash
from RFML.prompt.PromptQuery import PromptQuery

import spacy
from spacy.matcher import Matcher


class Validator(IPromptValidator):
    nlp = spacy.load("en_core_web_sm")

    def __init__(self):
        # Load the spaCy language model
        # Initialize the Matcher
        self.matcher = Matcher(self.nlp.vocab)

    # configure prompt_queries for validation check
    def configure_prompt_queries(self, model_name: str, prompt_query_list: list[PromptQuery]):
        pass

    # process input and store in prompt_queries for validation check
    def process_prompt_queries(self, model_name: str, pc: PromptCash, user_input: str):
        pass

    def format_prompt_queries(self, model_name: str, pc: PromptCash, valid_fields, user_input: str) -> str:
        pass

    def handle_invalid_input(self, context: Context, interaction: Interaction) -> str:
        except_list = ["Hi", "Hello", "Hey", "Greetings"]
        default_response = "Could you provide additional details, please?"

        if len(interaction.input.split()) == 1:
            if interaction.input.strip().capitalize() not in except_list:
                return default_response  # "Please provide more details or ask a specific question."
        # if interaction.input.lower().strip() == "donate": return default_response
        # if interaction.input.lower().strip() == "what can": return default_response
        else:
            return self.validate_sentence_patterns(interaction.input)

    def chek_valid(self, sentence):
        # Define patterns for incomplete sentences
        patterns = [
            # Incomplete sentences like "can do?"
            [{"lower": {"in": ["can", "could", "will", "would", "shall", "should"]}}, {"dep": "ROOT"}],

            # Incomplete sentences like "what do?"
            [{"lower": {"in": ["what", "how", "why"]}}, {"dep": "ROOT"}],
        ]

        # Add the patterns to the matcher
        for pattern in patterns:
            self.matcher.add("INCOMPLETE_SENTENCE", [pattern])

        # Test sentences
        sentences = ["can do?", "what do?", "I can do it.", "what do you think?"]

        # for sentence in sentences:
        doc = self.nlp(sentence)
        matches = self.matcher(doc)

        if matches:
            # print(f"Incomplete sentence detected: '{sentence}'")
            return "None"
        else:
            # print(f"Complete sentence: '{sentence}'")
            return None

    def validate_sentence_patterns(self,sentence):
        """
        Validates if the given sentences match the expected patterns.
        """
        # Load SpaCy model
        nlp = spacy.load("en_core_web_sm")
        matcher = Matcher(nlp.vocab)

        # Define patterns to match similar sentence structures
        patterns = [
            # Pattern 1: "What’s the process for donating to Save the Children?"
            [
                {"POS": "PRON", "LOWER": "what’s"},
                {"POS": "DET", "LOWER": "the"},
                {"POS": "NOUN", "LOWER": "process"},
                {"POS": "ADP", "LOWER": "for"},
                {"POS": "VERB", "LOWER": "donating"},
                {"POS": "ADP", "LOWER": "to"},
                {"POS": "PROPN"}
            ],
            # Pattern 2: "Can you guide me on how to donate to Save the Children?"
            [
                {"POS": "AUX", "LOWER": "can"},
                {"POS": "PRON", "LOWER": "you"},
                {"POS": "VERB", "LOWER": "guide"},
                {"POS": "PRON", "LOWER": "me"},
                {"POS": "ADP", "LOWER": "on"},
                {"POS": "ADV", "LOWER": "how"},
                {"POS": "PART", "OP": "?"},
                {"POS": "VERB", "LOWER": "donate"},
                {"POS": "ADP", "LOWER": "to"},
                {"POS": "PROPN"}
            ],
            # Pattern 3: "How do I make a donation to Save the Children?"
            [
                {"POS": "ADV", "LOWER": "how"},
                {"POS": "AUX", "LOWER": "do"},
                {"POS": "PRON", "LOWER": "i"},
                {"POS": "VERB", "LOWER": "make"},
                {"POS": "DET", "LOWER": "a"},
                {"POS": "NOUN", "LOWER": "donation"},
                {"POS": "ADP", "LOWER": "to"},
                {"POS": "PROPN"}
            ]
        ]

        # Add patterns to the matcher
        for i, pattern in enumerate(patterns):
            matcher.add(f"PATTERN_{i + 1}", [pattern])

        # Process and validate each sentence
        # for sentence in sentences:

        doc = nlp(sentence)
        matches = matcher(doc)
        if matches:
            print(f"✅ The sentence '{sentence}' matches a valid pattern.")
        else:
            print(f"❌ The sentence '{sentence}' does NOT match any valid patterns.")

