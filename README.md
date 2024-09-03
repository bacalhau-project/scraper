# Artifact Collector

This tool allows you to collect and consolidate data from various sources, including GitHub repositories and websites. It also provides functionality to consolidate the collected data into a specified token context window using Ollama and Llama models.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/bacalhau-project/scraper.git
   cd scraper
   ```

2. Install the required Python packages:
   ```bash
   uv venv .venv --seed
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

3. Install Ollama:
   - For Linux:
     ```bash
     curl https://ollama.ai/install.sh | sh
     ```
   - For MacOS:
     ```bash
     brew install ollama
     ```
   - For Windows:
     Download the installer from [Ollama's official website](https://ollama.ai/download)

4. Pull the Llama3.1 model using Ollama:
   ```bash
   ollama pull llama3.1:8b
   ```

## Usage

The script provides several options:

1. Download data:
   ```bash
   python main.py --download
   ```

2. Consolidate data into multiple files (max 5MB each):
   ```bash
   python main.py --consolidate
   ```

3. Consolidate data to a specific token context size using Ollama:
   ```bash
   python main.py --context-consolidate 2048 --model llama3.1:8b
   ```

   You can adjust the context size (e.g., 2048) and the model name as needed.

4. Perform all operations:
   ```bash
   python main.py --download --consolidate --context-consolidate 2048
   ```

## Configuration

Edit the `config.json` file to specify:
- Output directory
- GitHub repositories to clone/update
- Websites to scrape
- Maximum depth for web crawling
- Maximum pages per site
- Number of worker threads

## Troubleshooting

If you encounter any issues with Ollama or the Llama model:

1. Ensure Ollama is running:
   ```bash
   ollama serve
   ```

2. Check available models:
   ```bash
   ollama list
   ```

3. If the Llama3.1 model is missing, pull it again:
   ```bash
   ollama pull llama3.1:8b
   ```

4. For more detailed Ollama usage, refer to the [Ollama documentation](https://github.com/jmorganca/ollama/tree/main/docs).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.