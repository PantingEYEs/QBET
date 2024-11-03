"""
File name:
  markdown_updater.py

Function:
  Updates the QB.md file with OCR output for each selected area (questions, answers).

Dependencies:
  os
  markdown (maybe)

"""

import os

def update_markdown_file(image_number, question_text, answer_text, is_correct=False):
    """
    Update the QB.md file with the given question and answer.

    Args:
        image_number (int): The number of the image being processed.
        question_text (str): The text of the question.
        answer_text (str): The text of the answer.
        is_correct (bool): Flag indicating if the answer is marked as correct.

    Returns:
        None
    """
    markdown_file_path = "output/QB.md"
    
    # Ensure the markdown file exists
    if not os.path.exists(markdown_file_path):
        # Create a new markdown file if it doesn't exist
        with open(markdown_file_path, 'w') as md_file:
            md_file.write("# Question Bank\n\n")

    # Prepare the new content to be added
    if is_correct:
        answer_entry = f"* ==\"{answer_text}\"== \n"
    else:
        answer_entry = f"* \"{answer_text}\" \n"

    # Create the entry for the question and answer
    entry = f"## {question_text}\n\n{answer_entry}\n"

    # Append the entry to the markdown file
    with open(markdown_file_path, 'a') as md_file:
        md_file.write(entry)

    print(f"Updated {markdown_file_path} with question and answer.")

# Example usage
if __name__ == "__main__":
    # Sample inputs for testing
    update_markdown_file(1, "What is the capital of France?", "Paris")
    update_markdown_file(1, "What is the capital of France?", "Berlin", is_correct=True)
