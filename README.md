# Autogen_Core1

A multi-agent, agentic AI project featuring a Pizza Shop simulation and agent-based game logic. This repository demonstrates advanced Python async programming, agent orchestration, and secure development practices.

## Features

- **PizzaShop_Project**: Modular pizza shop simulation with creative naming, customer service, and chef agents.
- **autogenCore_practise**: Experiments with agent logic, including best-of-3 Rock-Paper-Scissors, async/await patterns, and gRPC-based agent runtimes.
- **Secure by Design**: No secrets or API keys are stored in the repository. Use `.env` files locally for configuration.

## Project Structure
```
Autogen_Core1/
├── main.py
├── pyproject.toml
├── README.md
├── autogenCore_practise/
│   ├── llm_config.py
│   ├── singleTreaded.ipynb
│   └── ...
└── PizzaShop_Project/
    ├── main.py
    ├── agents/
    ├── config/
    ├── messages/
    ├── utils/
    └── ...
```

## Getting Started
1. **Clone the repository:**
   ```sh
   git clone https://github.com/BalajiG2002/Autogen_Core1.git
   cd Autogen_Core1
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   # or use pyproject.toml with poetry/uv
   ```
3. **Set up your `.env` files:**
   - Copy `.env.example` to `.env` in each relevant folder and add your API keys (do not commit secrets).

## Usage
- Run the main simulation:
  ```sh
  python main.py
  ```
- Explore agent logic and experiments in the `autogenCore_practise` notebooks and scripts.

## Security
- **Never commit secrets:** All API keys and sensitive data must be kept in local `.env` files and are excluded from version control.
- **GitHub Push Protection:** This repository is protected by secret scanning and push protection.

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](LICENSE)

---
*Created by Balaji Gopi and contributors.*
