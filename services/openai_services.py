import openai

class OpenAIService:
    def __init__(self, api_key):
        openai.api_key = api_key

    def classify_comment(self, comment):
    # Yorumun hangi kategoriye ait olduğunu anlaması için modelin yönlendirilmesi
        prompt = f"""
{comment}
Which category does this comment belong to? Answer only category's name
Positive: Appreciative and positive comments, guidance messages, quotations from religious books
Negative: Derogatory remarks, insults, negative criticism, insults to Islam, support for different beliefs
Question: Questions about Islamic/religious topics or the channel
Donation: Intent to make a monetary donation or questions about donations
    """

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt.strip()}
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini-2024-07-18",
                messages=messages,
                max_tokens=5,
                temperature=0
            )
            category = response.choices[0].message['content'].strip()
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            category = "Uncategorized"
        
        return category
