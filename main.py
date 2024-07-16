import streamlit as st
from openai import OpenAI
from IPython.display import Image

# Statics

# functions
def generate_story(prompt):
  story_response = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages = [{
        "role":'system',
        "content":"""You are a bestseller story writer. You will take user's prompts and generate a 100 word short story for adults aged 20-30"""
    },
                {
                    "role": "user",
                    "content": f'{prompt}'
                }],
      max_tokens = 400,
      temperature = 1
  )

  story = story_response.choices[0].message.content
  return story


def refine_image_prompt(story) -> str:
  design_response = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages = [{
        "role":'system',
        "content":"""Based on the story given, design a detailed image prompt for the cover image of this story.
        the image prompt should include the theme of the story with relevant color, suitable for adults.
        the output should be around 100 characters long."""
    },
                {
                    "role": "user",
                    "content": f'{story}'
                }],
    max_tokens = 400,
    temperature = 1
  )

  design_prompt = design_response.choices[0].message.content
  return design_prompt

def generate_image_url(image_prompt):
  cover_response = client.images.generate(
    model = 'gpt-3.5-turbo',
    prompt = image_prompt,
    size = "256x256",
    quality = 'standard',
    n = 1
  )

  image_url = cover_response.data[0].url
  return image_url

api_key = st.secrets['OPENAI_SECRET']
client = OpenAI(api_key = api_key)


with st.form(key = ' '):
  st.write('This is for user to key in information')
  msg = st.text_input('Enter your prompt here')
  
  if st.form_submit_button('Submit'):
    story = generate_story(msg)
    prompt = refine_image_prompt(story)
    image_url = generate_image_url(prompt)
    if image_url:
      st.image(image_url)
      st.balloons()
    


