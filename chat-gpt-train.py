from openai import OpenAI
from keys import openai_key_adi
from keys import openai_key_david
import toolkit as tk
import numpy as np

TEMPERATURE = 1.2

MAX_STR_LENGTH = 256000

CLIENT = OpenAI(
        api_key = openai_key_adi
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

def get_user_queries(uid):
    f = open(f"./user_data/{uid}_real.txt", "r").read()
    
    print(len(f))

    if len(f) > MAX_STR_LENGTH/2:
        split_inputs = []
        running_count = 0
        input_lst = []
        for search in f.split('\n'):
            if running_count < MAX_STR_LENGTH/2 :
                running_count += len(search)
                input_lst.append(search)
            else:
                running_count = 0
                split_inputs.append('\n'.join(input_lst[:]))
                input_lst = []
                
        if running_count != 0:
            split_inputs.append('\n'.join(input_lst[:]))
            
        return split_inputs
        
    else:
        return [f.strip('\n')]

def agent_gpt(queries, user_id, temp = None):
    print("SENDING")
    if temp==None: 
        temp = TEMPERATURE

    query = get_user_queries(user_id)
    
    thread = CLIENT.beta.threads.create()
    assistant_id = "asst_LXtqp01t1YTv3QkQwgKF4orV"
    
    sys_message = CLIENT.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=f"Generate {queries} in total (output should be a list of length \
        {queries} queries) based on the following list of queries. Generate \
            only after the Agent says 'Start Mission Agent GPT'. ",)
    
    for sub_q in query:
        CLIENT.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=sub_q,)
    
    sys_message = CLIENT.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=f"Start Mission Agent GPT",)
    
    
    run = CLIENT.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id,
        )
    print("WAITING")
    while run.status in ["queued", "in_progress"]:
        keep_retrieving_run = CLIENT.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id
        )

        # If the run status is completed
        if keep_retrieving_run.status == "completed":
            # Retrieve the assistant's response
            all_messages = CLIENT.beta.threads.messages.list(
                thread_id=thread.id)

            # Display the assistant's response
            save_sample_queries(user_id, 
                                all_messages.data[0].content[0].text.value)
            return all_messages.data[0].content[0].text.value

            break
        elif keep_retrieving_run.status in ["queued", "in_progress"]:
            pass
        else:
            break

    print("SAVING")

def save_sample_queries(uid, query_lst):
    save_queries = '\n'.join([x[2:] for x in query_lst.split("\n")])
    #print(save_queries)
    f = open(f"./user_data/{uid}_real_GPT.txt", "w")
    f.write(save_queries)
    f.close()

if __name__ == "__main__":
    #test = api_test(10)
    outputs = {}
    
    NUM_QUERIES = 50
    uids =  ["71845", "6124931", "3817598", "5288646", "18350315"]
    for u in uids:
        print(f"RUNNING {u}")
        outputs[u] = agent_gpt(NUM_QUERIES, u)
    
    print(outputs)    
    # tf_bro = "How to make a man cum twice?"
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
    
    # temps = temperature_optimizer(3, query=tf_bro)
    # print(f"Queries to obscure: {tf_bro}")
    # for t in temps.keys():
    #     message, acc = temps[t]
    #     tk.block_print(title=f"GPT TEMP: {t}", data=message)
