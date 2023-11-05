# AInonymous
AEC Tech hackathon

```mermaid
sequenceDiagram
    participant UserInput
    participant Anonymizer
    participant GPT
    participant Deanonymize
    participant UserOutput

    UserInput->>Anonymizer: Input
    Anonymizer->>GPT: Anonymized Data
    GPT->>Deanonymize: Processed Data
    Deanonymize->>UserOutput: Output
