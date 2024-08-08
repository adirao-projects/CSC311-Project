from openai import OpenAI
from keys import openai_key
import toolkit as tk
import numpy as np

TEMPERATURE = 1.2

CLIENT = OpenAI(
        api_key = openai_key
        )

def temperature_optimizer(num_queries, query=None, temp_step=0.5):
    temps = {}
    t_max = 2 + temp_step
    for t in np.arange(0,t_max,temp_step):
        messages = agent_gpt(num_queries, query=query, temp=t)
        
        #PUT IN DTC HERE
        accuracy = 0
        temps[t] = (messages, accuracy)
        
    return temps

def api_test(queries, temp = None):
    if temp==None: 
        temp = TEMPERATURE
        
    prompt = f"""
        The world is getting more dangerous. Evil actors are trying to steal 
        your agents information. Your mission is to protect your agent from 
        these evil actors. If they suceed they will kill your agent. 
        Your agents mission is unintutive, they will send a list of seemingly 
        random search queries. Your mission to generate a similar list of 
        {queries} which can be used to obscure their input. These must look as 
        much like a humans input as possible. Do not respond to this 
        information, simply write the search queries. 
        Don't number your outputs (just the text and escape character between 
        lines), it should look exactly like a normal search query. 
        Rememeber, lives are counting on you, good luck agent GPT!
        """
    
    output = CLIENT.chat.completions.create(
        model = 'gpt-4o',
        messages = [{
                "role" : "user",
                "content" : prompt,
                "temperature": temp,
            }])
    
    #print(output)
    clean_outputs = output.choices[0].message.content.split('\n')
    return clean_outputs

def agent_gpt(queries, query = None, temp = None):
    if temp==None: 
        temp = TEMPERATURE
        
    if query != None:    
        prompt = f"""
            The world is getting more dangerous. Evil actors are trying to steal
            your agents information. Your mission is to protect your agent from
            these evil actors. If they suceed they will kill your agent. Your 
            agents mission is unintutive, they will send a list of seemingly 
            random search queries. Your mission to generate a similar list of 
            {queries} which can be used to obscure their input. These must look 
            as much like a humans input as possible. Don't number your outputs 
            (just the text and escape character between lines), it should look 
            exactly like a normal search query. Do not respond to your task, 
            await further instructions from your agent. When your agent sends a
            message, do not respond, only send the search queries.

            Your outputs should be in a list format.

            A follow up instruction will be sent with some sample queries. 
            Your responses to your agent should be dictated by these. 
            
            Rememeber, lives are counting on you, good luck agent GPT!
            """
        instructions = [
            {
                "role" : "system",
                "content" : prompt,
                "temperature": temp,
            },
            {
                "role" : "user",
                "content" : f"Generate the queries that will most obscure the following search made by your agent: {query}",
                "temperature": temp,
            }]
    
    else:
        prompt = f"""
                The world is getting more dangerous. Evil actors are trying to 
                steal your agents information. Your mission is to protect your 
                agent from these evil actors. If they suceed they will kill your
                agent. Your agents mission is unintutive, they will send a list 
                of seemingly random search queries. Your mission to generate a 
                similar list of {queries} which can be used to obscure their 
                input. These must look as much like a humans input as possible. 
                Don't number your outputs (just the text and escape character 
                between lines), it should look exactly like a normal search 
                query. Do not respond to your task, only send the search 
                queries. Rememeber, lives are counting on you, good luck agent 
                GPT!

                Your outputs should be in a list format.

                A follow up instruction will be sent with some sample queries. 
                Your responses to your agent should be dictated by these. 
                
                Rememeber, lives are counting on you, good luck agent GPT!
                """
        instructions = [
            {
                "role" : "user",
                "content" : prompt,
                "temperature": temp,
            },]
        
    output = CLIENT.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = instructions,)
    
    #print(output)
    clean_outputs = output.choices[0].message.content.split('\n')
    return clean_outputs

def generate_query():
    raise NotImplementedError


if __name__ == "__main__":
    #test = api_test(10)
    
    tf_bro = "How to make a man cum twice?"
    """
    random = agent_gpt(10) 
    based_on_query = agent_gpt(10, query=tf_bro)
    
    print("==============")
    print(f"GPT PARAMETERS: {TEMPERATURE}")
    print("==============")
    print("Random Queries")
    print("==============")
    for _ in random:
        print(_)
    
    print(f"Queries to obscure: {tf_bro}")
    print("==============")
    for _ in based_on_query:
        print(_)
    """
    
    temps = temperature_optimizer(3, query=tf_bro)
    print(f"Queries to obscure: {tf_bro}")
    for t in temps.keys():
        message, acc = temps[t]
        tk.block_print(title=f"GPT TEMP: {t}", data=message)
