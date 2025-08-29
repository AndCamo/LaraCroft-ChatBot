# 🏛️ Lara Dialogue System


## 📋 Table of Contents

- [🔍 Overview](#-overview)
- [✨ Features](#-features)
- [🛠️ Technical Stack](#️-technical-stack)
- [🏗️ System Architecture](#️-system-architecture)
  - [🎭 Dialogue Manager](#-dialogue-manager)
  - [🧠 Natural Language Understanding](#-natural-language-understanding)
  - [💬 Natural Language Generation](#-natural-language-generation)
- [❓ Question Types](#-question-types)
- [⚙️ Installation](#️-installation)
- [🚀 Usage](#-usage)
- [📁 Project Structure](#-project-structure)
- [📊 Evaluation](#-evaluation)
- [📚 Documentation](#-documentation)


## 🔍 Overview
A Natural Language Processing project implementing a dialogue system that embodies the character of Lara Croft, designed to conduct job interviews for potential assistants through interactive conversations. The Lara Dialogue System is a Dialogue System that simulates Lara Croft conducting job interviews to evaluate potential assistants. The system maintains character consistency while handling simple dialogue patterns, question-answering scenarios, and contextual responses.

### 🎯 Key Objectives

- **Character Embodiment**: Faithfully represent Lara Croft's personality and communication style
- **Intelligent Evaluation**: Assess user responses across multiple question types and difficulty levels
- **Context Awareness**: Maintain conversation flow and adapt responses based on user performance
- **Robust NLU**: Handle various response formats, ambiguities, and incomplete answers

## ✨ Features

- **🎯 Multi-type Question Handling**: Single-answer, multiple-choice, and true/false questions
- **🤖 Dynamic Response Generation**: Context-aware replies that adapt to user performance
- **🧠 Memory Management**: Tracks conversation history and user performance
- **🔧 Ambiguity Resolution**: Handles unclear or incomplete user responses
- **🎭 Character-Consistent Dialogue**: Maintains Lara Croft's personality throughout interactions
- **📈 Scoring System**: Evaluates user responses with weighted scoring

## 🛠️ Technical Stack

- **Language**: Python 3.x 🐍
- **NLP Framework**: spaCy with `en_core_web_trf` transformer model 🤖
- **Core Technologies**:
  - Part-of-Speech (PoS) Recognition 🏷️
  - Named Entity Recognition (NER) 👤
  - Dependency Parsing 🌳
  - Syntactic Analysis 📝
- **Interface**: Command Line Interface (CLI) 💻
- **Data Format**: JSON-based question dataset 📄

## 🏗️ System Architecture

### 🎭 Dialogue Manager

The system maintains comprehensive user and conversation state through:

- **👤 User Frame**: Stores user information (name, score, adjectives, question count)
- **🧠 Memory System**: Tracks asked questions, user responses, and results
- **🔄 Slot Filling**: Updates conversation state dynamically

### 🧠 Natural Language Understanding

Sophisticated text processing capabilities including:

- **❓ WH-Question Processing**: Extracts answers based on question type (what, who, when, where)
- **✅ Binary Response Handling**: Processes true/false questions with keyword matching
- **📝 Multiple Answer Management**: Handles list-based responses with partial completion support
- **🌳 Dependency Analysis**: Uses syntactic parsing for accurate information extraction

### 💬 Natural Language Generation

Context-aware response generation featuring:

- **📋 Template-based System**: Predefined templates reflecting Lara Croft's speaking style
- **🔄 Dynamic Contextualization**: Responses adapt to conversation state and user performance
- **🎭 Character Consistency**: Maintains personality traits throughout the interaction

## ❓ Question Types

The system handles three distinct question categories:

1. **📝 Single Answer Questions** (`single_wh_answer`)
   - Expect one specific answer (person, place, date, etc.)
   - Example: "Where did I track the Hand of Rathmore after learning it had been taken?"

2. **📋 Multiple Answer Questions** (`multiple_answer`)
   - Require lists of information
   - Example: "Name the four meteorite artifacts I collected."

3. **✅❌ True/False Questions** (`true_false`)
   - Binary verification questions
   - Example: "I was officially declared dead after my expedition in Egypt."

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/AndCamo/LaraCroft-ChatBot.git
cd lara-dialogue-system

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_trf
```

## 🚀 Usage

```bash
# Run the dialogue system
python main.py

# Follow the interactive prompts to:
# 1. Introduce yourself to Lara
# 2. Answer her questions about archaeology and adventures
# 3. Receive your final evaluation
```

### 💬 Example Interaction

```
Lara: Good evening! I'm Lara Croft. You're not here for a tour of my manor — 
      this is an interview, and I don't have time for games. Now, tell me: 
      who are you, and why do you think you can keep up with me?

User: Hi Lara, my name is Andrea. I am very brave and intelligent, 
      ideal characteristics for your future assistant.

Lara: Brave... That's what they all say, Andrea. Time to prove it. Let's start. First question, I won’t be too evil: The
light of Horus successfully defeated Set.

User: Yes it’s true

Lara: Wrong answer, Andrea. Maybe you are not as brave as you think.
```

## 📁 Project Structure

```
lara-dialogue-system/
├── main.py                 # Main application entry point
├── dialogue_manager.py     # Core dialogue management
├── question_handlers.py    # Question processing logic
├── nlg_module.py          # Natural Language Generation
├── nlu_module.py          # Natural Language Understanding
├── questions_dataset.json  # Question database (80 questions)
├── requirements.txt       # Project dependencies
├── Relazione.pdf         # Complete technical documentation (Italian)
└── README.md             # This file
```

## 📊 Evaluation

The system has been evaluated using:

- **💬 Dialogue Examples**: Multiple conversation scenarios testing different response types
- **📋 TRINDI Tick List**: Formal dialogue system evaluation framework
- **📈 Performance Metrics**: Question handling accuracy and context awareness

### ✅ Key Capabilities Demonstrated

✅ Context-sensitive interpretation  
✅ Handling over-informative responses  
✅ Managing under-informative responses  
✅ Ambiguity resolution  
✅ Appropriate follow-up questions  
✅ Inconsistency detection  

## 📚 Documentation

For complete technical details, implementation specifics, and evaluation results, please refer to the comprehensive project report: **[📖 Relazione.pdf](./Relazione.pdf)**

The report includes:
- 🏗️ Detailed system architecture
- 🔧 NLP processing algorithms
- 📊 Evaluation methodology
- 💬 Sample dialogues and analysis
- ✅ TRINDI Tick List assessment

---

Made with <3 by Andrea Camoia, 2025
