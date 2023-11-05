
![Logo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/th5xamgrr6se0x5ro4g6.png)


# SAiF-GPT

Project created for AECTech Hackathon 2023 @ New York.

SAiF-GPT aims to provide a solution for using Chat GPT in a secure and compliant manner, even when dealing with sensitive information. 
To ensure that corporate policies and NDAs are respected, the code and process automate entity detection and anonymization by replacing them with analogous values.
The end goal is to allow AEC industry to use AI technology like ChatGPT for document analysis while protecting confidential data.

# Getting Started with SAiF-GPT 

Before getting started with using SAiF GPT, you might want to check out Seyedomid Sajedi's repo's on building a local chatbot and using streamlit as a platform to host it.

SAif-GPT uses the streamlit platform.

1. To get started with SAif-GPT, you should clone the repo onto your local machine and install all requirements using: 

pip install -r requirements.txt

Disclaimer: We recommend setting up a local environment using Anaconda to make sure these pip-installed dependencies don't interfere with your other python projects.

2. Create a "hack_secret.txt" file within your local repository and paste your LLM API key into that file. This will allow you to call onto an api and actually have your encoded text processed by a large cloud based LLM. 

3. Once "hack_secret.txt" is saved, you can run the streamlit webapp directly from your terminal using: 

"streamlit run main2.py"

Disclaimer: The difference between main2 and main are in the NER model, main2 uses a strong NER model.

4. Streamlit should automatically open an instance of the webapp on your default browser. From there you can upload any PDF in your file browser, and ask questions about it like a traditional chatbot. The caveat, your confidential information will be "encrypted"

Contact us if you run into any issues!

![image](https://github.com/ssajedi/SAiF-GPT/assets/132618087/999757ab-6ff6-4d5f-90a1-50bb9f3f57c0)

## Known Limitations
- 512 token limits on the Local LLM, limits size of uploaded.
- Some cases of misclasified entities. (However all entities are anonymized)
- This model uses GPT-3.5-turbo.


## Usage/Examples & Future development ideas
The application could be extended to anonymize additional patterns.


## Presentation

You can access the [Presentation pdf here.](https://github.com/agusaboy)

## Team

- [Agustina Aboy](https://github.com/agusaboy)
- [Alexis Kotzambasis](https://github.com/lexiko80-LPA) 
- [Aman Sharma](https://github.com/aspeculat0r)
- [Carlos Luiz Amaral](https://www.github.com/closa1211)
- [Dan Miller](https://www.github.com/djmillerDeg)
- Kodai Endo / ek819@outlook.com
- [Omid Sajedi](https://github.com/ssajedi)
- R Yamashita / intaro0626@gmail.com
- [Samuel Winson Tanuwidjaja](https://www.github.com/samuelwt)
- [Sierra Davis](https://www.github.com/sierra-md)

Proof we were here: 

ADD PHOTOS HERE! 

## Acknowledgements

✨ Special thanks to: 
- Tamaho for helping on team comunication with translations.
- Alexander Matthias Jacobson for his initial insight on the brainstorming and being the brave on to jump out of the boat.

## License

[MIT](https://github.com/ssajedi/AInonymous/blob/main/LICENSE)


