from RFML.libs.NLP.CancelPrompt import CancelPrompt
from RFML.libs.NLP.NERGenerator import NERGenerator
from RFML.libs.core.DateTime import DateTime
from RFML.libs.core.Generator import Generator


class Nlp:
    gen = Generator()
    ner = NERGenerator()
    prompt = CancelPrompt()


class rf:
    datetime = DateTime()
    nlp = Nlp()
