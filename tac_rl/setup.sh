#!/bin/bash
set -e

echo "🚀 Setting up TAC-RL: TheAgentCompany Reinforcement Learning Training System"
echo "============================================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check Python version
    if ! command -v python &> /dev/null; then
        error "Python not found. Please install Python 3.12+"
    fi
    
    python_version=$(python --version | cut -d' ' -f2)
    log "Found Python $python_version"
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        error "Docker not found. Please install Docker"
    fi
    
    docker_version=$(docker --version | cut -d' ' -f3 | tr -d ',')
    log "Found Docker $docker_version"
    
    # Check Docker Compose
    if ! docker compose version &> /dev/null; then
        error "Docker Compose not found. Please install Docker Compose"
    fi
    
    compose_version=$(docker compose version | cut -d' ' -f4)
    log "Found Docker Compose $compose_version"
    
    # Check available disk space (need 30+ GB)
    available_space=$(df -h . | awk 'NR==2{print $4}' | sed 's/G//')
    if [ "${available_space%%.*}" -lt 30 ]; then
        warn "Available disk space: ${available_space}G. Recommend 30+ GB for full setup"
    else
        log "Available disk space: ${available_space}G ✓"
    fi
}

# Create directory structure
create_directories() {
    log "Creating directory structure..."
    
    mkdir -p tac_rl/{components,configs,data,outputs,checkpoints,logs}
    mkdir -p tac_rl/components/{task_sampling,openhands_integration,reward_computation,art_training,monitoring}
    
    log "Directory structure created ✓"
}

# Install Python dependencies
install_dependencies() {
    log "Installing Python dependencies..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        python -m venv venv
        log "Created virtual environment"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install core dependencies
    pip install \
        openhands-ai==0.42.0 \
        openpipe-art \
        torch \
        transformers \
        accelerate \
        peft \
        datasets \
        pyyaml \
        wandb \
        rich \
        typer \
        pydantic \
        aiohttp \
        docker \
        pandas \
        numpy \
        matplotlib \
        seaborn \
        jupyter \
        bitsandbytes \
        vllm
        
    log "Python dependencies installed ✓"
}

# Setup TheAgentCompany infrastructure
setup_tac_infrastructure() {
    log "Setting up TheAgentCompany infrastructure..."
    
    # Check if services are already running
    if docker ps | grep -q "api-server"; then
        log "TheAgentCompany services already running ✓"
        return 0
    fi
    
    log "Starting TheAgentCompany services (this may take 10-30 minutes)..."
    
    # Set proper Docker socket permissions
    if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo chmod 666 /var/run/docker.sock 2>/dev/null || warn "Could not set Docker socket permissions"
    fi
    
    # Download and run setup script
    curl -fsSL https://github.com/TheAgentCompany/the-agent-company-backup-data/releases/download/setup-script-20241208/setup.sh | sh
    
    # Wait for services to be ready
    log "Waiting for services to be ready..."
    timeout=1800  # 30 minutes
    elapsed=0
    while [ $elapsed -lt $timeout ]; do
        if curl -s http://localhost:2999/health > /dev/null 2>&1; then
            log "TheAgentCompany services are ready ✓"
            return 0
        fi
        sleep 30
        elapsed=$((elapsed + 30))
        log "Waiting... ($elapsed/${timeout}s)"
    done
    
    error "Services failed to start within timeout"
}

# Validate setup
validate_setup() {
    log "Validating setup..."
    
    # Check if Python packages are importable
    source venv/bin/activate
    
    if python -c "import openhands; print('OpenHands:', openhands.__version__)" 2>/dev/null; then
        log "OpenHands import successful ✓"
    else
        error "OpenHands import failed"
    fi
    
    if python -c "import openpipe; print('OpenPipe ART available')" 2>/dev/null; then
        log "OpenPipe ART import successful ✓"
    else
        error "OpenPipe ART import failed"
    fi
    
    # Check TheAgentCompany services
    if curl -s http://localhost:2999/health | grep -q "healthy"; then
        log "TheAgentCompany API server healthy ✓"
    else
        warn "TheAgentCompany API server not responding"
    fi
    
    # Check individual services
    services=("rocketchat:3000" "gitlab:8080" "plane:3001" "owncloud:8081")
    for service in "${services[@]}"; do
        IFS=':' read -ra ADDR <<< "$service"
        service_name="${ADDR[0]}"
        port="${ADDR[1]}"
        
        if curl -s "http://localhost:$port" > /dev/null 2>&1; then
            log "$service_name service responding ✓"
        else
            warn "$service_name service not responding on port $port"
        fi
    done
}

# Generate sample configuration
generate_config() {
    log "Generating sample configuration..."
    
    cat > tac_rl/configs/qwen_2_5_7b.yaml << EOF
# TAC-RL Configuration for Qwen 2.5 7B Model
model:
  name: "qwen-2.5-7b-tacrl"
  base_model_path: "Qwen/Qwen2.5-7B-Instruct"
  model_type: "qwen"
  parameter_count: "7B"
  context_length: 32768
  supports_function_calling: true

training:
  algorithm: "grpo"
  batch_size: 4
  learning_rate: 1e-5
  max_episodes_per_task: 3
  reward_scale: 1.0
  
  # Training phases
  current_phase: "warmup"
  tasks_per_phase: 15
  success_threshold: 0.6
  
  # Infrastructure
  max_parallel_tasks: 2
  checkpoint_frequency: 50
  evaluation_frequency: 25
  
  # Paths
  output_dir: "./outputs"
  checkpoint_dir: "./checkpoints" 
  log_dir: "./logs"

# Task selection for different phases
task_phases:
  warmup:
    - "admin-make-spreadsheet"
    - "hr-check-attendance-one-day"
    - "ds-calculate-spreadsheet-stats"
  
  intermediate:
    - "admin-arrange-meeting-rooms"
    - "hr-check-attendance-multiple-days"
    - "finance-budget-variance"
    
  advanced:
    - "pm-create-plane-issue"
    - "admin-employee-info-reconciliation"
    - "ds-merge-multiple-sheets"

# OpenHands configuration  
openhands:
  max_iterations: 100
  timeout: 300
  enable_auto_lint: true
  use_host_network: true

# Environment configuration
environment:
  server_hostname: "localhost"
  services:
    - "gitlab"
    - "plane" 
    - "rocketchat"
    - "owncloud"
    - "api-server"

# Monitoring and logging
monitoring:
  use_wandb: true
  project_name: "tac-rl-training"
  log_level: "INFO"
  save_trajectories: true
EOF

    log "Sample configuration created: tac_rl/configs/qwen_2_5_7b.yaml ✓"
}

# Main setup function
main() {
    echo "Starting TAC-RL setup..."
    
    check_prerequisites
    create_directories
    install_dependencies
    setup_tac_infrastructure
    validate_setup
    generate_config
    
    echo ""
    echo -e "${GREEN}🎉 TAC-RL setup completed successfully!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Activate the virtual environment: source venv/bin/activate"
    echo "2. Start training: python tac_rl/train.py --config tac_rl/configs/qwen_2_5_7b.yaml"
    echo "3. Monitor progress: python tac_rl/monitor.py --run-id latest"
    echo ""
    echo "For more information, see tac_rl/README.md"
}

# Run main function
main "$@"