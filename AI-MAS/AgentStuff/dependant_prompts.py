
def DEPENDANT_PROMPTS():
    """
    Test Prompts for Multi-Agent System Benchmarking
    100 prompts organized by dependency type:
    - "then" = sequential dependency (must wait for previous result)
    - "AND" = parallel independent tasks
    """
    prompts = {
    # ================================================================
    # CATEGORY 1: TWO DEPENDENT TASKS - Sequential (25 prompts)
    # Uses "then" to indicate dependency
    # ================================================================
    "two_dependent": [
        # Code then Text
        "Write Python code to add two numbers then explain what the code does",
        "Write Python code to reverse a string then describe how it works",
        "Write Python code to find maximum of a list then explain the algorithm",
        "Write Python code to check if number is even then explain the logic",
        "Write Python code to calculate factorial then describe the approach",
        
        # Math then Text
        "Calculate 15 multiplied by 8 then explain how multiplication works",
        "Calculate the square of 12 then define what squaring means",
        "Calculate 100 divided by 4 then explain the division process",
        "Calculate 25 plus 75 then describe what addition is",
        "Calculate 50 minus 18 then explain subtraction",
        
        # Text then Translate
        "Define what is artificial intelligence then translate the definition to Arabic",
        "Explain what is machine learning then translate the explanation to Arabic",
        "Describe what is a neural network then translate it to Arabic",
        "Define what is an algorithm then translate the definition to Arabic",
        "Explain what is cloud computing then translate the explanation to Arabic",
        
        # Math then Translate
        "Calculate 9 multiplied by 9 then translate the result to Arabic",
        "Calculate 144 divided by 12 then translate the answer to Arabic",
        "Calculate 33 plus 67 then translate the sum to Arabic",
        "Calculate the square of 7 then translate the result to Arabic",
        "Calculate 200 minus 85 then translate the difference to Arabic",
        
        # Code then Translate
        "Write Python code to print hello world then translate the output to Arabic",
        "Write Python code to add 5 and 10 then translate the result to Arabic",
        "Write Python code to create a greeting message then translate it to Arabic",
        "Write Python code to calculate sum of 1 to 5 then translate the result to Arabic",
        "Write Python code to multiply 6 by 7 then translate the product to Arabic"
    ],
    
    # ================================================================
    # CATEGORY 2: THREE DEPENDENT TASKS - Sequential Chain (25 prompts)
    # Uses "then" to indicate dependency chain
    # ================================================================
    "three_dependent": [
        # Math then Code then Text
        "Calculate 8 plus 12 then write Python code to verify that calculation then explain the code",
        "Calculate 5 multiplied by 9 then write Python code to compute it then describe the algorithm",
        "Calculate 100 divided by 5 then write Python code for division then explain how it works",
        "Calculate the square of 6 then write Python code to compute squares then explain the logic",
        "Calculate 75 minus 25 then write Python code for subtraction then describe the approach",
        
        # Text then Code then Translate
        "Define what is a loop then write Python code demonstrating a loop then translate the output to Arabic",
        "Explain what is a function then write Python code with a function then translate the result to Arabic",
        "Describe what is a variable then write Python code using variables then translate it to Arabic",
        "Define what is a list then write Python code to create a list then translate the output to Arabic",
        "Explain what is a condition then write Python code with if statement then translate the output to Arabic",
        
        # Code then Math then Translate
        "Write Python code to generate number 15 then calculate its square then translate the result to Arabic",
        "Write Python code to add 10 and 20 then multiply the result by 2 then translate to Arabic",
        "Write Python code to compute 7 times 3 then add 10 to it then translate the final answer to Arabic",
        "Write Python code to subtract 5 from 25 then divide by 4 then translate the result to Arabic",
        "Write Python code to calculate 8 plus 8 then find its double then translate to Arabic",
        
        # Math then Text then Translate
        "Calculate 12 multiplied by 12 then explain what multiplication is then translate everything to Arabic",
        "Calculate 256 divided by 16 then describe the division process then translate to Arabic",
        "Calculate 45 plus 55 then define what addition means then translate the explanation to Arabic",
        "Calculate the square of 9 then explain what a square is then translate to Arabic",
        "Calculate 90 minus 35 then describe subtraction then translate the description to Arabic",
        
        # Text then Math then Translate
        "Define what is percentage then calculate 20 percent of 150 then translate the result to Arabic",
        "Explain what is average then calculate the average of 10 and 30 then translate to Arabic",
        "Describe what is doubling then calculate double of 45 then translate the answer to Arabic",
        "Define what is halving then calculate half of 84 then translate the result to Arabic",
        "Explain what is sum then calculate sum of 33 and 44 then translate to Arabic"
    ],
    
    # ================================================================
    # CATEGORY 3: MIXED - Parallel AND Sequential (25 prompts)
    # Pattern: (A AND B) then C - Two parallel first, then one dependent
    # ================================================================
    "mixed_parallel_then_sequential": [
        # (Math AND Math) then Translate
        "Calculate 10 plus 5 AND calculate 20 minus 8 then translate both results to Arabic",
        "Calculate square of 4 AND calculate square of 5 then explain what squaring means",
        "Calculate 7 times 8 AND calculate 9 times 6 then compare which product is larger",
        "Calculate 100 divided by 4 AND calculate 100 divided by 5 then explain the difference",
        "Calculate 15 plus 15 AND calculate 30 minus 10 then translate the results to Arabic",
        
        # (Text AND Text) then Code
        "Define AI AND define ML then write Python code demonstrating a simple concept from both",
        "Explain encryption AND explain decryption then describe how they work together",
        "Define what is input AND define what is output then write Python code showing both",
        "Explain hardware AND explain software then describe how they interact",
        "Define what is a loop AND define what is a function then write Python code using both",
        
        # (Code AND Code) then Text
        "Write Python code for addition AND write Python code for subtraction then explain both approaches",
        "Write Python code for multiplication AND write Python code for division then explain arithmetic operations",
        "Write Python code to find maximum AND write Python code to find minimum then compare the algorithms",
        "Write Python code for a loop AND write Python code for a condition then explain control flow",
        "Write Python code to create a list AND write Python code to create a string then explain data types",
        
        # (Translate AND Translate) then Text
        "Translate hello to Arabic AND translate goodbye to Arabic then explain greetings in Arabic",
        "Translate yes to Arabic AND translate no to Arabic then explain affirmative and negative",
        "Translate cat to Arabic AND translate dog to Arabic then explain animal names",
        "Translate hot to Arabic AND translate cold to Arabic then explain opposites",
        "Translate sun to Arabic AND translate moon to Arabic then explain celestial terms",
        
        # (Mixed AND Mixed) then Result
        "Define programming AND calculate 10 plus 10 then write Python code using that number",
        "Calculate 5 times 5 AND explain what multiplication is then translate the result to Arabic",
        "Write Python code to print hello AND translate hello to Arabic then explain the greeting",
        "Define what is a variable AND calculate 7 plus 3 then write Python code assigning that value",
        "Explain what is addition AND calculate 25 plus 25 then translate the sum to Arabic"
    ],
    
    # ================================================================
    # CATEGORY 4: MIXED - Sequential then Parallel (25 prompts)
    # Pattern: A then (B AND C) - One first, then two parallel dependent
    # ================================================================
    "mixed_sequential_then_parallel": [
        # Math then (Text AND Translate)
        "Calculate 15 plus 25 then explain what addition is AND translate the result to Arabic",
        "Calculate the square of 8 then define squaring AND translate the result to Arabic",
        "Calculate 50 times 2 then explain multiplication AND translate the product to Arabic",
        "Calculate 144 divided by 12 then define division AND translate the answer to Arabic",
        "Calculate 90 minus 30 then describe subtraction AND translate the difference to Arabic",
        
        # Code then (Text AND Translate)
        "Write Python code to reverse a string then explain the algorithm AND translate the code comments to Arabic",
        "Write Python code to find maximum then describe the algorithm AND translate the output to Arabic",
        "Write Python code for a loop then explain iteration AND translate loop concept to Arabic",
        "Write Python code to add numbers then explain the function AND translate the result to Arabic",
        "Write Python code to check even number then describe the logic AND translate even to Arabic",
        
        # Text then (Code AND Translate)
        "Define artificial intelligence then write Python code for a simple AI task AND translate the definition to Arabic",
        "Explain what is a database then write Python code to store data AND translate database to Arabic",
        "Describe what is sorting then write Python code to sort a list AND translate sorting to Arabic",
        "Define what is a function then write Python code with a function AND translate function to Arabic",
        "Explain what is a variable then write Python code using variables AND translate variable to Arabic",
        
        # Text then (Math AND Translate)
        "Define what is percentage then calculate 10 percent of 200 AND translate percentage to Arabic",
        "Explain what is doubling then calculate double of 35 AND translate double to Arabic",
        "Describe what is average then calculate average of 20 and 40 AND translate average to Arabic",
        "Define what is a square then calculate square of 11 AND translate square to Arabic",
        "Explain what is sum then calculate 55 plus 45 AND translate sum to Arabic",
        
        # Translate then (Text AND Math)
        "Translate number to Arabic then define what is a number AND calculate 100 plus 100",
        "Translate computer to Arabic then explain what is a computer AND calculate 64 divided by 8",
        "Translate mathematics to Arabic then define mathematics AND calculate square of 7",
        "Translate code to Arabic then explain what is coding AND calculate 12 times 12",
        "Translate science to Arabic then define science AND calculate 1000 divided by 10"
    ]
    }
    
    return prompts