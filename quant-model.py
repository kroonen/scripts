import os
import sys
import subprocess
import argparse
from tqdm import tqdm

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {cmd}")
        print(f"Error message: {e.stderr}")
        sys.exit(1)

def detect_gpu():
    try:
        nvidia_smi = run_command("nvidia-smi")
        return True
    except:
        return False

def convert_to_gguf(model_dir):
    print(f"Converting {model_dir} to GGUF format...")
    convert_cmd = f"python ./convert_hf_to_gguf.py {model_dir}"
    run_command(convert_cmd)
    print("Conversion complete.")

def quantize_model(input_file, output_file, type_id, use_gpu, threads):
    gpu_flag = f"-ngl 35" if use_gpu else ""  # Assuming 35 layers, adjust as needed
    thread_flag = f"-t {threads}" if threads else ""
    quantize_cmd = f"./llama-quantize {gpu_flag} {thread_flag} {input_file} {output_file} {type_id}"
    run_command(quantize_cmd)

def convert_and_quantize(model_dir, output_dir, use_gpu, threads):
    model_name = os.path.basename(model_dir)
    
    # Convert the model to GGUF format
    convert_to_gguf(model_dir)
    
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
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Quantize the model with different configurations
    input_file = os.path.join(model_dir, "ggml-model-f16.gguf")
    for config, type_id in tqdm(quantize_configs, desc="Quantizing"):
        output_file = os.path.join(output_dir, f"{model_name}-{config}.gguf")
        print(f"Quantizing to {config}...")
        quantize_model(input_file, output_file, type_id, use_gpu, threads)
        print(f"Quantization to {config} complete.")

def main():
    parser = argparse.ArgumentParser(description="Convert and quantize LLaMA models.")
    parser.add_argument("model_dir", help="Directory containing the model to quantize")
    parser.add_argument("--output-dir", default=".", help="Output directory for quantized models")
    parser.add_argument("--no-gpu", action="store_true", help="Disable GPU usage")
    parser.add_argument("--threads", type=int, default=16, help="Number of threads to use")
    args = parser.parse_args()

    use_gpu = detect_gpu() and not args.no_gpu
    if use_gpu:
        print("GPU detected and will be used for quantization.")
    else:
        print("GPU not detected or disabled. CPU will be used for quantization.")

    convert_and_quantize(args.model_dir, args.output_dir, use_gpu, args.threads)

if __name__ == "__main__":
    main()
