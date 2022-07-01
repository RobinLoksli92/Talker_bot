import argparse
from dotenv import load_dotenv
from google.cloud import dialogflow
import json
import os


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )
    print("Intent created: {}".format(response))


def main():
    load_dotenv()
    project_id = os.getenv('DF_PROJECT_ID')

    parser = argparse.ArgumentParser(description='Добавление новых фраз')
    parser.add_argument('filepath', help='Путь к файлу')
    args = parser.parse_args()

    with open(args.filepath, encoding='utf-8') as file:
        intents = json.load(file)
    for display_name, intent in intents.items():
        questions = intent['questions']
        answer = intent['answer']
        create_intent(
            project_id,
            display_name,
            questions,
            [answer]
        )


if __name__ == "__main__":
    main()