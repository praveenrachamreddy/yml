import openai
import os

# Set up OpenAI API credentials
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the Langchain agent
# agent = "gpt-3.5-turbo"

# Function to generate code using ChatGPT
def generate_code(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,
        n=1,
        stop=None
    )

    return response.choices[0].text.strip()
    




# Function to create a simple Java project
def create_java_project():
    user_input = input("Enter the name of the Java project: ")
    prompt = f"Create a simple Java {user_input} project."

    # Generate code using ChatGPT
    generated_code = generate_code(prompt)

    # Process generated code
    file_name = f"{user_input.capitalize()}.java"
    file_content = generated_code.strip()
    file_structure = f"- src/\n  - {file_name}"

    # Create file tree and write code
    create_file_tree(file_structure)
    write_code_to_file(file_name, file_content)

    # Provide feedback to the user
    feedback = f"Java {user_input.capitalize()} project created successfully!\nThe project contains a single file named \"{file_name}\" located in the \"src\" directory. The file contains the following code:\n\n{file_content}"
    print(feedback)

# Function to create the file tree
def create_file_tree(file_structure):
    # Remove leading and trailing whitespaces
    file_structure = file_structure.strip()

    # Split file structure by lines
    lines = file_structure.split('\n')

    # Create directories
    for line in lines:
        # Count leading spaces to determine the level of indentation
        indentation = len(line) - len(line.lstrip())

        # Remove indentation and leading/trailing whitespaces
        entry = line.strip()

        if entry.endswith('/'):
            # Directory entry
            directory_name = entry[:-1]  # Remove trailing '/'
            directory_path = os.path.join(*(['.'] + [os.path.normpath(d) for d in directory_name.split('/')]))
            os.makedirs(directory_path, exist_ok=True)
        else:
            # File entry
            file_path = os.path.join(*(['.'] + [os.path.normpath(d) for d in entry.split('/')]))
            with open(file_path, 'w') as file:
                file.write('')  # Create an empty file

    print("File tree created successfully!")


# Function to write code to a file
def write_code_to_file(file_name, code):
    try:
        with open(file_name, 'w') as file:
            file.write(code)
        print(f"Code written to file: {file_name}")
    except IOError:
        print(f"Error writing code to file: {file_name}")



# Main program loop
while True:
    user_input = input("Enter your request (or 'exit' to quit): ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    # Handle user requests
    if any(keyword in user_input.lower() for keyword in ["java project", "java code", "xxx code in java"]):
        create_java_project()
    else:
        print(f"Sorry, I can only handle requests related to creating a {user_input.capitalize()} project.")
