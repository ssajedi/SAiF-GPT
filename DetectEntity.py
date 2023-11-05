# Use a pipeline as a high-level helper
import csv
import random
from transformers import pipeline
# Load model directly
from transformers import AutoTokenizer, AutoModelForTokenClassification
import json
from itertools import groupby
import re
from copy import deepcopy

class DetectEntity(object):

    pipe = pipeline("token-classification", model="mdarhri00/named-entity-recognition")
    tokenizer = AutoTokenizer.from_pretrained("mdarhri00/named-entity-recognition")
    model = AutoModelForTokenClassification.from_pretrained("mdarhri00/named-entity-recognition")
    usedWords = []
    # Dictionary of all enities detected
    entities = {}
    # Dictionary of all the replaced data
    replacedData = {}

    def __init__(self, text):
        self.text = text

    """ 
    Swaps the email information with a generic email address
    """
    def RemoveEmail(self) -> str:
        
        changedText = deepcopy(self.text)

        email_pattern = re.compile(r'''
        [a-zA-Z0-9._%+'-]+        # username part, with added '+' and '-'
        @                          # @ symbol
        [a-zA-Z0-9.-]+             # domain name part
        (?<!\.\.)                  # negative lookbehind to ensure no double dots
        \.[a-zA-Z]{2,}             # dot-something
        ''', re.VERBOSE)
        matches = email_pattern.findall(changedText)    
        matches = list(set(matches))
        outData = []

        for indx, val in enumerate(matches): 
            replacedVal = f"_Email_{indx}"
            changedText = changedText.replace(val, replacedVal)
            outData.append({"original": val, "replaced": replacedVal})

        self.replacedData["email"] = outData

        self.text = changedText
        return changedText

    """
    Swaps the phone number with a generic phone number
    """
    def RemovePhone(self) -> str:

        changedText = deepcopy(self.text)

        phone_pattern = re.compile(r'''
            (\+?\d{1,3}\s?)?                     # optional country code
            (\(?\d{3}\)?[\s.-]?)?                # optional area code with optional separator after
            (\d{3})                              # first 3 digits
            ([\s.-]?\d{4})                       # optional separator followed by last 4 digits
            (\s*(ext|x|ext.)\s*\d{2,5})?         # extension
            ''', re.VERBOSE)

        matches = phone_pattern.findall(changedText)
        matches = [''.join(match).strip() for match in matches if match[2] and match[3]]

        matches = list(set(matches))
        outData = []

        for indx, val in enumerate(matches): 
            replacedVal = "0" * (10 - len(f'{indx}')) + f"{indx}"
            changedText = changedText.replace(val, replacedVal)
            outData.append({"original": val, "replaced": replacedVal})

        self.replacedData["number"] = outData
        self.text = changedText
        return changedText

    """
    Swaps the detected entities with a generic entity name
    """
    def RemoveDetected(self) -> str:
        
        for key, val in self.entities.items():
            i = 1
            for entity in val:
                if key == 'Person_Name':
                    repVal = 'PersonName' + str(i)
                elif key == 'location':
                    repVal = 'LocationName' + str(i)
                elif key == 'Organization_Name':
                    repVal = 'OrganizationName' + str(i)
                else:
                    repVal = 'OtherEntityName' + str(i)

                self.text = self.text.replace(entity, repVal)
                self.replacedData[key].append({"original": entity, "replaced": repVal})
                i += 1

        with open(r'data\ChangedText.txt', 'w+') as outfile:
             outfile.write(self.text)
        
    """
    Swaps the words in the user prompt
    """
    def UserPromptReplace(self, text) -> str:
        try:
            for key in self.replacedData.keys():
                for val in self.replacedData[key]:
                    if isinstance(val, dict): 
                        newval = val['original']
                        oldval = val['replaced']
                        text = re.sub(r'\b{}\b'.format(newval), oldval, text)
        except Exception as e:
            print(f'Error: {e} in UserPromptReplace')
        return text


    """
    Swaps the words in the reply to the user
    """
    def ReplyToUser(self, text) -> str:
        try:
            for key in self.replacedData.keys():
                for val in self.replacedData[key]:
                    if isinstance(val, dict): 
                        newval = val['replaced']
                        oldval = val['original']
                        text = re.sub(r'\b{}\b'.format(newval), oldval, text)
        except Exception as e:
            print(f'Error: {e} in ReplyToUser')
        return text

    """
    Get the original text
    """
    def InfillDetected(self, text) -> str:
        
        try:
            for key in self.replacedData.keys():
                for val in self.replacedData[key]:
                    if isinstance(val, dict): 
                        oldval = val['original']
                        newval = val['replaced']
                        text = re.sub(r'\b{}\b'.format(newval), oldval, text)
        except Exception as e:
            print(f'Error: {e} in InfillDetected') 

        with open(r'data\OriginalText.txt', 'w+') as outfile:
            outfile.write(text)
        with open(r'data\replacedText.txt', 'w+') as outfile:
            for key, val in self.replacedData.items():
                outfile.write(f'{key}: {val}\n')

        return text
    
    """
    Detect using te HuggingFace pipeline
    """
    def Detect(self) :

        # Clean data for the email 
        self.RemoveEmail()
        # Clean data for the phone number
        self.RemovePhone()

        # Get the model's tokenizer
        inputs = self.tokenizer(self.text, return_tensors="pt")
        outputs = self.model(**inputs)    
        # Get the predicted token label IDs as a list of integers
        predictions = outputs.logits.argmax(-1).tolist()[0]  # Convert to list and get first item
        # Map labels to actual tokens
        tokens = self.tokenizer.convert_ids_to_tokens(inputs.input_ids[0])
        results = [(token, self.model.config.id2label[prediction]) for token, prediction in zip(tokens, predictions)]
        outData = []

        for i in range(len(results)):
            if results[i][1] != "O":
                outData.append(results[i])

        # Clean the data
        self.CleanData(self.CombineTokens(outData))        

    """
    Combine tokens to a list
    """
    def CombineTokens(self, tokenized_list) -> list:
        combined_names = []
        current_name = ''
        for token, token_type in tokenized_list:
            if token.startswith('##'):
                current_name += token[2:]  # Remove '##' and concatenate
            else:
                if current_name:  # If there's a current name, append it to the list
                    combined_names.append((current_name, token_type))
                current_name = token  # Start a new name
        # Add the last name if the list didn't end with '##'
        if current_name:
            combined_names.append((current_name, token_type))
        return combined_names

    """
    Clean the data
    """
    def CleanData(self, data: list) -> dict:
        
        uniqueKeys = set([val for key, val in data])
        for key in uniqueKeys:
            self.entities[key] = []
            self.replacedData[key] = []

        # Pattern for the regex characters
        pattern = re.compile('[A-Za-z]')
        outData = [data for data in data if pattern.search(data[0])]

        # Remove duplicates
        outData.sort(key=lambda x: x[0])
        outData = [next(group) for key, group in groupby(outData, lambda x: x[0])]
        # Remove any single character
        outData = [data for data in outData if len(data[0]) != 1]

        # Combine the data with unique keys
        for key in uniqueKeys:
            for data in outData:
                dataKey, dataVal = data
                if  key == dataKey:
                    self.entities[key].append(dataVal)
                if key == dataVal:
                    self.entities[key].append(dataKey)

        return self.entities
    

if __name__ == "__main__":

    # test = """
    #        ExxonMobil Infrastructure Development Proposal
            # Executive Summary:
            # This comprehensive proposal envisions the construction of ExxonMobil's new operational hub,
            # designed to bolster its strategic expansion and operational excellence within the energy sector.
            # Introduction:
            # We propose to construct a state-of-the-art facility that reflects ExxonMobil's commitment to innovation,
            # sustainability, and global leadership in energy. The project will span a meticulously selected 35,000-square-foot 
            # site in Houston, Texas, with the potential to become a landmark of industrial prowess and architectural ingenuity.
            # Project Team:
            # Leading the project will be Chief Project Engineer, Thomas Booker, with over two decades of experience in industrial
            # construction. Architectural design will be spearheaded by Ava Clarke, whose portfolio includes several LEED-certified
            # buildings across Dallas. Our environmental engineering efforts will be led by Dylan Rhodes in Austin, ensuring adherence
            # to the most stringent ecological standards.
            # Site and Structure:
            # The facility will be located in the heart of Houston’s Energy Corridor, taking advantage of the area's rich
            # infrastructure and proximity to ExxonMobil’s main operations. Geotechnical assessments and site preparation will be
            # undertaken by Houston-based expert, Nora Quintana. The building's framework, designed for resilience and adaptability, 
            # will be overseen by structural engineer Alex Johnson from Fort Worth.
            # Sustainability and Environment:
            # Sustainability Coordinator, Rachel Santos from Corpus Christi, will implement cutting-edge green technologies, 
            # including a state-of-the-art HVAC system designed by El Paso's mechanical engineer, Omar Fernandez. Rainwater
            # harvesting and waste management systems will be developed in collaboration with environmental specialists from Galveston 
            # test@gmail.com
            # 123-456-7890
            # """
    
    with open(r'data\test.txt', 'r') as infile:
        test = infile.read()
    cls = DetectEntity(test)
    cls.Detect()
    cls.RemoveDetected()
    cls.InfillDetected(cls.text)

    print(cls.UserPromptReplace("Who is Rachel Santos?"))
    print(cls.ReplyToUser("""
                        PersonName11 is designated as the Sustainability Coordinator for the proposed construction of OrganizationName1's 
                          new operational hub. They are based in LocationName9, within the region of LocationName4 LocationName2.
                          Their role involves implementing cutting-edge green technologies in the facility, including a 
                          state-of-the-art HVAC system. This system is designed by the mechanical engineer, PersonName8, from
                           OrganizationName2. PersonName11's responsibilities also include overseeing the development of rainwater
                           harvesting and waste management systems, in collaboration with environmental specialists from
                           OrganizationName3. This indicates that PersonName11 is likely to have a background in environmental
                           engineering or sustainability practices, and is tasked with ensuring that the new facility meets high
                           environmental standards and incorporates sustainable practices into its design and operation.
"""))
    pass