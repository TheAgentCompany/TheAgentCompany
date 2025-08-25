#!/usr/bin/env python3
"""
GPU Validation Script for TAC-RL
================================

Validates GPU setup and memory requirements for local model training.
"""

import sys
import logging
from pathlib import Path

def check_cuda_availability():
    """Check if CUDA is available"""
    try:
        import torch
        
        if not torch.cuda.is_available():
            print("❌ CUDA not available. GPU training requires CUDA.")
            print("   Install CUDA toolkit: https://developer.nvidia.com/cuda-toolkit")
            return False
        
        print(f"✅ CUDA available: {torch.version.cuda}")
        return True
        
    except ImportError:
        print("❌ PyTorch not installed. Run: pip install torch")
        return False

def check_gpu_memory():
    """Check GPU memory requirements"""
    try:
        import torch
        
        if not torch.cuda.is_available():
            return False
        
        device_count = torch.cuda.device_count()
        print(f"📊 Found {device_count} CUDA device(s):")
        
        suitable_gpus = []
        
        for i in range(device_count):
            props = torch.cuda.get_device_properties(i)
            memory_gb = props.total_memory / (1024**3)
            
            print(f"   GPU {i}: {props.name}")
            print(f"   Memory: {memory_gb:.1f} GB")
            print(f"   Compute Capability: {props.major}.{props.minor}")
            
            if memory_gb >= 12:
                suitable_gpus.append(i)
                print(f"   ✅ Suitable for training")
            else:
                print(f"   ❌ Insufficient memory (need 12+ GB)")
            
            print()
        
        if suitable_gpus:
            print(f"✅ {len(suitable_gpus)} GPU(s) suitable for training")
            return True
        else:
            print("❌ No GPUs with sufficient memory found")
            print("   Minimum: 12 GB (RTX 3090/4090)")  
            print("   Recommended: 16+ GB (RTX 4090/6000)")
            return False
            
    except Exception as e:
        print(f"❌ Error checking GPU: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    
    required_packages = [
        ("torch", "PyTorch"),
        ("transformers", "HuggingFace Transformers"),
        ("peft", "Parameter-Efficient Fine-Tuning"),
        ("accelerate", "HuggingFace Accelerate"),
        ("art", "OpenPipe ART"),
        ("openhands", "OpenHands")
    ]
    
    missing = []
    
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name}")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("   Run: ./tac_rl/setup.sh")
        return False
    
    return True

def estimate_memory_usage():
    """Estimate GPU memory usage for training"""
    
    print("\n📊 Estimated GPU Memory Usage:")
    print("   Base Model (7B):    ~14 GB")
    print("   LoRA Adapters:      ~32 MB") 
    print("   Training Batch:     ~2 GB")
    print("   RULER Judge:        ~4 GB")
    print("   ________________________")
    print("   Total Estimated:    ~20 GB")
    print()
    print("💡 GPU Recommendations:")
    print("   Minimum:    RTX 4090 (24 GB)")
    print("   Recommended: RTX 6000 Ada (48 GB)")
    print("   Professional: A100 (80 GB)")

def main():
    """Main validation function"""
    
    print("🔧 TAC-RL GPU Validation")
    print("=" * 40)
    
    all_good = True
    
    print("\n1. Checking CUDA availability...")
    if not check_cuda_availability():
        all_good = False
    
    print("\n2. Checking GPU memory...")
    if not check_gpu_memory():
        all_good = False
        
    print("\n3. Checking dependencies...")
    if not check_dependencies():
        all_good = False
    
    estimate_memory_usage()
    
    print("\n" + "=" * 40)
    if all_good:
        print("🎉 All validations passed! Ready for training.")
        print("   Start training: python tac_rl/train.py --config configs/qwen_2_5_7b_local.yaml")
    else:
        print("❌ Some validations failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()