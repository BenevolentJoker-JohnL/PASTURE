***PLEASE NOTE, THIS FRAMEWORK IS IN ACTIVE DEVELOPMENT AND THIS IS JUST PRELIMINARY DOCUMENTATION AND FRAMEWORK DESIGN. THIS WILL BE GETTING UPDATED AS IT IS FLESHED OUT, WITH PIPELINE EXAMPLE FLOWS TO DEMONSTRATE HOW PASTURE CAN BE OPTIMALLY UTILIZED. AS SUCH, ATTEMPTING TO INSTILL IT VIA PIP COMMAND /WILL/ FAIL***

# PASTURE Framework

**P**ipeline for **A**nalytical **S**ynthesis of **T**extual **U**nification and **R**esource **E**nhancement
```
        ___         ___           ___                       ___           ___           ___     
       /  /\       /  /\         /  /\          ___        /__/\         /  /\         /  /\    
      /  /::\     /  /::\       /  /:/_        /  /\       \  \:\       /  /::\       /  /:/_   
     /  /:/\:\   /  /:/\:\     /  /:/ /\      /  /:/        \  \:\     /  /:/\:\     /  /:/ /\  
    /  /:/~/:/  /  /:/~/::\   /  /:/ /::\    /  /:/     ___  \  \:\   /  /:/~/:/    /  /:/ /:/_ 
   /__/:/ /:/  /__/:/ /:/\:\ /__/:/ /:/\:\  /  /::\    /__/\  \__\:\ /__/:/ /:/___ /__/:/ /:/ /\
   \  \:\/:/   \  \:\/:/__\/ \  \:\/:/~/:/ /__/:/\:\   \  \:\ /  /:/ \  \:\/:::::/ \  \:\/:/ /:/
    \  \::/     \  \::/       \  \::/ /:/  \__\/  \:\   \  \:\  /:/   \  \::/~~~~   \  \::/ /:/ 
     \  \:\      \  \:\        \__\/ /:/        \  \:\   \  \:\/:/     \  \:\        \  \:\/:/  
      \  \:\      \  \:\         /__/:/          \__\/    \  \::/       \  \:\        \  \::/   
       \__\/       \__\/         \__\/                     \__\/         \__\/         \__\/    
```

 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Pipeline for Analytical Synthesis Unification and Resource Enhancement
 ⠀⠀⠀⠀⠀⠀⠀⠀             A TRIVIAL MIDDLEWARE SOLUTION TO MODEL NON-UNIFORMITY
```
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠤⠖⢊⣯⣀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⣺⡥⢲⠂⠈⢻⡯
		⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠎⡸⠋⠀⢸⢀⡴⠋⠀
		⣀⡿⠀⠙⣳⠦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⣰⣖⣄⣿⣶⣆⣾⣦⣴⣶⡶⣇⣠⡀⠀⠀⠀⢠⠞⠁⡼⠁⠀⠀⢸⣼⠁⠀⠀
		⠈⣧⣬⡻⡀⠉⠱⢽⡲⢤⣀⡀⠀⠀⠀⠀⣤⢴⣾⣿⠿⠋⠉⠉⠁⠈⠀⠀⠀⠀⠉⠀⠉⠻⠧⡿⣤⠞⠁⢀⡼⠁⠀⠀⠀⣸⡏⠀⠀⠀
		⠀⠙⠁⣷⢣⠀⠀⠀⠹⢄⠀⠉⠓⡦⣄⣾⡟⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⣿⣖⣋⠀⠀⠀⠀⠀⣿⠁⠀⠀⠀
		⠀⠀⠀⠘⢎⢧⠀⠀⠀⠈⠓⠦⢄⣛⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⢿⣄⠀⠀⠀⢰⢻⠂⠀⠀⠀
		⠀⠀⠀⠀⠈⠻⣧⠀⠀⠀⠀⣤⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠿⣧⠀⠀⣯⠎⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⢯⣣⡀⠀⣠⣿⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⡄⡼⡟⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠸⡵⣄⣹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⠟⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠙⢬⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⣆⠀⠀___________________________⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⠀⠀⠀⠀⢀⣀⣀⡀⠀⠀⠀⠀⢸⠀⠀|⠀⠀                           \
		⠀⠀⠀⠀⠀⠀⠀⠀⠨⣿⢄⠀⠀⠀⠀⢀⣀⣠⣀⠀⠀⠀⢠⠖⠋⠁⠀⠀⠈⠓⢦⠀⢠⣿⣿⣿⣟⠷⡄⠀⠀⣸⡏⠀⠀|⠀⠀The Greatest things,  |
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡶⠀⠀⠀⣠⣾⡿⣿⣿⣿⣆⣠⡏⠀⠀⠀⠀⠀⠀⠀⠈⣦⠟⣽⣿⣿⣻⠀⣇⡠⠴⠿⣁⠀⠀|⠀⠀often have yet to be built⠀⠀|                           
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⢦⠀⠀⢹⡙⢯⣿⣿⣫⠋⢿⡇⠀⠀⠀⠀⠀⠀⠀⠀⢻⡦⠽⠷⠾⠓⠋⠁⠀⠀⠘⢏⠁⠀\⠀⠀⠀⠀                          |
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣳⠞⠒⠓⠚⠩⠝⠛⠂⣹⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠱⡄⠀⠀⠀⠀⠀⠀⠀⠀⠘⣆⠀⠀\⠀⠀___________________________/⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡁⠀⠀⠀⠀⠀⠀⠀⢠⠏⠀⠀⣆⣀⣀⢀⣤⣘⣆⠀⠀⠙⣆⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀/⠀/⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡿⠉⠀⠀⠀⠀⠀⠀⣠⣾⡆⠀⢀⣿⣧⣌⠉⣼⢶⡿⠀⠀⡿⢺⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀ //⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷⡀⠀⠀⠀⠀⠀⠀⠀⡏⣿⠀⠀⠉⠁⠙⣮⠏⠀⠀⠀⠀⣇⡼⠀⠀⠀⠀⠀⠀⠀⠐⣿⠀//⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠁⠀⠀⠀⠀⠀⠀⠀⠳⣘⢄⠀⠀⠀⠀⢸⡀⠀⠀⢀⣼⠟⠀⠀⠀⠀⠀⠀⠀⢀⣿⠋//⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⡄⠀⠀⠀⠀⠀⠀⠀⠈⠚⠷⣤⠤⠴⠿⠿⠒⢊⡝⠁⠀⠀⠀⠀⠀⠀⠀⠀⢛⣹⣄⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⣶⠄⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⠤⠤⠤⠔⠋⠀⠀⠀⠀⠀⠀⢀⣠⠖⠀⠈⣏⠉⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢿⡆⠀⠀⠰⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠴⠒⠉⠀⠀⠀⢀⡟⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⠀⠀⠀⠀⠉⠉⠒⠒⠒⠒⠒⠒⠒⠒⠒⠚⠉⠉⠁⠀⠀⠀⠀⠀⠀⢼⡄⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣇⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡆⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⡿⠟⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⡄⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣺⠇⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⠟⠉⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⠗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢱⠀⠀⠀⠀⠀⠀
```

## Acronym Explained

```
 _______   _______   _______   _______   _______   _______   _______ 
|       | |       | |       | |       | |       | |       | |       |
| P     | | A     | | S     | | T     | | U     | | R     | | E     |
|_______| |_______| |_______| |_______| |_______| |_______| |_______|
```

- **P**ipeline: A structured sequence of processing steps for coordinated model execution
- **A**nalytical: Focused on analyzing and processing various types of information
- **S**ynthesis: Combining outputs from multiple models into coherent results
- **T**extual: Operating primarily on text-based inputs and outputs
- **U**nification: Bringing together different models with standardized interfaces
- **R**esource: Managing computational resources effectively (memory, processing, etc.)
- **E**nhancement: Improving reliability, error handling, and output quality

## Overview

```
  _____             _                  __                                         _    
 |  _  |___ ___ ___| |_ ___ ___ ___   |  |   ___ ___ ___ _____ ___ _ _ _ ___ ___| |_  
 |   __| .'|_ -|  _|  _| . |  _| -_|  |  |__| .'|   | -_|     | . | | | | . |  _|  _| 
 |__|  |__,|___|___|_| |___|_| |___|  |_____|__,|_|_|___|_|_|_|___|_____|___|_| |_|   
                                                                                        
```

PASTURE is a middleware framework designed to orchestrate multiple AI models hosted on Ollama. It enables seamless communication between different LLMs while ensuring robust error handling, response validation, and high reliability.

**Important Note**: PASTURE is a backend orchestration framework for Ollama-hosted models. It does not determine how models generate responses or what the content should be. Users are responsible for configuring their specific model invocation patterns, prompts, and tuning parameters. PASTURE helps solve the communication and orchestration challenges but leaves the "what to ask" and model-specific configurations to you.

## Problem Space

Currently, there is no standardized way to:
- Chain multiple LLMs together reliably
- Handle the various JSON parsing errors that occur across different models
- Deal with resource constraints when loading multiple models
- Implement robust fallback mechanisms when models fail
- Cache responses to avoid redundant API calls

PASTURE addresses these challenges by providing a comprehensive orchestration layer that sits between your application and Ollama-hosted models.

## Core Features

```
░▒▓████████▓▒░▒▓████████▓▒░░▒▓██████▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓████████▓▒░░▒▓███████▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        
░▒▓██████▓▒░ ░▒▓██████▓▒░ ░▒▓████████▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓██████▓▒░  ░▒▓██████▓▒░  
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░    ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░  
                                                                                                         
  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡟⠧⠤⢾⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⠃
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣦⡀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠞⠃⠀⠀⢿⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⠃⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⡿⠙⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣠⡶⠤⠿⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣿⣿⡿⠁⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⢲⣤⠮⢿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⣾⡿⣫⢾⡟⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠞⣩⠞⣫⡾⣡⠋⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡴⠞⣉⡴⠋⣡⡾⢋⡾⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡟⠿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡤⠖⠋⣁⡴⠞⠉⣠⠞⢁⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠈⠻⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣶⠇⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡴⠖⠋⠁⣠⠴⠚⠉⢀⡰⠞⠁⣠⠞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠙⢷⣦⡀⣀⣠⣤⡶⠶⠛⠋⠉⣹⠇⠀⠀⠀⣀⣠⡤⠖⠒⠋⠉⠀⣠⡴⠒⠉⠀⢀⣠⠖⠋⢀⡤⠎⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠉⠛⠉⠉⠀⠀⠀⠀⠀⢠⡟⠒⠊⠉⠉⠁⠀⠀⣀⣤⠔⠚⠉⠁⠀⢀⣠⠖⠋⠁⢀⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠁⢀⣠⣤⠤⠒⠚⠉⠁⠀⠀⠀⣀⠴⠚⠉⠀⠀⣠⠞⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣴⠿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠏⠉⠁⠀⠀⠀⠀⠀⣀⣠⠴⠒⠉⠁⠀⠀⣀⠴⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣀⣴⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡏⠀⠀⣀⣀⡤⠴⠒⠋⠉⠀⠀⠀⢀⣠⠴⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣠⣴⠞⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢻⣞⠉⠉⠀⠀⠀⠀⠀⠀⣀⡤⠖⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠛⠿⠷⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣧⠀⠀⠀⢀⣠⠴⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣄⠀⠀⣠⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠙⠻⠶⢤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢷⡖⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣸⠈⠻⡛⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠹⣇⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⠀⠀⠀⠀⠈⢻⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠾⢿⣥⡀⠀⡈⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡄⠀⠀⠀⠀⠀⢠⡾⠋⠉⠙⠛⠛⠛⠛⠛⠛⠛⠛⠷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣧⡾⠉⠙⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠺⣷⠀⠀⠀⢀⣴⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡄⠀⣠⡾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢰⡄⠀⠀⠀⡀⠀⠀⠀⠀⠘⣧⣰⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢸⠙⠶⠶⣿⠋⠀⠀⠀⠀⠀⢹⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⢶⣄⠀⠀⠀⣀⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣤⣿⡋⠀⠀⠀⣯⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠀⠙⠷⠞⠛⣹⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡀⠀⠀⠀⠀⠀⠀
⠀⠉⠙⣇⣰⠓⠚⠻⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡶⠟⠀⠀⠀⠀⢠⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡟⠶⣾⡇⠀⠀⠀
⠀⠀⠀⠙⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⠿⣤⣤⡀⠀⠀⠀⠀⠻⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠻⢯⡄⢠⣽⣄⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣧⠀⣼⠟⠒⠒⠛⠷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⠏⠉⠉⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢛⡃⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
```

### Model Management
- **Sequential Loading**: Prevents memory issues by loading models sequentially
- **Health Checks**: Proactive model health verification
- **Resource Management**: Efficient model loading/unloading to reduce memory usage
- **Model Fallbacks**: Automatic fallback to alternative models when primary ones fail

### Error Resilience
- **Robust Retry Logic**: Configurable exponential backoff for transient errors
- **Error Classification**: Differentiation between recoverable and non-recoverable errors
- **Circuit Breaking**: Automatic disabling of consistently failing models
- **Response Validation**: Quality checks to ensure adequate responses

### JSON Processing
- **Automatic Repair**: Fixes common JSON formatting errors from model outputs
- **Schema Validation**: Ensures outputs conform to expected structures
- **Content Extraction**: Reliably extracts structured data from mixed text

### Pipeline Architecture
- **Step Dependencies**: Define dependencies between processing steps
- **Sequential Processing**: Controlled execution flow with proper error handling
- **Result Aggregation**: Combines outputs from multiple models into cohesive results
- **Execution Tracking**: Detailed metrics on pipeline performance

### Performance Optimization
- **Caching System**: File-based caching with TTL support
- **Result Reuse**: Avoids redundant API calls for identical requests
- **Parallel Processing**: Optional concurrent execution when appropriate

### Distributed Processing (Optional)
- **Celery Integration**: Scale across multiple workers (requires optional dependencies)
- **Task Distribution**: Offload model processing to worker nodes
- **Queue Management**: Prioritize and manage task queues

## Architecture

```
 ______   ______   ______   __  __   __   ______  ______   ______   ______  __  __   ______   ______    
/\  __ \ /\  == \ /\  ___\ /\ \_\ \ /\ \ /\__  _\/\  ___\ /\  ___\ /\__  _\/\ \/\ \ /\  == \ /\  ___\   
\ \  __ \\ \  __< \ \ \____\ \  __ \\ \ \\/_/\ \/\ \  __\ \ \ \____\/_/\ \/\ \ \_\ \\ \  __< \ \  __\   
 \ \_\ \_\\ \_\ \_\\ \_____\\ \_\ \_\\ \_\  \ \_\ \ \_____\\ \_____\  \ \_\ \ \_____\\ \_\ \_\\ \_____\ 
  \/_/\/_/ \/_/ /_/ \/_____/ \/_/\/_/ \/_/   \/_/  \/_____/ \/_____/   \/_/  \/_____/ \/_/ /_/ \/_____/ 
                                                                                                                                                             
```

PASTURE is built on three fundamental dependencies:

1. **Pydantic**: For robust data validation and configuration management
2. **Asyncio**: For efficient asynchronous processing and non-blocking I/O
3. **Tenacity**: For resilient retry logic with configurable backoff strategies

With optional support for:

- **Celery + Redis**: For distributed task processing and scaling across multiple workers

For a detailed architectural overview, see [ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Installation

```
🦙♡˙ᵕ˙🦙♡˙ᵕ˙🦙♡˙ᵕ˙🦙♡˙ᵕ˙🦙♡˙ᵕ˙🦙
	⠀⢰⡏⢹⡆⠀⠀⠀⢰⡏⢹⡆⠀
	⠀⢸⡇⣸⡷⠟⠛⠻⢾⣇⣸⡇⠀
	⢠⡾⠛⠉⠁⠀⠀⠀⠈⠉⠛⢷⡄
	⣿⠀⢀⣄⢀⣠⣤⣄⡀⣠⡀⠀⣿
	⢻⣄⠘⠋⡞⠉⢤⠉⢳⠙⠃⢠⡿
	⣼⠃⠀⠀⠳⠤⠬⠤⠞⠀⠀⠘⣷
	⢿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡿
	⢸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇
	⢸⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡿
🦙♡˙ᵕ˙🦙♡˙ᵕ˙🦙♡˙ᵕ˙🦙♡˙ᵕ˙🦙♡˙ᵕ˙🦙	
```

### Basic Installation

```bash
# Install Ollama (if not already installed)
# For Linux: curl -fsSL https://ollama.com/install.sh | sh
# For macOS: Download from https://ollama.com

# Install PASTURE with core dependencies
pip install pasture
```

### With Optional Dependencies

```bash
# With Celery support for distributed processing
pip install "pasture[celery]"

# With development tools
pip install "pasture[dev]"

# With all optional features
pip install "pasture[all]"
```

### From Source

```bash
git clone https://github.com/yourrepo/pasture.git
cd pasture
pip install -e .
```

## Configuration

```
   ╔═╗┌─┐┌┐┌┌─┐┬┌─┐┬ ┬┬─┐┌─┐┌┬┐┬┌─┐┌┐┌  ╦ ╦┌─┐┌─┐┌┬┐┌─┐ ┬ ┬┌─┐┬─┐┌┬┐┌─┐┬─┐┌─┐   
   ║  │ ││││├┤ ││ ┬│ │├┬┘├─┤ │ ││ ││││  ╠═╣├┤ ├─┤ │││─┼┐│ │├─┤├┬┘ │ ├┤ ├┬┘└─┐   
   ╚═╝└─┘┘└┘└  ┴└─┘└─┘┴└─┴ ┴ ┴ ┴└─┘┘└┘  ╩ ╩└─┘┴ ┴─┴┘└─┘└└─┘┴ ┴┴└─ ┴ └─┘┴└─└─┘   
   ╔═╗┌─┐┌─┐┬ ┬┌─┐     ╔╦╗┌─┐┌┬┐┌─┐┬  ┌─┐    ╦═╗┌─┐┌┬┐┬─┐┬ ┬                    
   ║  ├─┤│  ├─┤├┤      ║║║│ │ ││├┤ │  └─┐    ╠╦╝├┤  │ ├┬┘└┬┘                    
   ╚═╝┴ ┴└─┘┴ ┴└─┘     ╩ ╩└─┘─┴┘└─┘┴─┘└─┘    ╩╚═└─┘ ┴ ┴└─ ┴                     
    ╦ ╦╔╦╗╔╦╗╔═╗      ╦  ┌─┐┌─┐┌─┐     ╔╦╗┬┌─┐┌─┐                               
    ╠═╣ ║  ║ ╠═╝      ║  │ ││ ┬└─┐     ║║║│└─┐│                                 
    ╩ ╩ ╩  ╩ ╩        ╩═╝└─┘└─┘└─┘     ╩ ╩┴└─┘└─┘                               


```

PASTURE offers extensive configuration options using a hierarchical structure:

### Core Configuration

```python
from pasture import Config

# Create with defaults
config = Config()

# Or specify custom settings
config = Config(
    # Cache settings
    cache={"enabled": True, "dir": "./my_cache", "default_ttl": 7200},
    
    # Logging settings
    log_level="DEBUG",
    verbose_output=True,
    debug_mode=True,
    
    # HTTP settings
    request_timeout=120.0,
    
    # Retry settings
    retry={
        "max_attempts": 5,
        "strategy": "exponential",
        "min_wait": 1.0,
        "max_wait": 60.0
    },
    
    # Model settings
    preload_models=True,
    sequential_execution=True,
    fallback_threshold=3,
    min_response_length=20,
    
    # Misc settings
    simulation_mode=False
)
```

### From Configuration File

```python
# Load from a JSON configuration file
config = Config.from_file("path/to/config.json")
```

### Configuration Schema

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| **Cache Settings** |
| `cache.enabled` | bool | `True` | Enable caching of model responses |
| `cache.dir` | str | `"./cache"` | Directory for cached responses |
| `cache.default_ttl` | int | `3600` | Default time-to-live in seconds |
| **Log Settings** |
| `log_level` | enum | `"INFO"` | Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `verbose_output` | bool | `False` | Enable verbose output |
| `debug_mode` | bool | `False` | Enable debug mode |
| **HTTP Settings** |
| `request_timeout` | float | `90.0` | Timeout for API requests in seconds |
| **Retry Settings** |
| `retry.max_attempts` | int | `3` | Maximum number of retry attempts |
| `retry.strategy` | enum | `"exponential"` | Retry strategy (exponential, fixed, random_exponential, none) |
| `retry.min_wait` | float | `1.0` | Minimum wait time between retries |
| `retry.max_wait` | float | `30.0` | Maximum wait time between retries |
| **Model Settings** |
| `preload_models` | bool | `True` | Proactively load models before generating |
| `sequential_execution` | bool | `True` | Execute models sequentially to prevent resource contention |
| `fallback_threshold` | int | `2` | Number of failures before using fallback model |
| `min_response_length` | int | `10` | Minimum acceptable response length |
| **Misc Settings** |
| `simulation_mode` | bool | `False` | Run in simulation mode (no actual API calls) |

## Basic Usage

```
 ░░      ░░        ░        ░        ░        ░   ░░░  ░░      ░░░░░░░░      ░░        ░░      ░░       ░░        ░        ░       ░░
▒  ▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒  ▒▒▒▒    ▒▒  ▒  ▒▒▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒▒▒▒  ▒▒▒▒  ▒▒▒▒▒▒▒  ▒▒▒▒  ▒
▓  ▓▓▓   ▓      ▓▓▓▓▓▓  ▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓  ▓▓▓▓  ▓  ▓  ▓  ▓▓▓   ▓▓▓▓▓▓▓      ▓▓▓▓▓  ▓▓▓▓  ▓▓▓▓  ▓       ▓▓▓▓▓  ▓▓▓▓      ▓▓▓  ▓▓▓▓  ▓
█  ████  █  ██████████  ███████  ███████  ████  ██    █  ████  ████████████  ████  ████        █  ███  █████  ████  ███████  ████  █
██      ██        ████  ███████  ████        █  ███   ██      ████████      █████  ████  ████  █  ████  ████  ████        █       ██
                                                                                                                                    


```

### Simple Single-Model Example

```python
import asyncio
from pasture import Config, FileCache, ModelManager, ModelStep, Pipeline

async def main():
    # Initialize components
    config = Config()
    cache = FileCache(config.cache_dir)
    model_manager = ModelManager(config, cache)
    
    # Create a model step
    model_step = ModelStep(
        model_manager=model_manager,
        model_name="llama3",  # Use any model available in your Ollama
        prompt_template="Answer the following question: {query}",
        options={"temperature": 0.7}
    )
    
    # Create a pipeline with the step
    pipeline = Pipeline(
        steps=[("answer", model_step, [])],
        config=config
    )
    
    # Run the pipeline
    results = await pipeline.run({"query": "What is artificial intelligence?"})
    
    # Access the response
    response = results["results"]["answer"]["output"]["response"]
    print(response)
    
    # Clean up
    await model_manager.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### Multi-Model Pipeline

```python
import asyncio
from pasture import Config, FileCache, ModelManager, ModelStep, Pipeline

async def main():
    # Initialize components
    config = Config()
    cache = FileCache(config.cache_dir)
    model_manager = ModelManager(config, cache)
    
    # Create steps for different analyses
    economic_step = ModelStep(
        model_manager=model_manager,
        model_name="llama3",
        prompt_template="Analyze the economic impact of {query}.",
        options={"temperature": 0.7}
    )
    
    social_step = ModelStep(
        model_manager=model_manager,
        model_name="mistral",
        prompt_template="Analyze the social implications of {query}.",
        options={"temperature": 0.7}
    )
    
    integration_step = ModelStep(
        model_manager=model_manager,
        model_name="llama3",
        prompt_template="""
        Integrate these analyses into a comprehensive report:
        
        Topic: {query}
        
        Economic Analysis:
        {economic[response]}
        
        Social Analysis:
        {social[response]}
        """,
        options={"temperature": 0.5}
    )
    
    # Create pipeline with dependencies
    pipeline = Pipeline(
        steps=[
            ("economic", economic_step, []),  # No dependencies
            ("social", social_step, []),      # No dependencies
            ("integration", integration_step, ["economic", "social"])  # Depends on both analyses
        ],
        config=config
    )
    
    # Run the pipeline
    results = await pipeline.run({
        "query": "The impact of artificial intelligence on modern society"
    })
    
    # Get the integrated response
    final_response = results["results"]["integration"]["output"]["response"]
    print(final_response)
    
    # Clean up
    await model_manager.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Advanced Usage

```
   ___   ___ _   _____   _  ______________    __  _________  _________  _____________  ___  ______________  _____  __
  / _ | / _ \ | / / _ | / |/ / ___/ __/ _ \  / / / / __/ _ |/ ___/ __/ /_  __/ __/ _ \/ _ \/  _/_  __/ __ \/ _ \ \/ /
 / __ |/ // / |/ / __ |/    / /__/ _// // / / /_/ /\ \/ __ / (_ / _/    / / / _// , _/ , _// /  / / / /_/ / , _/\  / 
/_/ |_/____/|___/_/ |_/_/|_/\___/___/____/  \____/___/_/ |_\___/___/   /_/ /___/_/|_/_/|_/___/ /_/  \____/_/|_| /_/  
                                                                                                                     
⠀⣀⣀⣤⣤⣤⣤⣄⣀⣀⠀⠀⢀⣀⣀⣠⣤⣤⣤⣴⣤⣀⠀
⠘⠟⠋⢉⣠⣤⣭⣭⠭⡍⠀⠀⠀⢩⠭⣭⣭⣤⣄⡈⠙⠻⠂
⠀⠀⠴⠯⢽⣿⡿⣹⣍⠟⠀⠀⠀⠻⠸⠏⠿⠿⠧⡽⠂⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠆⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠀⢰⠃⠀⠀
⠀⠀⠀⠀⠀⢠⣀⣀⣀⣀⣀⣀⣀⣀⡤⠤⠞⠁⢀⡏⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠋⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠸⠀⠀⠀⠀

```

### Customizing Model Options

```python
# Create a step with detailed model options
step = ModelStep(
    model_manager=model_manager,
    model_name="llama3",
    prompt_template="Generate creative text about {topic}.",
    options={
        "temperature": 0.8,  # Higher for more creative output
        "top_p": 0.95,       # Nucleus sampling parameter
        "top_k": 40          # Consider top 40 tokens
    }
)
```

### Adding Fallback Models

```python
# Create a step with fallback models
step = ModelStep(
    model_manager=model_manager,
    model_name="llama3",
    prompt_template="Answer: {query}",
    options={"temperature": 0.7},
    fallback_models=["mistral", "phi3", "gemma"]  # Try these in order if primary fails
)
```

### Implementing Caching Strategy

```python
# Initialize cache with custom directory
cache = FileCache("./my_cache_dir")

# Set responses with specific TTL values
await cache.set(cache_key, response, ttl=3600)  # Cache for 1 hour
await cache.set(cache_key, response, ttl=86400)  # Cache for 1 day
await cache.set(cache_key, response, ttl=None)   # Cache indefinitely

# Get cache statistics
stats = await cache.get_stats()
print(f"Active entries: {stats['active_entries']}")
print(f"Cache size: {stats['cache_size_bytes']} bytes")

# Clear specific entries or entire cache
await cache.clear("specific_key")  # Clear one entry
await cache.clear()                # Clear all entries
```

### Distributed Processing with Celery

To use distributed processing, install the optional dependencies:

```bash
pip install "pasture[celery]"
```

```python
# You need Redis running as a message broker

import asyncio
from pasture import Config, FileCache, ModelManager
from pasture.distributed import CeleryModelStep, DistributedPipeline

async def main():
    # Initialize components
    config = Config()
    cache = FileCache(config.cache_dir)
    model_manager = ModelManager(config, cache)
    
    # Create Celery-based steps
    step1 = CeleryModelStep(
        model_name="llama3",
        prompt_template="Analyze this: {query}",
        options={"temperature": 0.7},
        task_timeout=180  # 3 minute timeout
    )
    
    step2 = CeleryModelStep(
        model_name="mistral",
        prompt_template="Summarize this analysis: {step1[response]}",
        options={"temperature": 0.5},
        task_timeout=120  # 2 minute timeout
    )
    
    # Create distributed pipeline
    pipeline = DistributedPipeline(
        steps=[
            ("step1", step1, []),
            ("step2", step2, ["step1"])
        ],
        config=config
    )
    
    # Run the pipeline
    results = await pipeline.run({"query": "Complex topic for distributed analysis"})
    
    # Access results
    print(results["results"]["step2"]["output"]["response"])

if __name__ == "__main__":
    asyncio.run(main())
```

For details on Celery integration, see [CELERY.md](docs/CELERY.md).

## Model Management

```
⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣶⣶⣦⠀⠀
⠀⠀⣠⣤⣤⣄⣀⣾⣿⠟⠛⠻⢿⣷⠀
⢰⣿⡿⠛⠙⠻⣿⣿⠁⠀⠀⠀⣶⢿⡇
⢿⣿⣇⠀⠀⠀⠈⠏⠀⠀⠀Model Management
⠀⠻⣿⣷⣦⣤⣀⠀⠀⠀⠀⣾⡿⠃⠀
⠀⠀⠀⠀⠉⠉⠻⣿⣄⣴⣿⠟⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣿⡿⠟⠁⠀⠀⠀⠀
```

### Preloading and Unloading Models

PASTURE can automatically preload models before use and unload them when switching to different models to optimize memory usage:

```python
# Enable automatic model preloading/unloading
config = Config(preload_models=True)
model_manager = ModelManager(config, cache)

# Manual model loading/unloading
await model_manager.preload_model("llama3")
await model_manager.unload_model("llama3")
```

### Model Health Checks

PASTURE continuously monitors model health and can automatically switch to fallbacks:

```python
# Check model health
is_healthy = await model_manager.check_model_health("llama3")

# Get a fallback model if the primary is unhealthy
fallback = await model_manager.get_fallback_model("llama3", available_models)
```

### Model Status Tracking

The system keeps track of model statuses to make intelligent decisions:

```python
# Get comprehensive status report
status_report = await model_manager.get_model_status_report()
print(f"Active model: {status_report['active_model']}")
print(f"Loaded models: {status_report['loaded_models']}")
```

## Caching Strategies

```
                          ▗▄▄▖ ▗▄▖  ▗▄▄▖▗▖ ▗▖▗▄▄▄▖     ▗▄▄▖▗▄▄▄▖▗▖  ▗▖▗▄▄▄▖▗▄▄▖  ▗▄▖ ▗▖                
                         ▐▌   ▐▌ ▐▌▐▌   ▐▌ ▐▌▐▌       ▐▌   ▐▌   ▐▛▚▖▐▌  █  ▐▌ ▐▌▐▌ ▐▌▐▌                
                         ▐▌   ▐▛▀▜▌▐▌   ▐▛▀▜▌▐▛▀▀▘    ▐▌   ▐▛▀▀▘▐▌ ▝▜▌  █  ▐▛▀▚▖▐▛▀▜▌▐▌                
                         ▝▚▄▄▖▐▌ ▐▌▝▚▄▄▖▐▌ ▐▌▐▙▄▄▖    ▝▚▄▄▖▐▙▄▄▖▐▌  ▐▌  █  ▐▌ ▐▌▐▌ ▐▌▐▙▄▄▖             
       ▗▖ ▗▖▗▄▄▄▖▗▖  ▗▖          ▗▄▄▄▖▗▄▄▄▖▗▖             ▗▖  ▗▖ ▗▄▖ ▗▖           ▗▄▄▖▗▄▄▄▖▗▄▖▗▄▄▄▖    
       ▐▌▗▞▘▐▌    ▝▚▞▘             █    █  ▐▌             ▐▌  ▐▌▐▌ ▐▌▐▌          ▐▌     █ ▐▌ ▐▌ █      
       ▐▛▚▖ ▐▛▀▀▘  ▐▌              █    █  ▐▌             ▐▌  ▐▌▐▛▀▜▌▐▌           ▝▀▚▖  █ ▐▛▀▜▌ █      
       ▐▌ ▐▌▐▙▄▄▖  ▐▌              █    █  ▐▙▄▄▖           ▝▚▞▘ ▐▌ ▐▌▐▙▄▄▖       ▗▄▄▞▘  █ ▐▌ ▐▌ █      
                                                                                                       
                                                                                                                                                        
```

### Basic Caching

Cache is enabled by default and can be configured:

```python
config = Config(
    cache_dir="./my_cache",  # Custom cache directory
)
cache = FileCache(config.cache_dir)
```

### TTL (Time-To-Live) Caching

Set expiration times for cached responses:

```python
# Cache a response for 1 hour (3600 seconds)
await cache.set("cache_key", response_data, ttl=3600)

# Cache a response permanently
await cache.set("static_data", static_data)
```

### Cache Management

```python
# Clear a specific cache entry
await cache.clear("cache_key")

# Clear all cache entries
await cache.clear()

# Get cache statistics
stats = await cache.get_stats()
print(f"Total entries: {stats['total_entries']}")
print(f"Expired entries: {stats['expired_entries']}")
print(f"Cache size: {stats['cache_size_bytes']} bytes")
```

## Pipeline Orchestration

```
    ┌───┐            ┌───┐
    │ A │            │ B │
    └─┬─┘            └─┬─┘
      │                │
      └───┐        ┌───┘
          ▼        ▼
         ┌──────────┐
         │    C     │
         └────┬─────┘
              │
              ▼
         ┌────────┐
         │   D    │
         └────────┘
```

### Pipeline Construction

```python
from pasture import Pipeline, ModelStep

# Create steps with dependencies
economic_step = ModelStep(model_manager, "llama3", "Analyze economic impacts: {query}")
social_step = ModelStep(model_manager, "mistral", "Analyze social impacts: {query}")
integration_step = ModelStep(
    model_manager, 
    "llama3", 
    "Integrate these analyses:\nEconomic: {economic[response]}\nSocial: {social[response]}"
)

# Define the pipeline with dependencies
pipeline = Pipeline(
    steps=[
        ("economic", economic_step, []),              # No dependencies
        ("social", social_step, []),                  # No dependencies
        ("integration", integration_step, ["economic", "social"])  # Depends on both
    ],
    config=config
)

# Run the pipeline
results = await pipeline.run({"query": "Impact of AI on manufacturing"})
```

### Custom Pipeline Steps

Create custom analysis steps by extending the `AnalysisStep` class:

```python
class DataPreprocessingStep(AnalysisStep):
    async def execute(self, data):
        # Process the input data
        processed_data = process_data(data["query"])
        
        return {
            "output": {"processed_data": processed_data},
            "time": execution_time,
            "status": "success"
        }
    
    async def get_fallback(self, data):
        # Fallback logic if primary execution fails
        return {
            "output": {"processed_data": simple_process(data["query"])},
            "time": execution_time,
            "status": "success",
            "fallback": True
        }

# Use in a pipeline
pipeline = Pipeline(
    steps=[
        ("preprocess", DataPreprocessingStep(), []),
        ("analyze", analyze_step, ["preprocess"])
    ],
    config=config
)
```

## Error Handling and Resilience

```
        _.--"""""--._
      .'`   ERROR   `'.
     /                 \
    |    *'^'v'*^'* |
    |  v PROTECTION ^v |
    |    Y*^'v'*^'v* |
     \                 /
      `.             .'
        `-._______.-'
           \  |  /
            ` V '
```

### Automatic Retries

Configure retry behavior:

```python
config = Config(
    max_retries=3,       # Maximum retry attempts
    retry_delay=2.0      # Base delay between retries (with exponential backoff)
)
```

### Fallback Models

Configure automatic fallbacks:

```python
step = ModelStep(
    model_manager=model_manager,
    model_name="llama3",
    prompt_template="Answer: {query}",
    fallback_models=["mistral", "phi3"]  # Try these models if llama3 fails
)
```

### Error Recovery

Handle and recover from various error types:

```python
try:
    response = await model_manager.generate_with_model("llama3", prompt)
    
    if "error" in response:
        error_type = response["error"]
        if error_type == "timeout":
            # Handle timeout error
            logger.warning("Request timed out, using cached results")
            response = get_cached_fallback()
        elif error_type == "connection_error":
            # Handle connection error
            logger.error("Connection failed")
            response = generate_error_response()
    
    # Process successful response
    return process_response(response)
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return generate_error_response()
```

## JSON Processing

```
   ▗▖ ▗▄▄▖ ▗▄▖ ▗▖  ▗▖    ▗▄▄▖ ▗▄▄▖  ▗▄▖  ▗▄▄▖▗▄▄▄▖ ▗▄▄▖ ▗▄▄▖▗▄▄▄▖▗▖  ▗▖ ▗▄▄▖       ▗▄▄▖ ▗▄▄▄▖▗▄▄▖  ▗▄▖ ▗▄▄▄▖▗▄▄▖ 
   ▐▌▐▌   ▐▌ ▐▌▐▛▚▖▐▌    ▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌▐▌   ▐▌   ▐▌   ▐▌     █  ▐▛▚▖▐▌▐▌          ▐▌ ▐▌▐▌   ▐▌ ▐▌▐▌ ▐▌  █  ▐▌ ▐▌
   ▐▌ ▝▀▚▖▐▌ ▐▌▐▌ ▝▜▌    ▐▛▀▘ ▐▛▀▚▖▐▌ ▐▌▐▌   ▐▛▀▀▘ ▝▀▚▖ ▝▀▚▖  █  ▐▌ ▝▜▌▐▌▝▜▌       ▐▛▀▚▖▐▛▀▀▘▐▛▀▘ ▐▛▀▜▌  █  ▐▛▀▚▖
▗▄▄▞▘▗▄▄▞▘▝▚▄▞▘▐▌  ▐▌    ▐▌   ▐▌ ▐▌▝▚▄▞▘▝▚▄▄▖▐▙▄▄▖▗▄▄▞▘▗▄▄▞▘▗▄█▄▖▐▌  ▐▌▝▚▄▞▘       ▐▌ ▐▌▐▙▄▄▖▐▌   ▐▌ ▐▌▗▄█▄▖▐▌ ▐▌
                                                                                                                
  { "status": "operational",
    "fixes": [
      "quotes", "commas", "braces"
    ],
    "capabilities": {
      "extract": true,
      "validate": true,
      "repair": true
    }
  }
```

### JSON Validation and Repair

```python
from pasture import JSONProcessor

# Check if string is valid JSON
is_valid = JSONProcessor.is_valid_json('{"key": "value"}')

# Extract JSON from text
json_str = JSONProcessor.extract_json("Here's some JSON: {\"key\": \"value\"}")

# Repair malformed JSON
fixed_json = JSONProcessor.repair_json("{'key': 'value'}")

# Parse JSON with robust error handling
parsed = JSONProcessor.parse('{"key": "value"}')
```

### Schema Validation

```python
from pydantic import BaseModel

# Define a schema
class AnalysisSchema(BaseModel):
    economic_impact: str
    social_impact: str
    recommendations: list[str]

# Validate response against schema
valid, validated_data = await JSONProcessor.validate_with_schema(response, AnalysisSchema)

if valid:
    # Use validated data
    print(validated_data["recommendations"])
else:
    # Handle validation failure
    print("Response did not match expected schema")
```

## Performance Optimization

```
 (       (   (       )  (      *              )                     )     )  (            
 )\ )    )\ ))\ ) ( /(  )\ ) (  `    (     ( /(   (           (  ( /(  ( /(  )\ )  *   )  
(()/((  (()/(()/( )\())(()/( )\))(   )\    )\())  )\  (     ( )\ )\()) )\())(()/(` )  /(  
 /(_))\  /(_))(_)|(_)\  /(_)|(_)()((((_)( ((_)\ (((_) )\    )((_|(_)\ ((_)\  /(_))( )(_)) 
(_))((_)(_))(_))_| ((_)(_)) (_()((_)\ _ )\ _((_))\___((_)  ((_)_  ((_)  ((_)(_)) (_(_())  
| _ \ __| _ \ |_  / _ \| _ \|  \/  (_)_\(_) \| ((/ __| __|  | _ )/ _ \ / _ \/ __||_   _|  
|  _/ _||   / __|| (_) |   /| |\/| |/ _ \ | .` || (__| _|   | _ \ (_) | (_) \__ \  | |    
|_| |___|_|_\_|   \___/|_|_\|_|  |_/_/ \_\|_|\_| \___|___|  |___/\___/ \___/|___/  |_|    
                                                                                          
```

### Concurrent Processing

Use asyncio for concurrent operations:

```python
import asyncio

async def process_multiple_queries(queries):
    # Create tasks for each query
    tasks = [
        model_manager.generate_with_model("llama3", query)
        for query in queries
    ]
    
    # Run tasks concurrently
    results = await asyncio.gather(*tasks)
    return results
```

### Resource Management

Optimize model loading/unloading for memory efficiency:

```python
config = Config(
    preload_models=True,       # Preload models before use
    sequential_execution=True  # Execute models sequentially to avoid memory pressure
)
```

### Batch Processing

Process related items together:

```python
async def analyze_documents(documents):
    results = []
    
    # Process in batches of 5
    batch_size = 5
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        
        # Process batch concurrently
        tasks = [
            model_manager.generate_with_model(
                "llama3", 
                f"Summarize this document: {doc}"
            )
            for doc in batch
        ]
        
        batch_results = await asyncio.gather(*tasks)
        results.extend(batch_results)
        
        # Small delay between batches to prevent rate limiting
        await asyncio.sleep(1)
    
    return results
```

## Distributed Processing

```
 ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
 │  Worker 1   │ │  Worker 2   │ │  Worker 3   │
 └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
                ┌───────▼───────┐
                │  Task Queue   │
                └───────────────┘
```

For high-volume workloads, PASTURE supports distributed processing with Celery.

### Setting Up Distributed Processing

Install with Celery support:
```bash
pip install "pasture[celery]"
```

Configure Celery integration:

```python
from pasture import Config, CeleryModelStep, DistributedPipeline

# Create steps with CeleryModelStep
economic_step = CeleryModelStep(
    model_name="llama3",
    prompt_template="Analyze economic impact: {query}",
    options={"temperature": 0.7},
    task_timeout=180
)

# Create distributed pipeline
pipeline = DistributedPipeline(
    steps=[
        ("economic", economic_step, []),
        # More steps...
    ],
    config=config
)

# Run the pipeline
results = await pipeline.run({"query": "Impact of AI on society"})
```

### Worker Management

Run Celery workers to process distributed tasks:

```bash
# Start Redis (if not already running)
redis-server

# Start Celery workers (in separate terminal)
celery -A pasture.celery_app worker --loglevel=info

# Optional: Monitor tasks with Flower
pip install flower
celery -A pasture.celery_app flower
```

## Adapting to Other Platforms

```
 ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
 ┃     CROSS-PLATFORM COMPATIBILITY      ┃
 ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
 ┏━━━━━━━━━━┓ ┏━━━━━━━━━━┓ ┏━━━━━━━━━━━┓
 ┃  OpenAI  ┃ ┃   Azure  ┃ ┃ Anthropic ┃
 ┗━━━━━━━━━━┛ ┗━━━━━━━━━━┛ ┗━━━━━━━━━━━┛
```

PASTURE can be adapted to work with other AI platforms beyond Ollama.

### OpenAI Compatibility

Create an OpenAI adapter by extending the ModelManager class:

```python
class OpenAIModelManager(ModelManager):
    def __init__(self, config, cache, api_key):
        super().__init__(config, cache)
        self.api_key = api_key
    
    async def _request(self, endpoint, method="GET", json_data=None):
        # Override to use OpenAI API instead of Ollama
        url = f"https://api.openai.com/v1/{endpoint}"
        
        session = await self._get_session()
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Implementation details...
```

Other adapters can be created for platforms like Anthropic Claude, Azure OpenAI, etc.

## Important Considerations

```
⋆·˚ ༘ *⚠️💣💥⋆·˚ ༘ *⚠️💣💥⋆·˚ ༘ *⚠️💣💥⋆·˚ ༘ *⚠️💣💥⋆·˚ ༘ *⚠️💣💥⋆·˚ ༘ *⚠️💣💥⋆·˚ ༘ *⚠️💣💥⋆·˚⋆·˚ ༘ *⚠️💣💥⋆·˚ ༘ *⚠️💣💥⋆·
 ▗▄▄▄▖▗▖  ▗▖▗▄▄▖  ▗▄▖ ▗▄▄▖▗▄▄▄▖▗▄▖ ▗▖  ▗▖▗▄▄▄▖     ▗▄▄▖ ▗▄▖ ▗▖  ▗▖ ▗▄▄▖▗▄▄▄▖▗▄▄▄ ▗▄▄▄▖▗▄▄▖  ▗▄▖▗▄▄▄▖▗▄▄▄▖ ▗▄▖ ▗▖  ▗▖ ▗▄▄▖ 
  █  ▐▛▚▞▜▌▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌ █ ▐▌ ▐▌▐▛▚▖▐▌  █      ▐▌   ▐▌ ▐▌▐▛▚▖▐▌▐▌     █  ▐▌  █▐▌   ▐▌ ▐▌▐▌ ▐▌ █    █  ▐▌ ▐▌▐▛▚▖▐▌▐▌    
  █  ▐▌  ▐▌▐▛▀▘ ▐▌ ▐▌▐▛▀▚▖ █ ▐▛▀▜▌▐▌ ▝▜▌  █      ▐▌   ▐▌ ▐▌▐▌ ▝▜▌ ▝▀▚▖  █  ▐▌  █▐▛▀▀▘▐▛▀▚▖▐▛▀▜▌ █    █  ▐▌ ▐▌▐▌ ▝▜▌ ▝▀▚▖ 
▗▄█▄▖▐▌  ▐▌▐▌   ▝▚▄▞▘▐▌ ▐▌ █ ▐▌ ▐▌▐▌  ▐▌  █      ▝▚▄▄▖▝▚▄▞▘▐▌  ▐▌▗▄▄▞▘▗▄█▄▖▐▙▄▄▀▐▙▄▄▖▐▌ ▐▌▐▌ ▐▌ █  ▗▄█▄▖▝▚▄▞▘▐▌  ▐▌▗▄▄▞▘ 
▗▄▄▖ ▗▄▄▄▖ ▗▄▖ ▗▄▄▄      ▗▄▄▖ ▗▄▖ ▗▄▄▖ ▗▄▄▄▖▗▄▄▄▖▗▖ ▗▖▗▖   ▗▖ ▗▖  ▗▖    ▗▄▄▖ ▗▄▄▄▖▗▄▄▄▖ ▗▄▖ ▗▄▄▖ ▗▄▄▄▖    ▗▖ ▗▖ ▗▄▄▖▗▄▄▄▖
▐▌ ▐▌▐▌   ▐▌ ▐▌▐▌  █    ▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌   ▐▌   ▐▌ ▐▌▐▌   ▐▌  ▝▚▞▘     ▐▌ ▐▌▐▌   ▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌       ▐▌ ▐▌▐▌   ▐▌   
▐▛▀▚▖▐▛▀▀▘▐▛▀▜▌▐▌  █    ▐▌   ▐▛▀▜▌▐▛▀▚▖▐▛▀▀▘▐▛▀▀▘▐▌ ▐▌▐▌   ▐▌   ▐▌      ▐▛▀▚▖▐▛▀▀▘▐▛▀▀▘▐▌ ▐▌▐▛▀▚▖▐▛▀▀▘    ▐▌ ▐▌ ▝▀▚▖▐▛▀▀▘
▐▌ ▐▌▐▙▄▄▖▐▌ ▐▌▐▙▄▄▀    ▝▚▄▄▖▐▌ ▐▌▐▌ ▐▌▐▙▄▄▖▐▌   ▝▚▄▞▘▐▙▄▄▖▐▙▄▄▖▐▌      ▐▙▄▞▘▐▙▄▄▖▐▌   ▝▚▄▞▘▐▌ ▐▌▐▙▄▄▖    ▝▚▄▞▘▗▄▄▞▘▐▙▄▄▖
                                                                                                                                     
⋆·˚ ༘ *⚠️💣💥⋆·˚ ༘ *⚠️💣💥⋆·˚ ༘ *⚠️💣💥⋆·˚ ༘ *⚠️💣💥⋆·˚ ༘ *⚠️💣💥⋆·˚ ༘ *⚠️💣💥⋆·˚ ༘ *⚠️💣⋆·˚ ༘ *⚠️💣💥⋆·˚ ༘ ⋆·˚ ༘ *⚠️💣                                                                                                                      
```

### 1. PASTURE is an Orchestration Framework

PASTURE focuses on the "how" (orchestration), not the "what" (model selection and prompt engineering). You still need to:
- Choose appropriate models for each task
- Design effective prompts
- Configure model parameters like temperature, top_p, etc.
- Define the pipeline structure and dependencies

### 2. Memory Management

Ollama loads models into memory, which can consume significant resources. PASTURE helps by:
- Loading models sequentially
- Unloading unused models
- Providing fallback mechanisms for when models fail to load

However, you should still be mindful of:
- Total system memory available
- Size of models you're using
- Number of models loaded simultaneously

### 3. Prompt Design Remains Critical

PASTURE doesn't improve model outputs directly - the quality of responses depends primarily on:
- Your prompt design
- Model selection
- Parameter tuning

PASTURE helps ensure reliable orchestration, but you still need to craft effective prompts.

### 4. Error Handling Strategy

Consider how your application should handle failures:
- Should it fail fast or try multiple fallbacks?
- What's an acceptable timeout?
- How should partial results be presented?

Configure retry settings based on your specific requirements.

## Troubleshooting

```
 ┌───────────────────────────────┐
 │      TROUBLESHOOTING          │
 │                               │
 │      ┌───┐                    │
 │      │ ? │                    │
 │      └───┘                    │
 └───────────────────────────────┘
```

### Common Issues

1. **Models fail to load**
   - Check system memory availability
   - Verify model exists in Ollama: `ollama list`
   - Try running model directly: `ollama run model-name`

2. **Slow performance**
   - Enable caching to reduce repeat API calls
   - Consider smaller models if memory constrained
   - Check network connectivity to Ollama

3. **Poor quality responses**
   - Review and improve prompts
   - Adjust temperature and other generation parameters
   - Ensure models are appropriate for the task

### Debugging

Enable debug mode for detailed logging:

```python
config = Config(debug_mode=True, log_level="DEBUG")
```

## More Information

- [Installation Guide](docs/INSTALL.md)
- [API Reference](docs/API.md)
- [Architecture Details](docs/ARCHITECTURE.md)
- [Celery Integration](docs/CELERY.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
 ┌───────────────────────────────────────────────────┐
 │                                                   │
 │               Happy Model Orchestrating!          │
 │                                                   │
 │        The greatest things often have             │
 │               yet to be built...                  │
 │                                                   │
 └───────────────────────────────────────────────────┘
```
