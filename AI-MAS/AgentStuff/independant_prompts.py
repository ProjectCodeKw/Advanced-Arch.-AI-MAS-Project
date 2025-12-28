
def EASY_PROMPTS():
    # test_prompts.py
    """
    Test Prompts for Multi-Agent System Benchmarking
    100 prompts organized by complexity (number of independent subtasks)
    """
    prompts = {
    # ================================================================
    # CATEGORY 1: SINGLE TASK (25 prompts)
    # ================================================================
    "single_task": [
        "Generate a Python code to loop through a list and print its values",
        "Define what is artificial intelligence",
        "Calculate 15 plus 27",
        "Explain what is machine learning",
        "Translate hello to Arabic",
        "Write Python code to add two numbers",
        "Describe what is a neural network",
        "Calculate 100 minus 45",
        "Write Python code to find the maximum of three numbers",
        "Define what is an algorithm",
        "Calculate 12 multiplied by 8",
        "Write Python code to reverse a string",
        "Explain what is cloud computing",
        "Calculate the square of 9",
        "Translate thank you to Arabic",
        "Write Python code to check if a number is even",
        "Describe what is the internet",
        "Calculate 50 divided by 5",
        "Write Python code to calculate the sum of a list",
        "Define what is a database",
        "Translate good morning to Arabic",
        "Explain what is encryption",
        "Translate goodbye to Arabic",
        "Translate welcome to Arabic",
        "Translate computer to Arabic"
    ],
    
    # ================================================================
    # CATEGORY 2: TWO INDEPENDENT TASKS (25 prompts)
    # ================================================================
    "two_tasks": [
        "Define what is artificial intelligence AND explain what is machine learning",
        "Calculate 15 plus 27 AND calculate 100 minus 45",
        "Write Python code to print Hello World AND define what is programming",
        "Translate good morning to Arabic AND translate good evening to Arabic",
        "Describe what is a neural network AND define what is an algorithm",
        "Calculate 12 multiplied by 8 AND calculate the square of 9",
        "Write Python code to add two numbers AND explain what is addition",
        "Explain what is cloud computing AND describe what is the internet",
        "Calculate 10 plus 20 AND translate hello to Arabic",
        "Write Python code to reverse a string AND describe what is a string",
        "Define what is a database AND explain what is encryption",
        "Calculate 50 divided by 5 AND calculate 20 plus 30",
        "Write Python code to check if a number is even AND define what is an even number",
        "Translate cat to Arabic AND translate dog to Arabic",
        "Calculate 7 multiplied by 6 AND calculate 100 divided by 4",
        "Write Python code to calculate sum of a list AND explain what is a list",
        "Translate water to Arabic AND calculate 5 multiplied by 5",
        "Calculate the square of 5 AND calculate 13 plus 17",
        "Write Python code to find maximum of two numbers AND define what is maximum",
        "Translate sun to Arabic AND translate moon to Arabic",
        "Explain what is gravity AND calculate 100 minus 25",
        "Translate hot to Arabic AND translate cold to Arabic",
        "Write Python code to count vowels in a string AND explain what is a vowel",
        "Translate yes to Arabic AND translate no to Arabic",
        "Write Python code to check if a number is odd AND define what is an odd number"
    ],
    
    # ================================================================
    # CATEGORY 3: FOUR INDEPENDENT TASKS (25 prompts)
    # ================================================================
    "four_tasks": [
        "Define artificial intelligence AND explain machine learning AND calculate 10 plus 5 AND translate computer to Arabic",
        "Write Python code to print hello AND define what is Python AND calculate 20 minus 8 AND translate hello to Arabic",
        "Calculate 5 plus 5 AND write Python code to print result AND define addition AND translate number to Arabic",
        "Explain cloud computing AND describe the internet AND calculate 6 multiplied by 7 AND translate internet to Arabic",
        "Write Python code to greet user AND translate welcome to Arabic AND calculate 10 plus 10 AND explain what is greeting",
        
        "Define database AND explain encryption AND calculate 100 divided by 4 AND translate security to Arabic",
        "Calculate square of 4 AND calculate square of 6 AND define what is square AND translate mathematics to Arabic",
        "Write Python code to reverse string AND explain what is string AND calculate 15 plus 15 AND translate text to Arabic",
        "Explain programming AND define variable AND calculate 50 minus 20 AND translate code to Arabic",
        "Define computer AND calculate 20 minus 5 AND write Python code to print message AND translate machine to Arabic",
        
        "Calculate 7 plus 13 AND calculate 25 minus 10 AND define addition AND translate calculate to Arabic",
        "Write Python code to check even number AND define even number AND calculate 9 multiplied by 3 AND translate even to Arabic",
        "Explain variables AND define data types AND calculate 5 multiplied by 5 AND translate data to Arabic",
        "Translate welcome to Arabic AND explain what is welcome AND calculate 3 multiplied by 3 AND define greeting",
        "Calculate 12 plus 18 AND define sum AND write Python code to add numbers AND translate add to Arabic",
        
        "Write Python code to create list AND explain what is list AND calculate 36 divided by 6 AND translate list to Arabic",
        "Define computer AND define CPU AND calculate 40 minus 15 AND translate processor to Arabic",
        "Calculate 100 divided by 10 AND define division AND translate divide to Arabic AND explain what is quotient",
        "Write Python code to find maximum AND explain what is maximum AND calculate 8 multiplied by 4 AND translate maximum to Arabic",
        "Explain hardware AND describe software AND calculate 64 divided by 8 AND translate software to Arabic",
        
        "Calculate 2 plus 2 AND calculate 3 plus 3 AND translate number to Arabic AND define what is number",
        "Write Python code to check odd number AND define odd number AND calculate 80 divided by 8 AND translate odd to Arabic",
        "Define AI AND define ML AND calculate square of 8 AND translate learning to Arabic",
        "Translate cat to Arabic AND translate dog to Arabic AND define what is animal AND explain what is pet",
        "Write Python code to calculate average AND explain what is average AND calculate square of 10 AND translate average to Arabic"
    ],
    
    # ================================================================
    # CATEGORY 4: FIVE INDEPENDENT TASKS (25 prompts)
    # ================================================================
    "five_tasks": [
        "Write Python code to add numbers AND define addition AND calculate 5 plus 5 AND translate add to Arabic AND explain what is sum",
        "Calculate 1 plus 1 AND translate one to Arabic AND define what is number AND write Python code to print number AND explain integer",
        "Define AI AND calculate 10 minus 2 AND write Python code to print AI AND translate intelligence to Arabic AND explain artificial",
        "Write Python code to divide numbers AND explain division AND calculate 20 divided by 4 AND define quotient AND translate divide to Arabic",
        "Translate hello to Arabic AND define greeting AND calculate 2 plus 2 AND write Python code to print hello AND explain salutation",
        
        "Calculate 10 minus 5 AND write Python code to subtract AND translate subtract to Arabic AND define subtraction AND explain difference",
        "Define multiply AND translate multiply to Arabic AND calculate 4 multiplied by 5 AND write Python code to multiply AND explain product",
        "Write Python code to print message AND define print function AND translate output to Arabic AND calculate 3 plus 3 AND explain function",
        "Calculate 2 multiplied by 3 AND define product AND translate multiply to Arabic AND write Python code for multiplication AND explain arithmetic",
        "Translate goodbye to Arabic AND calculate 20 minus 4 AND define farewell AND write Python code to print goodbye AND explain exit",
        
        "Define list AND write Python code to create list AND translate array to Arabic AND calculate 4 plus 4 AND explain what is array",
        "Calculate 3 multiplied by 4 AND write Python code for addition AND define sum AND translate calculate to Arabic AND explain operation",
        "Write Python code for loop AND translate loop to Arabic AND define what is loop AND calculate 30 minus 6 AND explain control flow",
        "Translate yes to Arabic AND calculate square of 2 AND define affirmative AND write Python code to check condition AND explain boolean",
        "Calculate 10 divided by 2 AND define division AND write Python code to divide AND translate quotient to Arabic AND explain remainder",
        
        "Define ML AND translate learning to Arabic AND calculate 5 plus 5 AND write Python code for ML AND explain what is model",
        "Write Python code to get input AND calculate 40 minus 8 AND define input AND translate data to Arabic AND explain user interaction",
        "Translate no to Arabic AND define negative AND calculate 4 multiplied by 5 AND write Python code for negation AND explain boolean",
        "Calculate 20 divided by 4 AND write Python code to check even AND translate even to Arabic AND define parity AND explain modulo",
        "Define variable AND calculate square of 3 AND translate variable to Arabic AND write Python code to create variable AND explain assignment",
        
        "Write Python code for condition AND translate condition to Arabic AND calculate 5 multiplied by 6 AND define conditional AND explain if statement",
        "Translate please to Arabic AND calculate 30 divided by 5 AND define politeness AND write Python code to print please AND explain courtesy",
        "Calculate 50 minus 10 AND define subtraction AND write Python code to subtract AND translate difference to Arabic AND explain operation",
        "Define string AND calculate square of 4 AND write Python code to create string AND translate text to Arabic AND explain concatenation",
        "Translate thank you to Arabic AND calculate 6 multiplied by 7 AND write Python code to print thanks AND define gratitude AND explain manners"
    ]
}


    prompts2 = {
    # ================================================================
    # CATEGORY 1: SINGLE TASK (25 prompts) - MIXED ORDER
    # ================================================================
    "single_task": [
        # Mix all types throughout
        #"First explain what is a prime number Then using that definition write a code showing how to detect it",
        "Generate a Python code to loop thhrough a list and print its values",
        "Define what is artificial intelligence",
        "Calculate 15 plus 27",
        "Explain what is machine learning",
        "Translate hello to Arabic",
        "Write Python code to add two numbers",
        "Describe what is a neural network",
        "Calculate 100 minus 45",
        "Write Python code to find the maximum of three numbers",
        "Define what is an algorithm",
        "Calculate 12 multiplied by 8",
        "Write Python code to reverse a string",
        "Explain what is cloud computing",
        "Calculate the square of 9",
        "Translate thank you to Arabic",
        "Write Python code to check if a number is even",
        "Describe what is the internet",
        "Calculate 50 divided by 5",
        "Write Python code to calculate the sum of a list",
        "Define what is a database",
        "Write Python code to convert Celsius to Fahrenheit",
        "Explain what is encryption",
        "Write Python code to count vowels in a string",
        "Write Python code to find the length of a list",
        "Write Python code to create a simple calculator"
    ],
    
    # ================================================================
    # CATEGORY 2: TWO INDEPENDENT TASKS (25 prompts) - MIXED ORDER
    # ================================================================
    "two_tasks": [
        # Avoid two code tasks in same prompt, mix types
        "Define what is artificial intelligence and explain what is machine learning",
        "Calculate 15 plus 27 and calculate 100 minus 45",
        "Write Python code to print Hello World and define what is programming",
        "Translate good morning to Arabic and explain what is greeting",
        "Describe what is a neural network and define what is an algorithm",
        "Calculate 12 multiplied by 8 and calculate the square of 9",
        "Write Python code to add two numbers and explain what is addition",
        "Explain what is cloud computing and describe what is the internet",
        "Calculate 10 plus 20 and translate hello to Arabic",
        "Write Python code to reverse a string and describe what is a string",
        "Define what is a database and explain what is encryption",
        "Calculate 50 divided by 5 and calculate 20 plus 30",
        "Write Python code to check if a number is even and define what is an even number",
        "Describe what is a computer and explain what is a program",
        "Calculate 7 multiplied by 6 and calculate 100 divided by 4",
        "Write Python code to calculate sum of a list and explain what is a list",
        "Define what is water and calculate 5 multiplied by 5",
        "Calculate the square of 5 and calculate 13 plus 17",
        "Write Python code to find maximum of two numbers and define what is mathematics",
        "Translate good morning to Arabic and write Python code to print your name",
        "Explain what is gravity and calculate 100 minus 25",
        "Write Python code to convert Celsius to Fahrenheit and explain what is temperature",
        "Write Python code to count vowels in a string and explain what is a vowel",
        "Write Python code to find length of a list and explain what is length",
        "Write Python code to check if a number is odd and define what is an odd number"
    ],
    
    # ================================================================
    # CATEGORY 3: FOUR INDEPENDENT TASKS (25 prompts) - MIXED ORDER
    # ================================================================
    "four_tasks": [
        # Mix all 4 task types, avoid clustering same type
        "Define artificial intelligence and explain machine learning and calculate 10 plus 5 and translate AI to Arabic",
        "Write Python code to print hello and define what is Python and calculate 20 minus 8 and translate hello to Arabic",
        "Calculate 5 plus 5 and write Python code to print result and define addition and translate sum to Arabic",
        "Explain cloud computing and describe the internet and calculate 6 multiplied by 7 and translate internet to Arabic",
        "Write Python code to greet user and translate hello to Arabic and calculate 10 plus 10 and explain greeting",
        
        "Define database and explain encryption and calculate 100 divided by 4 and translate security to Arabic",
        "Calculate square of 4 and calculate square of 6 and define square and translate square to Arabic",
        "Write Python code to reverse string and explain what is string and calculate 15 plus 15 and translate reverse to Arabic",
        "Explain programming and define variable and calculate 50 minus 20 and translate variable to Arabic",
        "Define computer and calculate 20 minus 5 and write Python code to print computer and translate computer to Arabic",
        
        "Calculate 7 plus 13 and calculate 25 minus 10 and define addition and translate calculate to Arabic",
        "Write Python code to check even number and define even number and calculate 9 multiplied by 3 and translate even to Arabic",
        "Explain variables and define data types and calculate 5 multiplied by 5 and translate data to Arabic",
        "Translate welcome to Arabic and explain welcome and calculate 3 multiplied by 3 and define greeting",
        "Calculate 12 plus 18 and define sum and write Python code to add numbers and translate add to Arabic",
        
        "Write Python code to create list and explain what is list and calculate 36 divided by 6 and translate list to Arabic",
        "Define computer and define CPU and calculate 40 minus 15 and translate processor to Arabic",
        "Calculate 100 divided by 10 and define division and translate divide to Arabic and explain quotient",
        "Write Python code to find maximum and explain maximum and calculate 8 multiplied by 4 and translate maximum to Arabic",
        "Explain hardware and describe software and calculate 64 divided by 8 and translate software to Arabic",
        
        "Calculate 2 plus 2 and calculate 3 plus 3 and translate number to Arabic and define number",
        "Write Python code to check odd number and define odd number and calculate 80 divided by 8 and translate odd to Arabic",
        "Define AI and define ML and calculate square of 8 and translate learning to Arabic",
        "Translate cat to Arabic and translate dog to Arabic and define animal and explain pet",
        "Write Python code to calculate average and explain average and calculate square of 10 and translate average to Arabic"
    ],
    
    # ================================================================
    # CATEGORY 4: FIVE INDEPENDENT TASKS (25 prompts) - MIXED ORDER
    # ================================================================
    "five_tasks": [
        # Maximum mixing, no two same types adjacent
        "Write Python code to add and define addition and calculate 5 plus 5 and translate add to Arabic and explain sum",
        "Calculate 1 plus 1 and translate one to Arabic and define number and write Python code to print number and explain integer",
        "Define AI and calculate 10 minus 2 and write Python code to print AI and translate intelligence to Arabic and explain artificial",
        "Write Python code to divide and explain division and calculate 20 divided by 4 and define quotient and translate divide to Arabic",
        "Translate hello to Arabic and define greeting and calculate 2 plus 2 and write Python code to print hello and explain salutation",
        
        "Calculate 10 minus 5 and write Python code to subtract and translate subtract to Arabic and define subtraction and explain difference",
        "Define multiply and translate multiply to Arabic and calculate 4 multiplied by 5 and write Python code to multiply and explain product",
        "Write Python code to print and define print and translate output to Arabic and calculate 3 plus 3 and explain function",
        "Calculate 2 multiplied by 3 and define product and translate multiply to Arabic and write Python code for multiplication and explain arithmetic",
        "Translate goodbye to Arabic and calculate 20 minus 4 and define farewell and write Python code to print goodbye and explain exit",
        
        "Define list and write Python code to create list and translate array to Arabic and calculate 4 plus 4 and explain array",
        "Calculate 3 multiplied by 4 and write Python code for addition and define sum and translate calculate to Arabic and explain operation",
        "Write Python code for loop and translate loop to Arabic and define loop and calculate 30 minus 6 and explain control flow",
        "Translate yes to Arabic and calculate square of 2 and define affirmative and write Python code to check condition and explain boolean",
        "Calculate 10 divided by 2 and define division and write Python code to divide and translate quotient to Arabic and explain remainder",
        
        "Define ML and translate learning to Arabic and calculate 5 plus 5 and write Python code for ML and explain model",
        "Write Python code to input and calculate 40 minus 8 and define input and translate data to Arabic and explain user interaction",
        "Translate no to Arabic and define negative and calculate 4 multiplied by 5 and write Python code for negation and explain boolean",
        "Calculate 20 divided by 4 and write Python code to check even and translate even to Arabic and define parity and explain modulo",
        "Define variable and calculate square of 3 and translate variable to Arabic and write Python code to create variable and explain assignment",
        
        "Write Python code for condition and translate condition to Arabic and calculate 5 multiplied by 6 and define conditional and explain if statement",
        "Translate please to Arabic and calculate 30 divided by 5 and define politeness and write Python code to print please and explain courtesy",
        "Calculate 50 minus 10 and define subtraction and write Python code to subtract and translate difference to Arabic and explain operation",
        "Define string and calculate square of 4 and write Python code to create string and translate text to Arabic and explain concatenation",
        "Translate thank you to Arabic and calculate 6 multiplied by 7 and write Python code to print thanks and define gratitude and explain manners"
    ]
}

    return prompts