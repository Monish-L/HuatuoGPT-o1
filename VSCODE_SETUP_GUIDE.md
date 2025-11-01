# 💻 Complete Visual Studio Code Setup Guide (Zero to Hero)

This guide assumes you know **absolutely nothing** about Visual Studio Code. We'll go through **every single step** to get you set up and training your model.

---

## 📋 Table of Contents

1. [Installing Visual Studio Code](#step-1-installing-visual-studio-code)
2. [First Launch and Initial Setup](#step-2-first-launch-and-initial-setup)
3. [Installing Essential Extensions](#step-3-installing-essential-extensions)
4. [Opening the Project](#step-4-opening-the-project)
5. [Understanding the VS Code Interface](#step-5-understanding-the-vs-code-interface)
6. [Setting Up the Terminal](#step-6-setting-up-the-terminal)
7. [Environment Setup](#step-7-environment-setup)
8. [Downloading the Dataset](#step-8-downloading-the-dataset)
9. [Running the Training](#step-9-running-the-training)
10. [Monitoring Training](#step-10-monitoring-training)
11. [Troubleshooting](#step-11-troubleshooting)
12. [VS Code Tips and Shortcuts](#step-12-vs-code-tips-and-shortcuts)

---

## Step 1: Installing Visual Studio Code

### 1.1 Download VS Code

**For Windows:**
1. Open your web browser (Chrome, Firefox, Edge, etc.)
2. Go to: https://code.visualstudio.com/
3. You'll see a big blue button that says "Download for Windows"
4. Click the button - a file called `VSCodeUserSetup-x64-X.XX.X.exe` will download
5. Wait for the download to complete (usually takes 1-2 minutes)

**For macOS:**
1. Go to: https://code.visualstudio.com/
2. Click "Download for Mac"
3. A file called `VSCode-darwin-universal.zip` will download
4. Wait for the download to complete

**For Linux (Ubuntu/Debian):**
1. Open Terminal (press `Ctrl + Alt + T`)
2. Copy and paste these commands one by one:
```bash
# Download and install VS Code
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
rm -f packages.microsoft.gpg

# Update and install
sudo apt update
sudo apt install code
```

### 1.2 Install VS Code

**For Windows:**
1. Find the downloaded file (usually in your Downloads folder)
2. Double-click `VSCodeUserSetup-x64-X.XX.X.exe`
3. A window will appear asking "Do you want to allow this app to make changes?" - Click **Yes**
4. License agreement appears - Click **I accept the agreement** → Click **Next**
5. Choose installation location - Leave default → Click **Next**
6. Select Start Menu Folder - Leave default → Click **Next**
7. **IMPORTANT**: On "Select Additional Tasks" screen:
   - ✅ Check "Add 'Open with Code' action to Windows Explorer file context menu"
   - ✅ Check "Add 'Open with Code' action to Windows Explorer directory context menu"
   - ✅ Check "Add to PATH"
   - Click **Next**
8. Click **Install** - Wait for installation (takes 1-2 minutes)
9. Click **Finish**

**For macOS:**
1. Find the downloaded `.zip` file in your Downloads folder
2. Double-click to extract it - creates `Visual Studio Code.app`
3. Drag `Visual Studio Code.app` to your Applications folder
4. Double-click to open it
5. If you see "Visual Studio Code is an app downloaded from the internet", click **Open**

**For Linux:**
Already installed from terminal commands above!

### 1.3 Verify Installation

**Windows:**
1. Press `Windows Key` on keyboard
2. Type: `code`
3. You should see "Visual Studio Code" appear
4. Click it to open

**macOS:**
1. Press `Cmd + Space` to open Spotlight
2. Type: `visual studio code`
3. Press Enter to open

**Linux:**
1. Press `Super Key` (Windows key) or open application menu
2. Type: `code`
3. Click Visual Studio Code

---

## Step 2: First Launch and Initial Setup

### 2.1 First Launch

1. **Open VS Code** (using method from Step 1.3)
2. **Welcome Screen appears** - Don't worry about this for now
3. You'll see a dark or light themed window - that's VS Code!

### 2.2 Basic Settings

Let's make VS Code comfortable for you:

1. **Choose a Theme** (optional but nice):
   - Look at the top menu bar
   - Click **File** → **Preferences** → **Color Theme**
     - (On Mac: **Code** → **Preferences** → **Color Theme**)
   - Use arrow keys to preview different themes
   - I recommend: **Dark+ (default dark)** or **Light+ (default light)**
   - Press **Enter** when you find one you like

2. **Set Auto Save** (so you don't lose work):
   - Click **File** → **Auto Save**
   - A checkmark appears - files now save automatically!

---

## Step 3: Installing Essential Extensions

Extensions add features to VS Code. We need a few for Python development.

### 3.1 Open Extensions View

**Method 1:**
- Look at the left sidebar (vertical bar with icons)
- Click the icon that looks like **4 squares** (with one separated) - This is Extensions
- The icon is near the bottom of the left sidebar

**Method 2:**
- Press `Ctrl + Shift + X` (Windows/Linux)
- Press `Cmd + Shift + X` (Mac)

You'll see a panel titled "EXTENSIONS" open on the left.

### 3.2 Install Python Extension

1. **In the Extensions search box** (at the top where it says "Search Extensions in Marketplace")
2. **Type**: `Python`
3. **Look for**: "Python" by Microsoft (it should be the first result)
   - It has a blue Python logo
   - Says "IntelliSense (Pylance), Linting, Debugging..."
4. **Click** the **Install** button (blue button)
5. **Wait** for installation (takes 10-30 seconds)
6. When done, the button changes to show a gear icon ⚙️

### 3.3 Install Jupyter Extension (Useful for Notebooks)

1. **In the same search box**, clear it and type: `Jupyter`
2. **Look for**: "Jupyter" by Microsoft
   - Has an orange/red logo
3. **Click Install**
4. **Wait** for installation

### 3.4 Install Pylance (Python Language Server)

This might already be installed with Python extension, but let's check:

1. **Search for**: `Pylance`
2. **Look for**: "Pylance" by Microsoft
3. If you see **Install** button - click it
4. If you see **Uninstall** or gear icon - it's already installed! ✓

### 3.5 Install GitLens (Optional but Helpful)

For better Git integration:

1. **Search for**: `GitLens`
2. **Look for**: "GitLens — Git supercharged" by GitKraken
3. **Click Install**

### 3.6 Verify Extensions Installed

1. Click the Extensions icon again (4 squares icon)
2. At the top, you should see tabs: "Search", "Installed", etc.
3. Click **Installed**
4. You should see:
   - ✅ Python
   - ✅ Jupyter
   - ✅ Pylance
   - ✅ GitLens (if you installed it)

---

## Step 4: Opening the Project

### 4.1 Locate Your Project

**Important**: First, you need to know where your HuatuoGPT-o1 project is located.

Based on our setup, it should be at:
```
/home/user/HuatuoGPT-o1
```

If you're on Windows and cloned it somewhere else, you need to know that path.

### 4.2 Open the Folder in VS Code

**Method 1 - Using File Menu:**
1. In VS Code, click **File** → **Open Folder...**
2. A file browser window opens
3. Navigate to your project location:
   - **Linux/Mac**: Go to `/home/user/HuatuoGPT-o1`
   - **Windows**: Navigate to wherever you cloned the repository
4. Click on the **HuatuoGPT-o1** folder (just once to select it)
5. Click **Select Folder** (or **Open** button, depending on your system)

**Method 2 - Using Terminal (Linux/Mac):**
1. Open your regular terminal (outside VS Code)
2. Type:
```bash
cd /home/user/HuatuoGPT-o1
code .
```
3. VS Code opens with the project!

### 4.3 Trust the Workspace

When the folder opens, you might see a message:
> "Do you trust the authors of the files in this folder?"

1. Click **Yes, I trust the authors**
   - This allows VS Code to run scripts and extensions properly

### 4.4 Verify Project Opened

Look at the left sidebar - you should now see:
- **EXPLORER** section at the top
- A folder icon with "HUATUOGPT-O1"
- Files listed below:
  - GETTING_STARTED.md
  - QUICKSTART.md
  - SETUP_AND_TRAINING_GUIDE.md
  - train_stage1.sh
  - download_and_prepare_dataset.py
  - And more...

**Congratulations!** 🎉 Your project is now open in VS Code!

---

## Step 5: Understanding the VS Code Interface

Let me explain what you're seeing:

### 5.1 The Main Areas

```
┌─────────────────────────────────────────────────────────┐
│  File  Edit  Selection  View  Go  Run  Terminal  Help  │ ← Menu Bar
├────┬────────────────────────────────────────────────────┤
│    │  Tab Bar (open files appear here)                  │
│    ├────────────────────────────────────────────────────┤
│ S  │                                                     │
│ i  │                                                     │
│ d  │            Editor Area                              │
│ e  │            (where you read/edit files)              │
│ b  │                                                     │
│ a  │                                                     │
│ r  ├────────────────────────────────────────────────────┤
│    │  Terminal Panel (appears at bottom)                │
└────┴────────────────────────────────────────────────────┘
```

### 5.2 Left Sidebar Icons (Top to Bottom)

Click each icon to see what it does:

1. **📄 Explorer** - Browse your project files
2. **🔍 Search** - Search across all files
3. **🔀 Source Control** - Git version control
4. **▶️ Run and Debug** - Debug your code
5. **📦 Extensions** - Install/manage extensions
6. **⚙️ Accounts/Settings** (at bottom)

### 5.3 Key Areas Explained

**Explorer (File Browser):**
- Shows all files and folders in your project
- Click a file to open it
- Right-click for more options (rename, delete, etc.)

**Editor:**
- The big area in the middle
- Where you view and edit files
- Can have multiple tabs open

**Terminal:**
- Command line interface at the bottom
- We'll use this to run commands
- If you don't see it, don't worry - we'll open it next!

---

## Step 6: Setting Up the Terminal

The terminal is where we'll run all our commands. Let's set it up properly.

### 6.1 Open the Terminal

**Method 1:**
- Look at the top menu
- Click **Terminal** → **New Terminal**

**Method 2:**
- Press `` Ctrl + ` `` (that's the backtick key, usually above Tab)
- On Mac: `` Cmd + ` ``

A panel opens at the bottom of VS Code - this is your integrated terminal!

### 6.2 Understanding the Terminal

You should see something like:
```bash
user@computer:~/HuatuoGPT-o1$
```

This is your command prompt. It shows:
- Your username (`user`)
- Your computer name (`computer`)
- Current directory (`~/HuatuoGPT-o1`)
- `$` means ready for input

### 6.3 Verify You're in the Right Directory

Type this command and press Enter:
```bash
pwd
```

You should see:
```
/home/user/HuatuoGPT-o1
```

This confirms you're in the project directory! ✓

### 6.4 List Files

Let's see what files are here:
```bash
ls -la
```

You should see a list of files including:
- GETTING_STARTED.md
- train_stage1.sh
- download_and_prepare_dataset.py
- SFT_stage1.py
- And more...

**Great!** Your terminal is working and you're in the right place.

---

## Step 7: Environment Setup

Now we'll set up Python and install all dependencies. Follow carefully!

### 7.1 Check if Conda is Installed

In the terminal, type:
```bash
conda --version
```

**If you see**: `conda X.XX.X` - Conda is installed! ✓ Skip to Step 7.3

**If you see**: `conda: command not found` - You need to install it! Continue to 7.2

### 7.2 Install Miniconda (If Needed)

**For Linux:**
```bash
# Download Miniconda installer
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Run installer
bash Miniconda3-latest-Linux-x86_64.sh

# Press Enter to continue
# Press Space to scroll through license
# Type 'yes' and press Enter to accept
# Press Enter to confirm installation location
# Type 'yes' when asked to initialize Miniconda3

# Close and reopen terminal, or run:
source ~/.bashrc

# Verify installation
conda --version
```

**For Windows:**
1. Download from: https://docs.conda.io/en/latest/miniconda.html
2. Choose "Miniconda3 Windows 64-bit"
3. Run the installer
4. Use default settings
5. Close and reopen VS Code
6. Open new terminal in VS Code

**For macOS:**
```bash
# Download installer
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh

# Run installer
bash Miniconda3-latest-MacOSX-x86_64.sh

# Follow prompts (same as Linux)
# Close and reopen terminal
source ~/.bash_profile
conda --version
```

### 7.3 Create Conda Environment

Now let's create a clean Python environment for our project:

**Step-by-step:**

1. **Create the environment:**
```bash
conda create -n huatuogpt python=3.10 -y
```
- This creates an environment named "huatuogpt"
- With Python 3.10
- `-y` means "yes" to all prompts
- **Wait**: This takes 1-2 minutes

2. **Activate the environment:**
```bash
conda activate huatuogpt
```

3. **Verify activation:**
   - Your terminal prompt should change to:
   ```bash
   (huatuogpt) user@computer:~/HuatuoGPT-o1$
   ```
   - See the `(huatuogpt)` at the beginning? That means it's activated! ✓

### 7.4 Check GPU Availability

Before installing packages, let's verify your GPU:

```bash
nvidia-smi
```

You should see:
- A table showing your GPU(s)
- GPU names (like "NVIDIA A100", "RTX 4090", etc.)
- Memory information
- Temperature and usage stats

**If you see an error:**
- "nvidia-smi: command not found" - NVIDIA drivers not installed
- "No devices were found" - GPU not detected
- Stop here and install NVIDIA drivers first!

### 7.5 Install PyTorch

PyTorch is the deep learning framework. Installation depends on your CUDA version.

**Find your CUDA version:**
```bash
nvidia-smi
```
Look at the top right corner - you'll see "CUDA Version: XX.X"

**Install PyTorch based on CUDA version:**

**For CUDA 11.8:**
```bash
pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu118
```

**For CUDA 12.1:**
```bash
pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121
```

**Wait**: This takes 5-10 minutes (PyTorch is large!)

**Verify PyTorch installation:**
```bash
python -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU count: {torch.cuda.device_count()}')"
```

You should see:
```
PyTorch version: 2.5.1
CUDA available: True
GPU count: X  (where X is your number of GPUs)
```

**If CUDA available is False** - something went wrong with CUDA installation!

### 7.6 Install All Other Dependencies

Now install all project dependencies:

```bash
pip install -r requirements-complete.txt
```

**What happens:**
- Lots of text scrolling by
- Installing many packages
- **Takes**: 10-20 minutes
- Some warnings are okay (yellow text)
- Errors are NOT okay (red text)

**If you see errors:**
- Read the error message
- Most common: DeepSpeed compilation issues
- Solution: `pip install deepspeed==0.15.4 --no-build-isolation`

**Verify installations:**
```bash
python -c "import transformers, accelerate, datasets, deepspeed; print('✓ All packages installed successfully!')"
```

You should see:
```
✓ All packages installed successfully!
```

### 7.7 Login to HuggingFace

You need a HuggingFace account to download models and datasets.

**If you don't have an account:**
1. Go to: https://huggingface.co/join
2. Sign up (it's free!)
3. Verify your email
4. Go to: https://huggingface.co/settings/tokens
5. Click "New token"
6. Give it a name: "HuatuoGPT Training"
7. Role: "read"
8. Click "Generate"
9. **Copy the token** (looks like: `hf_xxxxxxxxxxxxx`)

**Login in terminal:**
```bash
huggingface-cli login
```

You'll see:
```
Enter your token:
```

- **Paste your token** (right-click in terminal, or Ctrl+Shift+V)
- Press Enter
- You should see: `Login successful`

**For LLaMA models (if using LLaMA):**
1. Go to: https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct
2. Click "Agree and access repository"
3. Fill out the form
4. Wait for approval (usually instant)

---

## Step 8: Downloading the Dataset

Now let's download the medical reasoning dataset!

### 8.1 Understand What We're Downloading

- **Dataset**: FreedomIntelligence/medical-o1-reasoning-SFT
- **Size**: ~500 MB
- **Samples**: 19,700 medical reasoning examples
- **Format**: Question + Chain-of-Thought + Response

### 8.2 View the Download Script

Let's look at the script first:

1. **In VS Code Explorer** (left sidebar), find and click:
   - `download_and_prepare_dataset.py`
2. The file opens in the editor
3. **Read through it** - notice the helpful comments explaining what it does
4. Don't edit anything yet!

### 8.3 Run the Download Script

**In the terminal** (make sure `(huatuogpt)` environment is active):

```bash
python download_and_prepare_dataset.py --subset en --output_dir ./data
```

**What you'll see:**
```
================================================================================
Downloading FreedomIntelligence/medical-o1-reasoning-SFT dataset...
================================================================================

📥 Loading dataset subset 'en' (split: train)...
This may take a few minutes depending on your internet connection.

Downloading data: 100%|████████████| 500MB/500MB [XX:XX<00:00, XXMBit/s]
✓ Successfully loaded 19700 samples!

================================================================================
Converting to training format...
================================================================================
Processing samples: 100%|████████████| 19700/19700 [00:30<00:00]

💾 Saving processed dataset to ./data/medical_o1_sft_en_data.json...

================================================================================
✓ Dataset preparation complete!
================================================================================
📊 Total samples: 19700
📁 Saved to: ./data/medical_o1_sft_en_data.json
💾 File size: 487.25 MB
================================================================================
```

**Wait time**: 5-15 minutes depending on internet speed

### 8.4 Verify Dataset Downloaded

Check the data folder:

```bash
ls -lh ./data/
```

You should see:
```
medical_o1_sft_en_data.json  (~500 MB)
```

**Verify file contents:**
```bash
python -c "import json; data = json.load(open('./data/medical_o1_sft_en_data.json')); print(f'✓ Loaded {len(data)} samples'); print(f'✓ First sample has keys: {list(data[0].keys())}')"
```

Should show:
```
✓ Loaded 19700 samples
✓ First sample has keys: ['Question', 'Complex_CoT', 'Response']
```

**Perfect!** ✓ Dataset is ready!

---

## Step 9: Running the Training

Now for the exciting part - let's train the model!

### 9.1 Review Training Configuration

First, let's look at the training script:

1. **In Explorer**, click: `train_stage1.sh`
2. The file opens - you'll see a bash script
3. **Scroll to the top** - find the "CONFIGURATION" section

Key settings to check:
```bash
MODEL_PATH="meta-llama/Llama-3.1-8B-Instruct"  # The base model
DATA_PATH="./data/medical_o1_sft_en_data.json"  # Your data
NUM_GPUS=8                                       # Number of GPUs
TRAIN_BSZ_PER_GPU=2                              # Batch size
N_EPOCHS=3                                       # Training epochs
```

### 9.2 Adjust Configuration (If Needed)

**Do you have fewer than 8 GPUs?**
- Click at the line with `NUM_GPUS=8`
- Change the number to match your GPU count
- Example: If you have 4 GPUs → `NUM_GPUS=4`
- File saves automatically (we enabled auto-save earlier!)

**Do you have limited GPU memory?**
- Find line: `TRAIN_BSZ_PER_GPU=2`
- Change to: `TRAIN_BSZ_PER_GPU=1`
- Find line: `GRADIENT_ACCUMULATION_STEPS=8`
- Change to: `GRADIENT_ACCUMULATION_STEPS=16`

**Want to use a different model?**
- Find line: `MODEL_PATH="meta-llama/Llama-3.1-8B-Instruct"`
- Change to your desired model
- Example: `MODEL_PATH="Qwen/Qwen2.5-7B-Instruct"`

### 9.3 Make Script Executable

In terminal:
```bash
chmod +x train_stage1.sh
```

This gives the script permission to run.

### 9.4 Run Pre-flight Check

Let's test the script without actually training:

```bash
./train_stage1.sh
```

You'll see pre-flight checks:
```
================================================================================
                  HuatuoGPT-o1 Stage 1 Training
================================================================================

Running pre-flight checks...

✓ Python found: Python 3.10.X
✓ NVIDIA GPU found:
    1  Tesla V100, 32480 MiB
    2  Tesla V100, 32480 MiB
    ...
✓ Data file found: ./data/medical_o1_sft_en_data.json
✓ Training script found: SFT_stage1.py
✓ Accelerate library found
✓ Transformers library found
✓ Output directories created

================================================================================
                         Training Configuration
================================================================================
Model:                    meta-llama/Llama-3.1-8B-Instruct
Data:                     ./data/medical_o1_sft_en_data.json
Output Directory:         ./ckpts/sft_stage1
Number of GPUs:           8
Batch Size per GPU:       2
Gradient Accumulation:    8
Effective Batch Size:     128
Learning Rate:            5e-6
Number of Epochs:         3
Max Sequence Length:      8192
================================================================================

Ready to start training? This may take many hours. Continue? [y/N]:
```

**Review everything carefully!**

- Check GPU count is correct
- Check data path is correct
- Note the effective batch size
- Note expected training time

### 9.5 Start Training

If everything looks good:

1. Type: `y`
2. Press Enter

**Training starts!**

You'll see:
```
================================================================================
                         Starting Training
================================================================================

Using multi-GPU configuration with DeepSpeed ZeRO-3
Loading checkpoint shards: 100%|████████| 4/4 [00:10<00:00]
Loading dataset...
✓ Successfully loaded 19700 samples
Training...
```

Then:
```
Epoch 0:   0%|          | 0/1234 [00:00<?, ?it/s]
```

The progress bar updates as training progresses!

### 9.6 What's Happening Now

Your model is training! Here's what's going on:

**Behind the scenes:**
1. Model weights loaded to GPUs
2. Dataset loaded into memory
3. Training loop started
4. Model learns from each batch
5. Checkpoints saved after each epoch

**Your screen shows:**
- Current epoch
- Progress bar
- Current step / total steps
- Time elapsed / estimated time remaining
- Loss value (should decrease)
- Accuracy (should increase)
- Learning rate

---

## Step 10: Monitoring Training

### 10.1 Understanding the Progress Display

You'll see something like:
```
Epoch 0: 23%|██▍       | 285/1234 [1:23:45<4:32:10, loss=2.345, acc=0.456, length=8192, lr=4.2e-6]
```

Let's decode this:
- **Epoch 0**: First training pass through data (0/3)
- **23%**: 23% through this epoch
- **285/1234**: Completed 285 batches out of 1234
- **1:23:45**: Time elapsed (1 hour, 23 minutes, 45 seconds)
- **<4:32:10**: Estimated time remaining
- **loss=2.345**: Training loss (should decrease over time)
- **acc=0.456**: Training accuracy (should increase over time)
- **length=8192**: Sequence length being processed
- **lr=4.2e-6**: Current learning rate

### 10.2 Monitor GPU Usage

Open a **second terminal**:

**In VS Code:**
1. Click the **+** button in terminal panel (top right of terminal)
2. Or press `` Ctrl + Shift + ` `` (Cmd + Shift + ` on Mac)

**In the new terminal:**
```bash
watch -n 1 nvidia-smi
```

This refreshes GPU stats every second. You'll see:
- GPU utilization % (should be 90-100%)
- Memory usage (should be near max)
- Temperature
- Power draw

Press `Ctrl + C` to stop watching.

### 10.3 View Checkpoints

Training saves checkpoints after each epoch.

**Check checkpoints:**
```bash
ls -lh ./ckpts/sft_stage1/
```

You should eventually see:
```
checkpoint-0-1234/
checkpoint-1-2468/
checkpoint-2-3702/
```

Each checkpoint folder contains:
```
checkpoint-X-XXXX/
  └── tfmr/            # The trained model
      ├── config.json
      ├── model.safetensors
      ├── tokenizer_config.json
      └── ...
```

### 10.4 Training Logs

Logs are saved to:
```
./train_logs/sft_stage1_medical_o1/
```

View recent logs:
```bash
tail -f ./train_logs/sft_stage1_medical_o1/wandb/latest-run/logs/debug.log
```

Press `Ctrl + C` to stop viewing.

### 10.5 Expected Training Timeline

**On 8x A100 (80GB) GPUs:**
- Epoch 0: ~4-6 hours
- Epoch 1: ~4-6 hours
- Epoch 2: ~4-6 hours
- **Total**: 12-18 hours

**On fewer/slower GPUs:**
- Proportionally longer

**What to expect:**
- **Hours 0-2**: Loss drops quickly (3.0 → 2.0)
- **Hours 2-6**: Loss drops more slowly (2.0 → 1.7)
- **Hours 6-18**: Fine-tuning (1.7 → 1.5)
- **Accuracy**: Rises from ~0.3 to ~0.6-0.7

### 10.6 Signs Training is Going Well

✅ **Good signs:**
- Loss is decreasing
- Accuracy is increasing
- GPU utilization is high (>80%)
- No error messages
- Checkpoints being saved

❌ **Bad signs:**
- Loss increasing or stuck
- Many "CUDA out of memory" errors
- GPU utilization very low (<50%)
- Training crashes
- Loss becomes NaN

---

## Step 11: Troubleshooting

### 11.1 CUDA Out of Memory

**Error message:**
```
RuntimeError: CUDA out of memory. Tried to allocate X.XX GiB
```

**Solution:**

1. **Stop training**: Press `Ctrl + C` in terminal
2. **Edit train_stage1.sh**: Click the file in Explorer
3. **Reduce batch size**: Find and change:
   ```bash
   TRAIN_BSZ_PER_GPU=2   # Change to 1
   ```
4. **Increase gradient accumulation**:
   ```bash
   GRADIENT_ACCUMULATION_STEPS=8   # Change to 16
   ```
5. **Optionally reduce sequence length**:
   ```bash
   MAX_SEQ_LEN=8192   # Change to 4096
   ```
6. **Save the file** (auto-saves)
7. **Restart training**: `./train_stage1.sh`

### 11.2 Dataset Not Found

**Error message:**
```
FileNotFoundError: [Errno 2] No such file or directory: './data/medical_o1_sft_en_data.json'
```

**Solution:**

1. **Check if file exists**:
   ```bash
   ls -la ./data/
   ```

2. **If missing, re-download**:
   ```bash
   python download_and_prepare_dataset.py --subset en --output_dir ./data
   ```

### 11.3 HuggingFace Authentication Error

**Error message:**
```
OSError: You are trying to access a gated repo.
```

**Solution:**

1. **Login to HuggingFace**:
   ```bash
   huggingface-cli login
   ```

2. **For LLaMA models**:
   - Go to: https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct
   - Click "Agree and access repository"
   - Wait for approval

3. **Restart training**

### 11.4 Python Package Import Error

**Error message:**
```
ModuleNotFoundError: No module named 'XXX'
```

**Solution:**

1. **Verify environment is activated**:
   ```bash
   conda activate huatuogpt
   ```
   - Look for `(huatuogpt)` in prompt

2. **Reinstall dependencies**:
   ```bash
   pip install -r requirements-complete.txt
   ```

3. **If specific package**:
   ```bash
   pip install <package-name>
   ```

### 11.5 Training is Very Slow

**Symptoms:**
- Progress bar barely moving
- Low GPU utilization
- Taking much longer than expected

**Solutions:**

1. **Check GPU usage**:
   ```bash
   nvidia-smi
   ```
   - GPU-Util should be 90-100%

2. **Check system resources**:
   ```bash
   htop
   ```
   - Press `q` to quit

3. **Possible causes**:
   - CPU bottleneck (need more CPU cores)
   - Slow storage (SSD recommended)
   - Network issues (if model downloading)
   - Too many other processes running

4. **Try**:
   - Close other applications
   - Increase `--dataloader_num_workers` in script
   - Check nothing else is using GPU

### 11.6 Training Crashes Randomly

**Symptoms:**
- Training stops unexpectedly
- No clear error message
- System becomes unresponsive

**Possible causes:**
1. **Insufficient RAM** - Model + data don't fit
2. **GPU overheating** - Check temperatures
3. **Power issues** - GPU needs more power
4. **Driver issues** - Update NVIDIA drivers

**Solutions:**
1. Monitor system: `htop` and `nvidia-smi`
2. Check temperatures stay below 85°C
3. Update drivers:
   ```bash
   ubuntu-drivers autoinstall
   ```

---

## Step 12: VS Code Tips and Shortcuts

### 12.1 Essential Keyboard Shortcuts

**File Operations:**
- `Ctrl + S`: Save file (though auto-save is on)
- `Ctrl + W`: Close current tab
- `Ctrl + P`: Quick file open (type filename)
- `Ctrl + Shift + P`: Command palette (search any command)

**Editor:**
- `Ctrl + F`: Find in current file
- `Ctrl + H`: Find and replace
- `Ctrl + /`: Toggle comment
- `Ctrl + ]`: Indent line
- `Ctrl + [`: Outdent line

**Terminal:**
- `` Ctrl + ` ``: Toggle terminal
- `Ctrl + Shift + 5`: Split terminal
- `Ctrl + C`: Stop current process
- `Ctrl + L`: Clear terminal

**Navigation:**
- `Ctrl + B`: Toggle sidebar
- `Ctrl + J`: Toggle bottom panel
- `Alt + ↑/↓`: Move line up/down
- `Ctrl + D`: Select next occurrence

### 12.2 Useful Features

**Multi-cursor editing:**
1. Hold `Alt` (Windows/Linux) or `Opt` (Mac)
2. Click multiple locations
3. Type once, edits in all places!

**Split editor:**
1. Right-click a file tab
2. Choose "Split Right" or "Split Down"
3. View two files side by side

**Integrated Git:**
1. Click Source Control icon (left sidebar)
2. See changed files
3. Stage, commit, push - all in VS Code!

**Markdown preview:**
1. Open any `.md` file
2. Click preview icon (top right) or press `Ctrl + Shift + V`
3. See formatted version!

### 12.3 Recommended Settings

Open settings:
1. Press `Ctrl + ,` (comma)
2. Search for these settings and enable:

- **Auto Save**: Already done!
- **Format On Save**: Automatically format code
- **Trim Trailing Whitespace**: Clean up extra spaces
- **Files: Insert Final Newline**: Better for Git

### 12.4 Workspace Layout

Save your layout:
1. Arrange windows/panels how you like
2. VS Code remembers per folder
3. Next time you open project, layout is restored!

---

## 🎉 You're All Set!

You now know:
- ✅ How to install and use VS Code
- ✅ How to set up Python environment
- ✅ How to download and prepare dataset
- ✅ How to configure and run training
- ✅ How to monitor training progress
- ✅ How to troubleshoot common issues
- ✅ Useful VS Code tips and tricks

## 📚 Next Steps

While training runs:
1. **Read the documentation**:
   - GETTING_STARTED.md
   - SETUP_AND_TRAINING_GUIDE.md
2. **Monitor progress** occasionally
3. **Plan your evaluation** after training
4. **Prepare for Stage 2** (RL training)

## 🆘 If You Get Stuck

1. **Check the troubleshooting section** above
2. **Review SETUP_AND_TRAINING_GUIDE.md** for detailed help
3. **Look for error messages** - they usually tell you what's wrong
4. **Google the error** - someone likely solved it
5. **Ask for help** - open an issue on GitHub

---

**Good luck with your training!** 🚀

Remember: Training takes time (12-18 hours on 8 GPUs), but the result is worth it!

You're training a medical AI that can reason through complex problems - that's amazing! 🏥🤖
