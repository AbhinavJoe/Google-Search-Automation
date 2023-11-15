# Google Search Automation

![Google Search Automation Logo](assets/logo.png)

A simple Python application using Tkinter to automate Google searches with predefined filters.

**Disclaimer: This project is an independent and unofficial tool not affiliated with or endorsed by Google. The use of the Google name and logo is solely for descriptive purposes and to represent the functionality of the application.**

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This application provides a user-friendly interface for performing Google searches with predefined filters. It uses Tkinter for the GUI, allowing users to input their search query and trigger a search with specified filters.

## Features

- **Custom Filters:** Predefined filters for popular websites (e.g., Reddit, Stack Overflow, Medium, GeeksforGeeks, Stack Exchange, Quora). Helpful for programmers that need the searches from popular discussion and question-and-answer platforms. The custom filters can be changed and/or removed based on user needs.
- **Automatic Chrome Detection:** The application automatically detects the Chrome browser's executable path on the user's system.
- **Responsive GUI:** A simple and responsive graphical user interface for easy interaction.

## Requirements

- Python 3
- Tkinter (`ttkbootstrap` for styling)
- Web browser (Chrome recommended)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/AbhinavJoe/Google-Search-Automation.git

   ```

2. Install the required Python packages:

   ```bash
   pip install ttkbootstrap

   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. Launch the application using the provided main.py script.
2. Enter your search query in the input field.
3. Click the "Search" button.
4. The application will open a new Chrome window with the Google search results.

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
