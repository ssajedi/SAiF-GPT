import re
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

class Anonymizer:
    def __init__(self, model_name="Babelscape/wikineural-multilingual-ner"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForTokenClassification.from_pretrained(model_name)
        self.nlp = pipeline("ner", model=self.model, tokenizer=self.tokenizer, grouped_entities=True)
        self.entity_counters = {}
        self.anonymization_map = {}
        self.deanonymization_map = {}
        self.phone_regex = re.compile(r'\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\b')
        self.email_regex = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}')

    def _split_text(self, text, chunk_size=60):
        words = text.split()
        for i in range(0, len(words), chunk_size):
            yield ' '.join(words[i:i+chunk_size])

    def _get_anonymized_label(self, entity_group):
        if entity_group not in self.entity_counters:
            self.entity_counters[entity_group] = 1
        anonymized_label = f"{entity_group.lower()}{self.entity_counters[entity_group]}"
        self.entity_counters[entity_group] += 1
        return anonymized_label

    def _anonymize_with_regex(self, text, regex, entity_group):
        matches = regex.finditer(text)
        shift = 0
        for match in matches:
            entity_text = match.group()
            if entity_text not in self.anonymization_map:
                anonymized_label = self._get_anonymized_label(entity_group)
                self.anonymization_map[entity_text] = anonymized_label
                self.deanonymization_map[anonymized_label] = entity_text

            start, end = match.span()
            start += shift
            end += shift
            text = text[:start] + self.anonymization_map[entity_text] + text[end:]
            shift += len(self.anonymization_map[entity_text]) - (end - start)

        return text

    def _anonymize_chunk(self, chunk, entity_types):
        # Anonymize phone numbers and emails first
        if 'PHONE-NUM' in entity_types:
            chunk = self._anonymize_with_regex(chunk, self.phone_regex, 'PHONE-NUM')
        if 'EMAIL' in entity_types:
            chunk = self._anonymize_with_regex(chunk, self.email_regex, 'EMAIL')

        # Proceed with NER-based anonymization
        ner_results = self.nlp(chunk)
        shift = 0
        for entity in ner_results:
            if entity['entity_group'] in entity_types:
                entity_text = entity['word']
                if entity_text not in self.anonymization_map:
                    anonymized_label = self._get_anonymized_label(entity['entity_group'])
                    self.anonymization_map[entity_text] = anonymized_label
                    self.deanonymization_map[anonymized_label] = entity_text

                start = entity['start'] + shift
                end = entity['end'] + shift
                chunk = chunk[:start] + self.anonymization_map[entity_text] + chunk[end:]
                shift += len(self.anonymization_map[entity_text]) - (end - start)

        return chunk

    def anonymize(self, text, entity_types, chunk_size=60):
        chunks = list(self._split_text(text, chunk_size=chunk_size))
        anonymized_chunks = []

        for chunk in chunks:
            anonymized_chunk = self._anonymize_chunk(chunk, entity_types)
            anonymized_chunks.append(anonymized_chunk)

        return ' '.join(anonymized_chunks)

    # def deanonymize(self, anonymized_text):
    #     for anonymized_entity, original_entity in self.deanonymization_map.items():
    #         anonymized_text = anonymized_text.replace(anonymized_entity, original_entity)
    #     return anonymized_text

    def deanonymize(self, anonymized_text):
        # Sort keys by length in descending order to replace longer keys first
        for anonymized_entity in sorted(self.deanonymization_map.keys(), key=len, reverse=True):
            original_entity = self.deanonymization_map[anonymized_entity]
            # Use regular expressions to match whole words
            anonymized_text = re.sub(r'\b' + re.escape(anonymized_entity) + r'\b', original_entity, anonymized_text)
        return anonymized_text

    def get_anonymization_map(self):
        return self.anonymization_map
