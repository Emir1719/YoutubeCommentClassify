import openai

class OpenAIService:
    def __init__(self, api_key):
        openai.api_key = api_key

    def classify_comment(self, comment):
    # Yorumun hangi kategoriye ait olduğunu anlaması için modelin yönlendirilmesi
        prompt = f"""
{comment}
Categorize the following comment. Respond with only one of these categories: Positive, Negative, Question or Donation.
Positive: Positive remarks, appreciative comments, guidance, or religious quotations.
Negative: Insults, negative remarks, criticism, derogatory comments, or promotion of beliefs contradicting Islam.
Question: Inquiries about Islamic topics, religious matters, or the channel.
Donation: Expressions of intent to donate or questions related to donations.
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
            
        print(category)
        
        return category
