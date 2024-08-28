import os
import sys
import subprocess

def convert_and_quantize(model_dir):
    model_name = os.path.basename(model_dir)
    
    # Convert the model to GGUF format
    convert_cmd = f"python ./convert_hf_to_gguf.py {model_dir}"
    subprocess.run(convert_cmd, shell=True)
    
    # Define the quantization configurations
    quantize_configs = [
        ("Q8_0", 7),
        ("Q4_K_S", 14),
        ("Q4_K_M", 15),
        ("Q5_K_S", 16),
        ("Q5_K_M", 17),
        ("Q6_K", 18),
        ("Q3_K_L", 13),
        ("Q3_K_M", 12),
        ("Q3_K_S", 11),
        ("F16", 1)
    ]
    
    # Quantize the model with different configurations
    for config, type_id in quantize_configs:
        input_file = os.path.join(model_dir, "ggml-model-f16.gguf")
        output_file = f"{model_name}-{config}.gguf"
        quantize_cmd = f"./llama-quantize {input_file} {output_file} {type_id}"
        subprocess.run(quantize_cmd, shell=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <model_directory>")
        sys.exit(1)
    
    model_dir = sys.argv[1]
    convert_and_quantize(model_dir)
