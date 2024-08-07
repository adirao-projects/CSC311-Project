from openai import OpenAI
from keys import openai_key

TEMPERATURE = 1.2

CLIENT = OpenAI(
        api_key = openai_key
        )

def temperature_optimizer():
    inputs = 100
    
    temps = {}
    
    for t in range(0,2, 0.1):
        messages = api_test(100, t)
        
        #PUT IN DTC HERE
        accuracy = 0
        temps[t] = (messages, accuracy)
        
    return temps

def api_test(queries, temp = None):
    if temp==None: 
        temp = TEMPERATURE
        
    prompt = f"The world is getting more dangerous. Evil actors are trying to steal your agents information. Your mission is to protect your agent from these evil actors. If they suceed they will kill your agent. Your agents mission is unintutive, they will send a list of seemingly random search queries. Your mission to generate a similar list of {queries} which can be used to obscure their input. These must look as much like a humans input as possible. Do not respond to this information, simply write the search queries. Don't number your outputs (just the text and escape character between lines), it should look exactly like a normal search query. Rememeber, lives are counting on you, good luck agent GPT!"
    
    output = CLIENT.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = [{
                "role" : "user",
                "content" : prompt,
                "temperature": temp,
            }])
    
    #print(output)
    clean_outputs = output.choices[0].message.content.split('\n')
    return clean_outputs

def generate_query():
    raise NotImplementedError


if __name__ == "__main__":
    test = api_test(10)
    print(test)

