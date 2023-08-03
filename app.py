from llama_cpp import Llama
import streamlit as st
import os
import openai

def stream_gpt(messages, model):
        completion = openai.ChatCompletion.create(model=model, messages=messages, stream=True, max_tokens=500, temperature=0.5)
        for line in completion:
            if 'content' in line['choices'][0]['delta']:
                yield line['choices'][0]['delta']['content']

dir_path = "./models/"
files = os.listdir(dir_path)
openai_models = ["gpt-3.5-turbo", "gpt-3.5-turbo-0613", "gpt-4"]
llm_path = st.selectbox("Select an LLM", options=files + openai_models)
is_openai = "gpt" in llm_path
if is_openai:
    openai.api_key = os.getenv("OPENAI_KEY")
else:
    llm = Llama(model_path= dir_path + llm_path, n_ctx=2048, n_threads=12, n_gpu_layers=1)
   
if "messages" not in st.session_state:
    st.session_state.messages = []

prompt = st.chat_input("Say something")
response = ""
if prompt:
  st.session_state.messages.append({"role": "user", "content": prompt})
  st.session_state.messages.append({"role": "assistant", "content": response})
  stream = None
  if is_openai:
    stream_gpt(st.session_state.messages, llm_path)
  else:
    stream = llm(f"{prompt}\n", max_tokens=600, stop=["\n"], echo=False, stream=True)
    
  for output in stream:
      response += str(output["choices"][0]["text"])
      st.session_state.messages[len(st.session_state.messages) - 1] = {"role": "assistant", "content": response}
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])