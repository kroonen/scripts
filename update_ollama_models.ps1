# Fetch the list of models dynamically using `ollama list`
$models = ollama list

# Convert the result into an array of lines
$modelsArray = $models -split "`n"

# Initialize an array to store model names
$modelNames = @()

# Loop through each line and extract the model name
foreach ($line in $modelsArray) {
    $modelName = $line -split "\s+" | Select-Object -First 1
    
    # Filter out any lines that don't look like a valid model name
    if ($modelName -and $modelName -ne "NAME") {
        $modelNames += $modelName
    }
}

# Initialize progress bar variables
$totalModels = $modelNames.Count
$currentModelIndex = 0

# Loop through each model name and attempt to update it
foreach ($model in $modelNames) {
    $currentModelIndex++
    
    # Update the status bar dynamically with the model name and progress
    $percentComplete = ($currentModelIndex / $totalModels) * 100
    Write-Progress -Activity "Updating Ollama Models" `
                   -Status "Processing model $model" `
                   -PercentComplete $percentComplete

    Write-Host "Updating model: $model"
    try {
        # Pull the model
        ollama pull $model

        # Check if the pull command was successful
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Successfully updated $model"
        } else {
            Write-Host "Failed to update $model"
        }
    } catch {
        Write-Host "An error occurred while updating $model"
    }
}

# Completion message
Write-Progress -Activity "Updating Ollama Models" `
               -Status "All updates completed" `
               -Completed

Write-Host "All updates completed."
