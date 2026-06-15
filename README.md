### Safety and Cost Control

This chatbot includes pre-LLM guardrails to reduce unnecessary API usage.  
Before calling the OpenAI API, the app checks whether the user's question is related to Wentao Jiang's profile, projects, skills, education, or work experience.  
Off-topic questions and prompt-injection attempts are handled with a fixed refusal message without calling the LLM.
