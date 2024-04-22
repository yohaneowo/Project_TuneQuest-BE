import os
import time
from openai import OpenAI, api_key
from src.prompt_assistant.search import semantic_search_by_prompt as ssearch_prompt
from dotenv import load_dotenv


load_dotenv()

CREATIVE_ASSISTANT_ID = os.getenv("CREATIVE_ASSISTANT_ID")
GOOD_MEMEORY_ASSISTANT_ID = os.getenv("GOOD_MEMEORY_ASSISTANT_ID")

client = OpenAI()
api_key = os.getenv('OPENAI_API_KEY')


def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )


def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")


def create_thread_and_run(assistant_id, user_input):
    thread = client.beta.threads.create()
    run = submit_message(assistant_id, thread, user_input)
    return thread, run


def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run


def extract_prompt(text):
    # This function extracts the text enclosed by <prompt> and </prompt> tags from a given string.
    start_tag = "<prompt>"
    end_tag = "</prompt>"
    
    # Find the positions of the start and end tags
    start_pos = text.find(start_tag)
    end_pos = text.find(end_tag)
    
    # Extract and return the text between the tags, if both tags are found
    if start_pos != -1 and end_pos != -1:
        return text[start_pos + len(start_tag):end_pos].strip()
    else:
        return "Prompt tags not found or incomplete."


def assemble_responses(messages):
    response = ""
    for m in messages:
        if(m.role != "user"):
            response += f"小幫手:\n {m.content[0].text.value}\n"
    return response


def prompt_suggestion(question):
    question = question.strip()
    thread, run = create_thread_and_run(CREATIVE_ASSISTANT_ID, question)
    run = wait_on_run(run, thread)
    response_messages = get_response(thread)

    first_response = assemble_responses(response_messages)
    suggested_promprt = extract_prompt(first_response)
    full_response= first_response.replace("<prompt>", "").replace("</prompt>", "")

    return {"suggested_promprt": suggested_promprt, "full_response": full_response}


def prompt_remix(query):
    query = query.replace("@explore", "").replace("@history", "").replace("@remix", "").strip()
    similar_prompts = prompt_retrieve(query)
    question = f"音樂敘述:\n {query}\n\n類似的prompt:\n"
    for i in range(len(similar_prompts)):
        question += f"{i+1}. {similar_prompts[i]}\n"

    question += "\n"

    thread, run = create_thread_and_run(GOOD_MEMEORY_ASSISTANT_ID, question)
    run = wait_on_run(run, thread)
    response_messages = get_response(thread)

    first_response = assemble_responses(response_messages)
    suggested_promprt = extract_prompt(first_response)
    full_response = first_response.replace("<prompt>", "").replace("</prompt>", "")
    
    return {"suggested_promprt": suggested_promprt, "similar_prompts": similar_prompts, "full_response": full_response}


def check_startwith_keyword(input_text):
    input_text_lower = input_text.lower()
    return input_text_lower.startswith(("@explore", "@history", "@remix"))


def prompt_retrieve(question):
    cursor = ssearch_prompt(question, 3)
    similar_prompts = []
    for t in cursor:
        similar_prompts.append(t["prompt"])
    return similar_prompts