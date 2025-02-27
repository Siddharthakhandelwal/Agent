import requests
from firecrawl import FirecrawlApp
from groq import Groq
import tiktoken

def groq_trans_querr(trans):
  groq_api="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"

  client = Groq(api_key=groq_api)

  chat_completion = client.chat.completions.create(
      messages=[
          {
              "role": "system",
              "content": "you are a helpful assistant."
          },
          {
              "role": "user",
              "content": f"you have this {trans} , you need to just return a question which user asked and required internet connection to answer just return them",
          }
      ],

      model="llama-3.3-70b-versatile",
      temperature=0.5,
      max_completion_tokens=1024,
      top_p=1,
      stop=None,
      stream=False,
  )

  # Print the completion returned by the LLM.
  print(chat_completion.choices[0].message.content)
  return chat_completion.choices[0].message.content
def crawl_web(querry):
  app = FirecrawlApp(api_key="fc-cffd0abdf63f46c0b029afd6d25c92bc")
  groq_api="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"
  search_engine="AIzaSyDMS2uBldD8l3xhT-B-5Etza0MLP26L3L0"
  engine_id="a49a4c9e1acce490d"
  tokenizer = tiktoken.get_encoding("cl100k_base") 
  client = Groq(api_key=groq_api)

  def groq_suum(data,querry):
      chat_completion = client.chat.completions.create(
          messages=[
              {
                  "role": "system",
                  "content": "you are a helpful assistant."
              },
              {
                  "role": "user",
                  "content": f"you have this {data} , summarize it according to user querry ,{querry} and try to extract and return the valuable info",
              }
          ],

          model="llama-3.3-70b-versatile",
          temperature=0.5,
          max_completion_tokens=1024,
          top_p=1,
          stop=None,
          stream=False,
      )

      # Print the completion returned by the LLM.
      print(chat_completion.choices[0].message.content)
      return chat_completion.choices[0].message.content
  url="https://www.googleapis.com/customsearch/v1"
  para={
      'q':querry,
      'key':search_engine,
      'cx':engine_id,
  }
  response=requests.get(url,params=para)
  results=response.json()
  if 'items' in results:
      target_url = results['items'][0]['link']
      print(f"Found URL: {target_url}")
      scrape_result = app.scrape_url(target_url, params={'formats': ['markdown', 'html']})
      data=scrape_result['markdown']
      tokens = tokenizer.encode(data)

# Keep only the first 6000 tokens
      trimmed_tokens = tokens[:5000]
      trimmed_text = tokenizer.decode(trimmed_tokens)

      print(f"Original tokens: {len(tokens)}, Trimmed tokens: {len(trimmed_tokens)}")
      data=groq_suum(trimmed_text,querry)
      return data


def to_check_querr(call_id):
  auth_token = '4529e07b-e40b-441d-81e4-ffeee189f40b'
  url = f"https://api.vapi.ai/call/{call_id}"
  headers = {
      'Authorization': f'Bearer {auth_token}',
      'Content-Type': 'application/json',
  }
  while True:
    response = requests.get(url, headers=headers)
    trans = response.json()
    if trans['status'] =='ended':
      
      transcript= trans['transcript']
      querry = groq_trans_querr(transcript) # type: ignore
      answer=crawl_web(querry)
      return answer
     
# to_check_querr("d379f518-4a5d-477d-b229-d2e1204dfdf2")