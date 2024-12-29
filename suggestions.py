import os
from huggingface_hub import InferenceClient

HF_API_TOKEN = os.getenv('HF_API_TOKEN')
client = InferenceClient(api_key=HF_API_TOKEN)

def get_suggestions(input_data, prediction):
    prompt = f"""
    Given the following details about a user's lifestyle and carbon footprint prediction, please provide 5 actionable suggestions to offset their carbon footprint:

    1. Body Type: {input_data['Body Type']}
    2. Gender: {input_data['Sex']}
    3. Diet: {input_data['Diet']}
    4. Social Activity Frequency: {input_data['Social Activity']}
    5. Transport: {input_data['Transport']}
    6. Monthly Vehicle Distance (km): {input_data['Vehicle Monthly Distance Km']}
    7. Frequency of Air Travel: {input_data['Frequency of Traveling by Air']}
    8. Waste Bag Size: {input_data['Waste Bag Size']}
    9. Waste Bag Weekly Count: {input_data['Waste Bag Weekly Count']}
    10. Energy Source for Heating: {input_data['Heating Energy Source']}
    11. Cooking Systems: {', '.join(input_data.get('Cooking_with_' + str(i), '') for i in range(len(input_data)) if f"Cooking_with_{i}" in input_data)}
    12. Recycling Materials: {', '.join(input_data.get(f"Do You Recyle_{x}", '') for x in input_data if f"Do You Recyle_{x}" in input_data)}
    13. Monthly Grocery Bill: {input_data['Monthly Grocery Bill']}
    14. Number of Clothes Bought Monthly: {input_data['How Many New Clothes Monthly']}
    15. TV/PC Daily Hours: {input_data['How Long TV PC Daily Hour']}
    16. Internet Daily Hours: {input_data['How Long Internet Daily Hour']}

    The carbon footprint prediction is: {prediction} grams of CO2 per month.

    Based on the above information, please provide 5 suggestions to reduce this individual's carbon footprint. These suggestions should focus on lifestyle changes, energy use, transportation, waste reduction, and consumption habits.
    (IMPORTANT) Give only the 5 suggestions , no other introductory like what data you got etc or ending text.
    """
    
    try:
        completion = client.chat.completions.create(
            model="Qwen/QwQ-32B-Preview",  
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        
        suggestions = completion.choices[0].message['content']

        suggestions_list = suggestions.split("\n")
        cleaned_suggestions = [suggestion.strip() for suggestion in suggestions_list if suggestion.strip() and not suggestion.lower().startswith('based on the above')]

        return {"suggestions": cleaned_suggestions}
    
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}
