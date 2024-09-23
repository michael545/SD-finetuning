$trainingSetFolder = "C:\Users\umzg\Documents\Projektil\clip_generated_training_set"
$outputBaseDir = "C:\Users\umzg\Documents\Projektil\dreambooth_output\test_dir"
$modelVersion = "stabilityai/stable-diffusion-xl-base-1.0"
$vaePATH = "stabilityai/sdxl-vae"
# Iterate through each folder in the training set folder
Get-ChildItem -Directory -Path $trainingSetFolder | ForEach-Object {
    $datasetPath = $_.FullName
    $outputDir = Join-Path $outputBaseDir $_.Name

    if (-not (Test-Path -Path $outputDir)) {
    Write-Host "Creating output directory: $outputDir" -ForegroundColor Cyan
    New-Item -Path $outputDir -ItemType Directory | Out-Null
    }
    $command = @(
        "accelerate", "launch",
       # "python"
        "C:\Users\umzg\Documents\Projektil\diffusers\examples\dreambooth\train_dreambooth_lora_sdxl.py",
        "--pretrained_model_name_or_path", "$modelVersion",
        "--pretrained_vae_model_name_or_path", "$vaePATH",
        "--instance_data_dir", "$datasetPath",
        "--output_dir", "$outputDir",
        "--instance_prompt", "painting",
        "--resolution", "1024",
        "--train_batch_size", "1",
        "--gradient_accumulation_steps", "1",
        "--learning_rate", "5e-06",
        "--lr_scheduler", "constant",
        "--lr_warmup_steps", "50",
        "--max_train_steps", "1000",
       "--mixed_precision", "fp16",
        "--use_8bit_adam"
        #"--enable_xformers_memory_efficient_attention"
    )
    
    # Join the command arguments into a single string
    $commandString = $command -join " "
    
    # Run the command
    Write-Host "Running training for $datasetPath" -ForegroundColor green
    Write-Host $commandString  -ForegroundColor red -BackgroundColor white
    Invoke-Expression $commandString
}