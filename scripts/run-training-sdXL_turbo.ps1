#pazi da poženesš s  kohya venvom!!!
cd C:\Users\umzg\Documents\Projektil\kohya_ss\sd-scripts\venv\Scripts
& .\Activate.ps1

do {
    $baseDir = Read-Host "vnsesi pot do mape z dataseti"

    if (-not (Test-Path -Path $baseDir)) {
        Write-Host "vnesli ste napacno pot do mape, poskusite znova." -ForegroundColor Red
    }

} while (-not (Test-Path -Path $baseDir))

Write-Host "vnesli ste  $baseDir" -ForegroundColor DarkGreen -BackgroundColor White
$directories = Get-ChildItem -Path $baseDir -Directory

foreach ($dir in $directories) {
    $datasetPath = $dir.FullName
    $outputName = $dir.Name

    Write-Host "Starting training for dataset: $outputName"

    $command = @"
accelerate launch --num_cpu_threads_per_process=1 "C:\Users\umzg\Documents\Projektil\kohya_ss\sd-scripts\sdxl_train.py" ``
--pretrained_model_name_or_path="C:\Users\umzg\Documents\Projektil\kohya_ss\sd-scripts\training_models\sdXL_v10VAEFix.safetensors" ``
--train_data_dir="$datasetPath" ``
--output_dir="output" ``
--output_name="$outputName" ``
--save_model_as="safetensors" ``
--train_batch_size=1 ``
--max_train_steps=1000 ``
--save_every_n_steps=250 ``
--optimizer_type="adafactor" ``
--optimizer_args scale_parameter=False relative_step=False warmup_init=False ``
--xformers ``
--cache_latents ``
--lr_scheduler="constant_with_warmup" ``
--lr_warmup_steps=100 ``
--learning_rate=1e-5 ``
--max_grad_norm=0.0 ``
--resolution="1024,1024" ``
--save_precision="fp16" ``
--save_n_epoch_ratio=1 ``
--max_data_loader_n_workers=1 ``
--persistent_data_loader_workers ``
--mixed_precision="fp16" ``
--logging_dir="logs" ``
--log_prefix="last" ``
--gradient_checkpointing ``
--sample_sampler="ddim" ``
--cache_latents ``
--cache_latents_to_disk ``
--no_half_vae``
--enable_xformers_memory_efficient_attention ``
--caption_extension =".txt"
"@

    Invoke-Expression -Command $command

    Write-Host "Finished training for dataset: $outputName"
    Write-Host "------------------------------------"
}

#added xformers memory efficient attention
#added 
Write-Host "Vsi modeli ustvarjeni"