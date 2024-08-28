# Rob's Scripts Collection 🚀

A growing collection of scripts to make your life easier! Whether you're updating models, backing up data, or automating tasks, these scripts have you covered.

## Scripts Included

- **Ollama Model Updater:**
  - **Script:** `update_ollama_models.ps1`
  - **Purpose:** Automatically updates all your Ollama models with real-time progress tracking.
  
- **Hugging Face Backup:**
  - **Script:** `hf_backup.py`
  - **Purpose:** Back up all your Hugging Face models and spaces to a local directory.

- ** LLaMa.CPP Quantizer:**
  - Script: `quant-model.py`
  - Purpose: Quantize raw language models to .GGUF files, supporting various quantization levels from 16-bit floating point down to 3-bit integer precision.

## Quick Start

1. **Clone the repo:**
    ```bash
    git clone https://github.com/kroonen/scripts.git
    ```
    
2. **Navigate to the script directory:**
    ```bash
    cd scripts
    ```
    
3. **Run the scripts:**
    - **For Ollama:**
      ```powershell
      ./update_ollama_models.ps1
      ```
    - **For Hugging Face:**
      ```bash
      python hf_backup.py
      ```
    - **For LLaMa.CPP Quantizer:**
      ```bash
      python quant-model ./{{MODEL_DIRECTORY}}
      ```

## More to Come
Stay tuned for more handy scripts! 🌟

## License
MIT License
