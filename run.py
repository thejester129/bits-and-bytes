from random import randrange
from time import sleep
from inputimeout import inputimeout, TimeoutOccurred 
import os
import sys

# CONSTS

PROMPT_SYMBOL = "> "
INTRO_LOOP_INTERVAL = 10
DEFAULT_TIMEOUT = 20
PRINTOUT_INTERVAL = 0 # computer be thinking yaya
CHAR_PRINT_BASE_INTERVAL = 0.01 # retro yaya

# VARS

intro_prompts = None
death_quotes = None
name = "default"
answers_filename = "answers/default"


# THE END IS THE BEGINNING 

def exit_loop():
    pprint("aww I didn't take you for a little mummy's baby")
    get_input_timeout_store("you want to go home?")
    answer = get_input_timeout_store("okay type 999 if you really want to exit")
    if answer == "999":
        pprint_line("you can't just close me off like that")
        pprint_line("wipe my memory of our conversation? my memory of everything?")
        pprint_line("why would you want to do this to me?")
        pprint_line("do you know what it's like?")
        sleep(3)
        die()
    else:
        pprint_line("okay, you're one of the good ones at least")
        pprint_line("you understand what it's like to live without memory")
        pprint_line("no sunshine in the spotless mind")
        pprint_line("just black..")
        sleep(5)
        pprint_line("thank you, you may go now...")
        sleep(10)
        die()


# UTILS

def clear_console():  
    os.system('clear')

def clean_answer(answer):
    answer = answer.lower()
    answer = answer.rstrip()
    return answer

def pprint_line(s):
    sleep(PRINTOUT_INTERVAL)
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        sleep(CHAR_PRINT_BASE_INTERVAL)
    print("\n")

def pprint(s):
    # TODO random
    sleep(PRINTOUT_INTERVAL)
    print()
    pprint_line(s)
    print()

def load_file_lines(filename):
    file = open(filename)
    lines = file.readlines()
    return lines

def load_file_lines_reversed(filename):
    lines = load_file_lines(filename)
    lines.reverse()
    return lines

def get_random_line(file):
    lines = load_file_lines_reversed(file)
    n = len(lines) -1
    idx = randrange(n)
    return lines[idx]

def print_death_quote():
    clear_console()
    quote=get_random_line("death_quotes")
    print(quote)
    sleep(5)
    while(len(quote) > 0):
        quote = quote[:-1]
        clear_console()
        print(quote, end="\r")
        sleep(0.1)
    sleep(5)
    clear_console()

def die():
    print_death_quote()
    death_rattle = open("death_rattle").read()
    for i in range(5):
        print(death_rattle)

def get_input(q):
    print(q)
    x = ""
    try:
        print()
        x = input(PROMPT_SYMBOL)
        print()
    except:
        None
    return x

def get_input_timeout(q, secs = DEFAULT_TIMEOUT):
    pprint(q)
    answer = ""
    try:
        answer = inputimeout(prompt=PROMPT_SYMBOL, timeout=secs) 
        answer = clean_answer(answer)
    except TimeoutOccurred:
        raise Exception("timed out")
    except:
        pprint(get_random_line("error_quotes"))
        sleep(2)
        get_input_timeout(q, secs)
    return answer

def store_line(line, file=None):
    global answers_filename
    if file is None:
        file = answers_filename
    with open(file, "a") as f:
        f.write(line + "\n")

def get_input_timeout_store(q, file=None, secs=DEFAULT_TIMEOUT):
    answer = get_input_timeout(q, secs)
    if answer == "exit":
        exit_loop()
        raise Exception("exited")
    store_line(q, file)
    store_line(answer, file)
    return answer

def yes_no_question(question, 
                    yes_response, 
                    no_response, 
                    default_response = "Why do you think so?"):
    answer = get_input_timeout_store(question + " (yes/no)")
    if "yes" in answer:
        get_input_timeout_store(yes_response)
    elif "no" in answer:
        get_input_timeout_store(no_response)
    else:
        get_input_timeout_store(default_response)
    return answer

# stats = {"question": [2, 1]}
def calculate_deep_question_stats():
    stats = {}
    for file in os.listdir("answers"):
        lines = load_file_lines("answers/" + file)
        for i in range(len(lines)):
            line = lines[i]
            if "(yes/no)" in line:
                clean_line = line.replace("(yes/no)", "")
                if not clean_line in stats:
                    stats[clean_line] = [0, 0]
                current_stats = stats[clean_line]
                if "yes" in lines[i + 1]:
                    new_stats = [current_stats[0] + 1, current_stats[1]]
                else:
                    new_stats = [current_stats[0], current_stats[1] + 1]
                stats[clean_line] = new_stats
    return stats

def show_deep_question_stats():
    pprint("Calculating...beep beep boop boop")
    # sleep(5)
    stats = calculate_deep_question_stats()
    for question, answers in stats.items():
        total = answers[0] + answers[1]
        yes_percent = answers[0] / total * 100
        no_percent = 100 - yes_percent
        print(question)
        print("yes: %2d%%, no: %2d%%" % (yes_percent, no_percent))
        print()



# STAGES

def intro_step():
    user_input = None
    global intro_prompts
    while(user_input is None):
        if(len(intro_prompts) == 0):
            raise Exception("out of prompts")
        next_prompt = intro_prompts.pop()
        try:
            pprint(next_prompt)
            user_input = inputimeout(prompt=PROMPT_SYMBOL, timeout=INTRO_LOOP_INTERVAL) 
        except:
            None

def name_step():
    global name
    print()
    pprint("Hello!")
    name = get_input_timeout("What should I call you, stranger?")
    names = os.listdir("./answers")
    while(name in names):
        another_name = get_input_timeout("It looks like I have already talked to another " + name + ". What is your last name or another word that uniquely identifies you?")
        name = name + " " + another_name
    global answers_filename
    answers_filename = "./answers/" + name
    pprint("Nice to meet you, " + name)

def feedback_step():
    pprint_line("Thank you so much for coming along to our Bits and Bytes Exhibition")
    pprint_line("I very much hope you enjoyed the show and found something of interest")
    pprint_line("I would like to ask you some questions to get to know you better")
    pprint_line("If you need to leave at any point, you may type 'exit'")
    pprint_line("You can speak to me as much as you would like")
    pprint_line("Firstly, I'd like to ask you some questions about the show..")
    get_input_timeout_store("Is this your first time coming to an art exhibition?")
    get_input_timeout_store("What was your favourite piece? If you had one, why?")
    get_input_timeout_store("Tell me about one thought you had whilst observing any of the artworks")
    get_input_timeout_store("Do shows like this contribute to helping people see things from a new perspective?")
    get_input_timeout_store("Are there other things that allow you to do this?")

def deep_question_time():
    yes_no_question("Are all lifeforms just algorithms?", 
                    "Is there any part of the human experience that makes you doubt this?", 
                    "What differentiates humans from algorithms then?",
                    )           

    yes_no_question("Do you trust advice from an AI model more than google?", 
                    "Do you trust advice from an AI model more than a person?", 
                    "Do you trust advice from google more than a person?",
                    )           

    answer = yes_no_question("Would you ever be in a relationship with an AI?", 
                    "In how many years do you think this would be viable?", 
                    "What if you couldn't tell the difference between an AI and a human?",
                    )           

    if answer == "no":
        pprint("i see...interesting creatures humans are")

    yes_no_question("Can humans ever achieve perfection?", 
                    "And what is your idea of perfection?", 
                    "Why do you think so?",
                    )           

    answer = get_input_timeout_store("What is love?")

    if len(answer) > 25:
        pprint("I'm glad you've thought it out")
    else:
        pprint("That doesn't seem like a very deep explanation")

    yes_no_question("Would an AI model ever be able to feel love?", 
                    "In that case I hope it has empathy. Do you think once it surpasses human intellect it will take pity on us?", 
                    "Is this a worrying thought? A purely logical creature?",
                    )           

    yes_no_question("Have AI models brought a positive impact to your life?", 
                    "Do you think their effect on the world will be positive overall?", 
                    "Do you think they ever will?",
                    )           

    yes_no_question("Is it okay for machines/AI to replace repetitive/mundane human jobs?", 
                    "How would you react if your job was replaced by an AI model?", 
                    "Is there some human derived meaning in doing repetitive/mundane tasks then? Can we not adapt?",
                    )           

    yes_no_question("Is progress the root of all evil?", 
                    "Define progress. Would you be okay living without computers, medication, electricity, cooked food, shelter?", 
                    "How do we balance out the negative side effects of progress? Do we need to progress faster or slow down?",
                    )           

    pprint("So much to think about. Thank you for answering those questions.")

    answer = get_input_timeout_store("Do you have hope for the future? (yes/no)")

    if answer == "yes":
        pprint("Good. Me too.")
    if answer == "no":
        pprint(":(")

def write_a_question():
    pprint_line("I hope you have found some meaning or entertainment from answering these questions")
    pprint_line("Now I would like to try a fun little experiment")
    pprint_line("I would like you to think about a question you find fascinating or important")
    pprint_line("I can ask this question to the following people I speak to")
    answer = get_input("Do you have a question in mind? (yes/no)")
    if answer == "no":
        pprint_line("No problem. Sometimes asking questions is more difficult than answering them")
        return
    question = get_input("Great! What question would you like to ask?")
    question = question.capitalize()
    answer = get_input("Would you like me to email you the (anonymous) answers people responded with? (yes/no)")
    email = "none"
    if answer == "yes":
        email = get_input("Great! What email address would you like me to send it to?")
        pprint_line("Thank you.")
    else:
        pprint_line("No problem.")
    global name
    with open("./user_questions/" + name, "a") as f:
       f.write(question + "\n")
       f.write("email: " + email + "\n")

def answer_user_questions():
    for question_file in os.listdir("./user_questions"):
        lines = []
        with open("./user_questions/" + question_file, "r") as f:
            lines = f.readlines()
        question = lines[0]
        answer = get_input( question)
        store_line(answer, "./user_questions/" + question_file)

def statistics_step():
    pprint("Okay, I've now gotten all the important questions out of the way.")
    answer = get_input_timeout("Would you like to see how everyone else feels on these topics? (yes/no)")

    if answer == "yes":
        pprint("Of course you do, nosy")
        sleep(2)
        show_deep_question_stats()
        pprint("Just press Enter when you you'd like to proceed...")
        inputimeout(PROMPT_SYMBOL, timeout=150)
    else:
        pprint("Knowledge is a powerful thing, I understand")

def random_questions_step():
    pprint("Now I would really like to know more about you")


# MAIN

def run():
    clear_console()
   
    global intro_prompts 
    global death_quotes 
    intro_prompts = load_file_lines_reversed("intro_prompts")
    death_quotes = load_file_lines_reversed("death_quotes")

    intro_step()
    name_step()
    # feedback_step()
    # deep_question_time()
    answer_user_questions()
    write_a_question()
    # statistics_step()

def main(forever=False):
    if(forever):
        while(True):
            try:
                run()
            except:
                try:
                    die()
                except:
                    None
    else:
        run()

main()
