import ollama
import json
from colorama import Fore, init
init(autoreset=True)

class Generate_class:
    def __init__(self,repo_path):
        print(Fore.YELLOW + "\n make sure you have ollama and mistral running on it.\n")
        print("This model Hallucinates in Usage And Installation section if enough Information is not provided consider checking file content and modify if needed.")
        self.title = "New Project"
        self.model = "mistral"
        self.description = ""
        self.features = ""
        self.installation = ""
        self.usage = ""
        self.installation_bash = ""
        self.usage_bash = ""
        self.license = {
            1: "MIT License",
            2: "Apache License 2.0",
            3: "GNU General Public License (GPL) v3.0",
            4: "BSD 3-Clause License",
            5: "Mozilla Public License 2.0",
            6: "Creative Commons Zero v1.0 Universal (CC0)",
            7: "Eclipse Public License 2.0",
            8: "GNU Lesser General Public License (LGPL) v3.0",
            9: "GNU Affero General Public License (AGPL) v3.0",
        }
        self.image = {
            1: "MIT",
            2: "Apache",
            3: "GNU",
            4: "BSD",
            5: "Mozilla",
            6: "Creative",
            7: "Eclipse",
            8: "GNU-Lesser",
            9: "GNU-Affero",
        }
        self.contribution = ""
        self.contact = ""
        self.newsec = ""
        self.repo_path=repo_path

        ip = input("Do you want to generate content with AI? (Enter 'y' for Yes, 'n' for No): ").lower()

        if ip == 'n':
            self.collect_manual_input()
        elif ip == 'y':
            self.generate_ai_content()
        else:
            print("Invalid choice. Please enter 'y' or 'n'.")
            exit()

    def format_features(self):
        if isinstance(self.features, list):
            return "\n".join(f"- {feature}" for feature in self.features)
        return self.features

    def format_contribution(self):
        return "\n\n".join(f"{contri}" for contri in list(self.contribution.split(',')))

    def collect_contact_info(self):
        print("Enter your contact details. Press Enter to skip any field.")
        name = input("Your Name: ").strip()
        email = input("Your Email: ").strip()
        github = input("GitHub Profile (e.g., https://github.com/yourusername): ").strip()
        linkedin = input("LinkedIn Profile (e.g., https://linkedin.com/in/yourprofile): ").strip()
        website = input("Personal Website/Portfolio (if any): ").strip()
        contact_info = []
        if name:
            contact_info.append(f" Name: {name}")
        if email:
            contact_info.append(f" Email: [{email}](mailto:{email})")
        if github:
            contact_info.append(f" GitHub: [{github}]({github})")
        if linkedin:
            contact_info.append(f" LinkedIn: [{linkedin}]({linkedin})")
        if website:
            contact_info.append(f" Website: [{website}]({website})")

        self.contact = "\n\n".join(contact_info) if contact_info else "No contact information provided."

    def collect_manual_input(self):
        self.title = input("Enter title: ")
        self.description = input("Enter description: ")
        self.features = input("Enter features: ")
        self.installation = input("Enter installation guide: ")
        self.usage = input("Enter usage: ")

        print("Select a license:")
        for key, value in self.license.items():
            print(f"{key}: {value}")
        selected_number = int(input("Enter the number of the license: "))
        selected_license = self.license.get(selected_number, "No license selected")
        print(selected_license)
        self.image = self.image.get(selected_number, "No image")
        self.license = selected_license
        self.contribution = input("Enter contribution guidelines: ")
        self.collect_contact_info()

    def generate_ai_content(self):
        print("Select a license:")
        for key, value in self.license.items():
            print(f"{key}: {value}")
        selected_number = int(input("Enter the number of the license: "))
        selected_license = self.license.get(selected_number, "No license selected")
        print(selected_license)
        self.image = self.image.get(selected_number, "No image")
        self.license = selected_license

        self.contribution = input("Enter contribution guidelines: ")
        self.collect_contact_info()

        self.installation_bash = input("Enter bash commands for installation (press Enter to skip): ").strip()
        self.usage_bash = input("Enter bash commands for usage (press Enter to skip): ").strip()

        project_description = input("Describe your project briefly: ")

        # Prompt for general README content
        pre_prompt = f"""
        Forget all previous inputs. Below is the project description. Generate a structured README file **strictly** in JSON format with the following keys:

        {{
          "title": "Project Title",
          "description": "A detailed project description (at least 80 words).",
          "features": "A list of key features of the project."
        }}

        **Instructions:**
        - **DO NOT** add or assume any extra commands yourself.
        - **Respond strictly in JSON format**, without additional text or explanations.
        """

        prompt = pre_prompt + project_description
        print("Generating content with AI...")

        generated = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        generated_text = generated['message']['content']

        # Separate AI-generated requests for installation and usage
        install_prompt = f"""
        Based on the following project description, generate only the installation instructions. 
        If installation commands are provided, format them in bullet points. 
        only describe the commands which are given by user dont create any command by yourself if no commands are given just return dont know as text
        Project description: {project_description}
        **Installation commands (if available):** {self.installation_bash}
        """

        usage_prompt = f"""
        Based on the following project description, generate only the usage instructions. 
        If usage commands are provided, format them in bullet points.
        only describe the commands which are given by user dont create any command by yourself if no commands are given just return dont know as text
        Project description: {project_description}
        **Usage commands (if available):** {self.usage_bash}
        """

        # Query AI for installation and usage separately
        gen_installation = ollama.chat(model=self.model, messages=[{"role": "user", "content": install_prompt}])
        gen_usage = ollama.chat(model=self.model, messages=[{"role": "user", "content": usage_prompt}])

        try:
            parsed_json = json.loads(generated_text)  # Parse AI response as JSON
            self.title = parsed_json.get("title", "New Project")
            self.description = parsed_json.get("description", "No description provided.")
            self.features = parsed_json.get("features", "No features listed.")

            self.installation = gen_installation['message']['content']
            self.usage = gen_usage['message']['content']
        except json.JSONDecodeError:
            print("Error: AI response is not valid JSON. Please review and update manually.")
        print('content generated')
        ip = input("Would you like to ask AI anything else? (y for yes, n for no): ")
        if ip.lower() == "y":
            prompt = input("Enter your request: ")
            self.newsec = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])['message'][
                'content']

    def generate(self):
        print(self.contact)
        print('debugging')
        license_section = f"""
## License
This project is licensed under the {self.license}.

See the [LICENSE](LICENSE) file for details.
""" if self.license else ""

        image_section = f"![License](https://img.shields.io/badge/license-{self.image}-blue)" if self.license else ""

        readme_content = f"""
# {self.title} ![Status](https://img.shields.io/badge/status-active-success) {image_section}

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
{"- [License](#license)" if self.license else ""}
- [Contributing](#contributing)
- [Contact](#contact)

---
## Description
{self.description}


---
## Features
{self.format_features()}


---
## Installation
{self.installation}


---
## Usage
{self.usage}

---
{license_section}

---

## Contributing
{self.format_contribution()}    
    

----
## Contact
{self.contact}

---
{self.newsec if self.newsec else ""}
"""
        with open(f"{self.repo_path}/README.md", "w") as file:
            file.write(readme_content.strip())
        print("README.md generated successfully!")
        print("")
        print(Fore.YELLOW + "This model Hallucinates in Usage And Installation section if enough Information is not provided consider checking file content and modify if needed.")

