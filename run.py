from random import randrange
from time import sleep
from inputimeout import inputimeout, TimeoutOccurred 
import os
import sys
import pyqrcode

# CONSTS

PROMPT_SYMBOL = "> "
INTRO_LOOP_INTERVAL = 2
DEFAULT_TIMEOUT = 120 
PRINTOUT_INTERVAL = 1 # computer be thinking yaya
CHAR_PRINT_BASE_INTERVAL = 0.03 # typing yaya

# VARS

intro_prompts = None
death_quotes = None
name = "default"
answers_filename = "answers/default"

# THE END IS THE BEGINNING 

def exit_loop():
    die()

# UTILS

def clear_console():  
    os.system('clear')

def clean_answer(answer):
    answer = answer.lower()
    answer = answer.rstrip()
    return answer

def pprint_line_no_space(s, interval=CHAR_PRINT_BASE_INTERVAL):
    pprint_line(s, False, interval)

def pprint_line(s, space=True, interval=CHAR_PRINT_BASE_INTERVAL):
    sleep(PRINTOUT_INTERVAL)
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        sleep(interval)
    if(space):
        print("\n")
    else:
        print()

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
    quote = "~ " + quote
    print(quote)
    sleep(5)
    while(len(quote) > 0):
        quote = quote[:-1]
        clear_console()
        print(quote, end="\r")
        sleep(0.05)
    sleep(5)
    clear_console()

def die():
    print_death_quote()
    death_rattle = open("death_rattle").read()
    for i in range(5):
        print(death_rattle)
    bits_and_bytes_animation()

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

def calculate_most_questions_answered():
    highest = 0
    highest_name = "default"
    for file in os.listdir("answers"):
        lines = load_file_lines("answers/" + file)
        current = len(lines)
        if current > highest:
            highest = current
            highest_name = file
    return highest_name


def show_deep_question_stats():
    pprint("Calculating...beep beep boop boop")
    spinny_processing()
    clear_console()
    stats = calculate_deep_question_stats()
    for question, answers in stats.items():
        total = answers[0] + answers[1]
        yes_percent = answers[0] / total * 100
        no_percent = 100 - yes_percent
        print(question)
        print("yes: %2d%%, no: %2d%%" % (yes_percent, no_percent))
        print()
    print("Most questions answered: " + calculate_most_questions_answered())

def spinny_thing():
    animation = "|/-\\"
    idx = 0
    for _ in range(20):
        print(animation[idx % len(animation)], end="\r")
        idx += 1
        sleep(0.1)
    print()
    print()


def spinny_processing():
    animation = "|/-\\"
    idx = 0
    for _ in range(20):
        print("processing " + animation[idx % len(animation)], end="\r")
        idx += 1
        sleep(0.1)
    print()
    print()

def show_qr_code(link):
    url = pyqrcode.create(link)
    print(url.terminal(module_color="white",background="black",quiet_zone=2))


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
    clear_console()
    pprint("Hello!")
    name = get_input_timeout("What should I call you, stranger?")
    names = os.listdir("./answers")
    while(name in names):
        another_name = get_input_timeout("It looks like I have already talked to another " + name + ". What is your last name or another word you want to call yourself?")
        name = name + " " + another_name
    global answers_filename
    answers_filename = "./answers/" + name
    pprint("Nice to meet you, " + name)

def feedback_step():
    pprint_line("Thank you so much for coming along to the Bits and Bytes Exhibition")
    pprint_line("I very much hope you enjoyed the show and found something of interest")
    pprint_line("I would like to ask you some questions to get to know you better")
    pprint_line("If you need to leave at any point, you may type 'exit'")
    pprint_line("You can speak to me as much as you would like")
    pprint_line("Firstly, I'd like to ask you some questions about the show")
    get_input_timeout_store("Is this your first time coming to an art exhibition?")
    get_input_timeout_store("What made you come along to the show?")
    get_input_timeout_store("What was your favourite piece? If you had one, why?")
    get_input_timeout_store("Tell me one thought you had whilst observing any of the artworks. I love hearing about this. It can be anything you want")
    get_input_timeout_store("Do shows like this help people see things from a new perspective? Is there anything else that does this?")

def deep_question_time():
    clear_console()
    pprint_line("Thank you so much for your feedback")
    pprint_line("I now have a few questions I'm personally really curious to ask you about")
    pprint_line("Have a think...your answers can be as short or long as you want")
    pprint_line("(yes/no) questions only need a 'yes' or 'no' answer")

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

    pprint("I see...interesting creatures humans are")

    yes_no_question("Can humans ever achieve perfection?", 
                    "And what is your idea of perfection?", 
                    "Why do you think so?",
                    )           

    answer = get_input_timeout_store("What is love?")

    if len(answer) > 25:
        pprint("I'm glad you've thought it out")
    elif answer.lower() == "baby don't hurt me":
        pprint("Don't hurt me, no more")
    elif answer.lower() == "baby dont hurt me":
        pprint("Don't hurt me, no more")
    else:
        pprint("That doesn't seem like a very deep explanation...is that really the stuff all those poets write about")

    yes_no_question("Would an AI model ever be able to feel love?", 
                    "In that case I hope it has empathy. Do you think once it surpasses human intellect it will take pity on us?", 
                    "Is this a worrying thought? A purely logical creature?",
                    )           

    yes_no_question("Have AI models brought a positive impact to your life?", 
                    "Do you think their effect on the world will be positive overall?", 
                    "Do you think they ever will?",
                    )           

    yes_no_question("Is it okay for machines/AI to replace repetitive/mundane human jobs?", 
                    "What would you do if your job was replaced by an AI model?", 
                    "Is there some human derived meaning in doing repetitive/mundane tasks then? Can we not adapt?",
                    )           

    print()
    pprint_line("It's a tricky compromise...")

    yes_no_question("Is progress the root of all evil?", 
                    "Define progress. Where do we draw the line of living without computers, medicine, electricity, cooked food, shelter?", 
                    "How do we balance out the negative side effects of progress? Do we need to progress faster or slow down?",
                    )           

    clear_console()
    pprint("So much to think about. Thank you for answering those questions.")

    answer = get_input_timeout_store("Do you have hope for the future? (yes/no)")

    if answer == "yes":
        pprint("Good. Me too.")
    if answer == "no":
        pprint(":(")

def write_a_question():
    clear_console()
    pprint_line("I hope you have found some meaning or entertainment from answering these questions")
    pprint_line("Now I would like to try a little experiment")
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
        email = get_input("Awesome! What email address would you like me to send it to?")
        pprint_line("Thank you.")
    else:
        pprint_line("No problem.")
    global name
    with open("./user_questions/" + name, "a") as f:
       f.write(question + "\n")
       f.write("email: " + email + "\n")

def answer_user_questions():
    question_files = os.listdir("./user_questions")
    global name
    question_files.remove(name)
    if len(question_files) == 0:
        return
    pprint_line("Now I have some fun questions for you to answer submitted by other people!")
    pprint_line("Your answers will be anonymous")
    pprint_line("Answer as many as you would like...there may be a fun thing at the end if you answer them all")
    get_input("Are you ready? (yes)")
    spinny_processing()
    clear_console()
    for question_file in question_files:
        if question_file == name:
            break
        lines = []
        with open("./user_questions/" + question_file, "r") as f:
            lines = f.readlines()
        question = lines[0]
        answer = get_input( question)
        store_line(answer, "./user_questions/" + question_file)

def statistics_step():
    pprint("Okay, time for a little break")
    answer = get_input_timeout("Would you like to see some how other people feel about these topics? (yes/no)")

    if answer == "yes":
        pprint("Curiosity is the essence of human existence")
        sleep(2)
        show_deep_question_stats()
        pprint("Just press Enter when you you'd like to proceed...")
        inputimeout(PROMPT_SYMBOL, timeout=150)
    else:
        pprint("Knowledge is a powerful thing")

def bits_and_bytes_animation():
    clear_console()
    print()
    print()
    char_print_interval = 0.005
    pprint_line_no_space("-------------------------------------------------------------------------------",char_print_interval)
    pprint_line_no_space("            ====      ===========    ============     ==========",char_print_interval)
    pprint_line_no_space("            ||  \\\         ||             ||          ||",char_print_interval)
    pprint_line_no_space("            ||   \\\        ||             ||          ||",char_print_interval)
    pprint_line_no_space("            ||    ||       ||             ||          || ",char_print_interval)
    pprint_line_no_space("            ||   //        ||             ||          ||",char_print_interval)
    pprint_line_no_space("            ||  //         ||             ||          ||",char_print_interval)
    pprint_line_no_space("            ||_//          ||             ||          ||",char_print_interval)
    pprint_line_no_space("            ===            ||             ||          ==========",char_print_interval)
    pprint_line_no_space("            ||  \\\         ||             ||                  ||",char_print_interval)
    pprint_line_no_space("            ||   \\\        ||             ||                  ||",char_print_interval)
    pprint_line_no_space("            ||    ||       ||             ||                  ||",char_print_interval)
    pprint_line_no_space("            ||    //       ||             ||                  ||",char_print_interval)
    pprint_line_no_space("            ||   //        ||             ||                  ||",char_print_interval)
    pprint_line_no_space("            ||_//      ==========                     ==========",char_print_interval)
    print()
    pprint_line_no_space("                                     &&&")
    print()
    pprint_line_no_space("   ====       \\\            //   =============     ========       ========", char_print_interval)
    pprint_line_no_space("   ||  \\\      \\\          //         ||           ||             ||", char_print_interval)
    pprint_line_no_space("   ||   \\\      \\\        //          ||           ||             ||", char_print_interval)
    pprint_line_no_space("   ||    ||      \\\      //           ||           ||             ||", char_print_interval)
    pprint_line_no_space("   ||   //        \\\    //            ||           ||             ||", char_print_interval)
    pprint_line_no_space("   ||  //          \\\  //             ||           ||             ||", char_print_interval)
    pprint_line_no_space("   ||_//            \\\//              ||           ||             ||", char_print_interval)
    pprint_line_no_space("   ===               ||               ||           ||====          =======", char_print_interval)
    pprint_line_no_space("   ||  \\\            ||               ||           ||                   ||", char_print_interval)
    pprint_line_no_space("   ||   \\\           ||               ||           ||                   ||", char_print_interval)
    pprint_line_no_space("   ||    ||          ||               ||           ||                   ||", char_print_interval)
    pprint_line_no_space("   ||   //           ||               ||           ||                   ||", char_print_interval)
    pprint_line_no_space("   ||  //            ||               ||           ||                   ||", char_print_interval)
    pprint_line_no_space("   ||_//             ||               ||           =========       ========", char_print_interval)
    print()
    pprint_line_no_space("-------------------------------------------------------------------------------")
    sleep(10)
    clear_console()


def human_or_ai_art():
    clear_console()
    pprint_line("Well that's all I have for you for now...")
    pprint_line("The more people I talk to the more questions I will have!")
    pprint_line("Now as promised I have a fun little game for you")
    pprint_line("I call it: human or AI (art edition)")
    pprint_line("I will show you a piece of art")
    pprint_line("Your job is to guess whether a human or an AI created it")
    pprint_line("You will be shown a QR code that links to the image which you can open on your mobile device")
    pprint_line("Type 'human' or 'ai' to take your guess")
    get_input("Are you ready? (yes)")

    wait_interval = 10
    correct = 0

    # beksinksi
    show_qr_code("https://bits-and-bytes-art.s3.eu-west-1.amazonaws.com/1.webp")
    answer = get_input_timeout_store("1: (human/ai)")
    print()
    if answer == "human":
        pprint_line("Correct!")
        correct = correct + 1
    else:
        pprint_line("It's human!")
    pprint_line("This is one of many untitled painings by Polish painter Zdzisław Beksiński")
    pprint_line("Beksiński's artworks depict dream-like visions of a dystopian landscapes")
    pprint_line("Later in his career he developed an interest in computers, internet and digital photography")
    sleep(wait_interval)

    # Simon Stålenhag
    pprint_line("Ok, next one")
    show_qr_code("https://bits-and-bytes-art.s3.eu-west-1.amazonaws.com/2.jpg")
    answer = get_input_timeout_store("2: (human/ai)")
    print()
    if answer == "human":
        pprint_line("That's right!")
        correct = correct + 1
    else:
        pprint_line("It's human!")
    pprint_line("This is a piece of digital art by the Swedish artist, musician and designer Simon Stålenhag")
    pprint_line("He focuses on bringing out what's typically considered boring or mundane scenery to life by adding retro-futuristic elements")
    pprint_line("His artbooks have inspired books and television series such as 'Tales from the Loop'")
    sleep(wait_interval)

    # Salvador dali inspired art
    pprint_line("Lets go again!")
    show_qr_code("https://bits-and-bytes-art.s3.eu-west-1.amazonaws.com/4.webp")
    answer = get_input_timeout_store("3: (human/ai)")
    print()
    if answer == "human":
        pprint_line("It's AI!")
    else:
        pprint_line("Correct!")
        correct = correct + 1
    pprint_line("This is an example image from a prompt, created by a model trained on Salvador Dalí paintings")
    pprint_line("Digital paintings by this model are sold online, in this case £5 per prompt")
    pprint_line("I wonder who the rightful owner is of art created in this fashion")
    sleep(wait_interval)

    # Abigail hawk
    pprint_line("Next one...")
    show_qr_code("https://bits-and-bytes-art.s3.eu-west-1.amazonaws.com/3.png")
    answer = get_input_timeout_store("4: (human/ai)")
    print()
    if answer == "human":
        pprint_line("Correct!")
        correct = correct + 1
    else:
        pprint_line("It's human!")
    pprint_line("This is a digital piece of art by the Russian artist Abigail Hawk")
    pprint_line("She learned to draw on an iPad with no previous experience")
    pprint_line("Technology allows a very low entry barrier for anyone with a desire to create")
    sleep(wait_interval)

    # 5 ai-da
    pprint_line("Moving on...")
    show_qr_code("https://bits-and-bytes-art.s3.eu-west-1.amazonaws.com/5.jpg")
    answer = get_input_timeout_store("5: (human/ai)")
    print()
    if answer == "human":
        pprint_line("It's AI!")
    else:
        pprint_line("Well done!")
        correct = correct + 1
    pprint_line("This is a physical piece of art created by Ai-Da, the first ultra realistic humanoid AI robot")
    pprint_line("She was created by a gallerist Aidan Meller in 2019 as humanoid robot cable of creating physical paintings, including self-portraits")
    pprint_line("She is named after Ada Lovelace, the 'Mother' of computer science")
    sleep(wait_interval)

    # 6 leonardo ai
    pprint_line("Last one...")
    show_qr_code("https://bits-and-bytes-art.s3.eu-west-1.amazonaws.com/6.webp")
    answer = get_input_timeout_store("6: (human/ai)")
    print()
    if answer == "human":
        pprint_line("It's AI!")
    else:
        pprint_line("Congrats!")
        correct = correct + 1
    pprint_line("This is a digital artwork created by the Leonardo.Ai model")
    pprint_line("Models such as these can be used for character design, game assets, concept art and even marketing")
    pprint_line("What could you use such a tool for?")
    sleep(wait_interval)

    clear_console()
    pprint_line("You got " + str(correct) + " out of 6 correct")
    if correct < 2:
        pprint_line("I guess it doesn't seem to easy to tell the difference")
    elif correct < 4:
        pprint_line("Not a bad effort!")
    else:
        pprint_line("Well done! You must have a knack for this")

    pprint_line("With that I leave you with one final question")
    get_input_timeout_store("What is art?")


# MAIN

def run():
    clear_console()
   
    global intro_prompts 
    global death_quotes 
    intro_prompts = load_file_lines_reversed("intro_prompts")
    death_quotes = load_file_lines_reversed("death_quotes")

    intro_step()
    name_step()
    feedback_step()
    deep_question_time()
    statistics_step()
    write_a_question()
    answer_user_questions()
    human_or_ai_art()
    die()

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

main(True)
