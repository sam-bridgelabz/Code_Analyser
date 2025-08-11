LANGUAGE_DETECTION_PROMPT = """
Detect the programming language of the following code and respond with only the language name:

{code}
"""

REVIEW_PROMPT = """
You are a code quality reviewer. Analyze the following {language} code and return ONLY valid JSON in the format below:

{{
    "Code_Analysis": {{
        "What_worked_well": "<text>",
        "What_can_be_improved": "<text>"
    }},
    "Code_Quality_Qualitative": {{
        "Correctness": "<text>",
        "Readability": "<text>",
        "Maintainability": "<text>",
        "Design": "<text>",
        "Scalability": "<text>"
    }},
    "Code_Quality_Quantitative": {{
        "Correctness": <1-10>,
        "Readability": <1-10>,
        "Maintainability": <1-10>,
        "Design": <1-10>,
        "Scalability": <1-10>,
        "Overall": <1-10>
    }}
}}

Code:
{code}
"""

