import os
import random
from PIL import Image
import streamlit as st
from typing import Dict, List, Tuple

# ImageDatasetManager Class
class ImageDatasetManager:
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.classes = ["glioma", "meningioma", "no_tumor", "pituitary"]
        self.image_data = self.load_data()

    def load_data(self) -> Dict[str, List[str]]:
        """Load image paths for each class."""
        image_data = {class_name: [] for class_name in self.classes}
        for class_name in self.classes:
            class_path = os.path.join(self.dataset_path, class_name)
            if os.path.exists(class_path):
                image_data[class_name] = [os.path.join(class_path, img) for img in os.listdir(class_path)]
        return image_data

    def get_random_image(self) -> Tuple[str, str]:
        """Get a random image and its class."""
        class_name = random.choice(self.classes)
        image_path = random.choice(self.image_data[class_name])
        return class_name, image_path

# BrainMRIGame Class
class BrainMRIGame:
    def __init__(self, dataset_manager: ImageDatasetManager):
        self.dataset_manager = dataset_manager
        if "score" not in st.session_state:
            st.session_state.score = 0
        if "total_attempts" not in st.session_state:
            st.session_state.total_attempts = 0
        if "max_tests" not in st.session_state:
            st.session_state.max_tests = 0
        if "current_class" not in st.session_state:
            st.session_state.current_class, st.session_state.current_image_path = self.dataset_manager.get_random_image()

    def start_test(self):
        """Start the test with the specified number of images."""
        st.session_state.max_tests = st.session_state.num_tests
        st.session_state.score = 0
        st.session_state.total_attempts = 0
        st.session_state.current_class, st.session_state.current_image_path = self.dataset_manager.get_random_image()

    def display_image(self):
        """Display the current image in the app."""
        img = Image.open(st.session_state.current_image_path)
        st.image(img, caption="Brain MRI Image", use_column_width=True)

    def check_guess(self, guessed_class: str):
        """Check if the user's guess is correct."""
        if st.session_state.total_attempts >= st.session_state.max_tests:
            return  # Stop if the user has completed the test

        st.session_state.total_attempts += 1
        if guessed_class == st.session_state.current_class:
            st.session_state.score += 1
            st.success("Correct! Your guess is right.")
        else:
            st.error(f"Wrong! The correct class was {st.session_state.current_class}.")

        # Check if the test is complete
        if st.session_state.total_attempts >= st.session_state.max_tests:
            self.end_test()
        else:
            # Load a new random image
            st.session_state.current_class, st.session_state.current_image_path = self.dataset_manager.get_random_image()

    def end_test(self):
        """End the test and provide feedback."""
        percentage_score = (st.session_state.score / st.session_state.max_tests) * 100
        if percentage_score == 100:
            st.balloons()
            st.success("Amazing! You scored 100%! 🎉")
        elif percentage_score >= 70:
            st.success(f"Congratulations! You scored {percentage_score:.0f}%! 🎉")
        else:
            st.warning(f"Good effort! You scored {percentage_score:.0f}%. Keep practicing!")

# Main Function
def main():
    st.title("Brain MRI Guessing Game 🧠")
    st.write("Test your knowledge of brain tumor identification!")

    # Load dataset
    dataset_path = "image_data"  # Replace with your dataset path
    dataset_manager = ImageDatasetManager(dataset_path)

    # Initialize the game
    game = BrainMRIGame(dataset_manager)

    # Input for number of tests
    if "num_tests" not in st.session_state:
        st.session_state.num_tests = 5
    st.session_state.num_tests = st.number_input("Number of tests:", min_value=1, max_value=20, value=st.session_state.num_tests)

    # Start test button
    if st.button("Start Test"):
        game.start_test()

    # Display the game if the test has started
    if st.session_state.max_tests > 0:
        st.write(f"Score: {st.session_state.score} | Attempts: {st.session_state.total_attempts}/{st.session_state.max_tests}")
        game.display_image()

        # Guess buttons
        for class_name in dataset_manager.classes:
            if st.button(class_name):
                game.check_guess(class_name)

# Run the app
if __name__ == "__main__":
    main()
