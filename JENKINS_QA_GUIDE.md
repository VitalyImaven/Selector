# Automation Studio Selector - Jenkins & QA Guide

**Complete Guide for CI/CD and Automated Testing**

Created by: Vitaly Grosman  
Indigo R&D Division  
© 2025

---

## 🎯 Problem Solved

**The Challenge:** You pull a project from Git to Jenkins, and you need to configure it for Automation Studio **without opening the GUI**.

**The Solution:** Use direct paths in CLI - no GUI configuration needed!

---

## 🚀 Quick Start for Jenkins

### **The Magic Command:**

```bash
python main.py -project-path "C:\Jenkins\workspace\MyBuild" -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" -prepare-only -silent
```

**That's it!** No GUI, no pre-configuration, just paths.

---

## 📋 Complete Jenkins Workflow

### **Scenario:**
1. Jenkins pulls your project from Git to `C:\Jenkins\workspace\MyProject`
2. You need to prepare it for AS 4.5
3. Run build/tests
4. No GUI interaction allowed

### **Solution:**

```batch
@echo off
REM Jenkins Build Script

echo ========================================
echo  Automation Studio Build Pipeline
echo ========================================

REM Define paths
set PROJECT_PATH=C:\Jenkins\workspace\MyProject
set AS45_PATH=C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe
set AS6_PATH=C:\Program Files (x86)\BRAutomation\AS6\bin-en\AutomationStudio.exe
set SELECTOR=C:\Tools\AutomationStudioSelector\AutomationStudioSelector.exe

echo.
echo Step 1: Preparing project for AS 4.5...
"%SELECTOR%" -project-path "%PROJECT_PATH%" -studio-path "%AS45_PATH%" -prepare-only -silent

if %errorlevel% neq 0 (
    echo ERROR: Failed to prepare project
    exit /b 1
)

echo ✓ Project prepared successfully

echo.
echo Step 2: Project is ready for build
echo   Project: %PROJECT_PATH%
echo   OCB.apj configured for AS 4.5
echo   Libraries copied from Libraries_45
echo   Physical.pkg updated

REM Now your build tools can work with the prepared project
REM Add your build/test commands here

exit /b 0
```

---

## 🔧 Direct Path Usage

### **Two Ways to Use CLI:**

#### **Method 1: With GUI Configuration (Traditional)**
```bash
# First configure in GUI (one time setup)
# Then use project names in CLI

python main.py OCB AS45
```

#### **Method 2: Direct Paths (Jenkins/QA)**
```bash
# No GUI configuration needed!
# Just use full paths

python main.py -project-path "C:\Path\To\Project" -studio-path "C:\Path\To\AS.exe" -prepare-only
```

### **Direct Path Parameters:**

| Parameter | Short | Description | Example |
|-----------|-------|-------------|---------|
| `-project-path` | `-path` | Full path to project directory | `C:\Jenkins\workspace\MyProject` |
| `-studio-path` | `-as-path` | Full path to AS executable | `C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe` |

---

## 💼 Real QA/Jenkins Scenarios

### **Scenario 1: Simple Jenkins Build**

**Jenkins Execute Windows batch command:**
```batch
REM Prepare project
python C:\Tools\Selector\main.py ^
  -project-path "%WORKSPACE%" ^
  -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" ^
  -prepare-only ^
  -silent

if errorlevel 1 exit /b 1

REM Project is now ready for your build tools
```

### **Scenario 2: Multi-Version Testing**

**Test with both AS 4.5 and AS 6:**

```batch
@echo off
set PROJECT=%WORKSPACE%
set SELECTOR=C:\Tools\Selector\main.py

echo Testing with AS 4.5...
python %SELECTOR% -project-path "%PROJECT%" -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" -prepare-only -silent
if errorlevel 1 goto AS45_FAILED

echo ✓ AS 4.5 configuration successful
REM Run your AS 4.5 tests here

echo.
echo Testing with AS 6...
python %SELECTOR% -project-path "%PROJECT%" -studio-path "C:\Program Files (x86)\BRAutomation\AS6\bin-en\AutomationStudio.exe" -prepare-only -silent
if errorlevel 1 goto AS6_FAILED

echo ✓ AS 6 configuration successful
REM Run your AS 6 tests here

echo.
echo ✓ All tests passed!
exit /b 0

:AS45_FAILED
echo ✗ AS 4.5 configuration failed
exit /b 1

:AS6_FAILED
echo ✗ AS 6 configuration failed
exit /b 1
```

### **Scenario 3: Git Pull + Auto-Configure**

**Complete workflow from Git to ready project:**

```batch
@echo off
REM git_build_workflow.bat

echo ========================================
echo  Git Build Workflow
echo ========================================

REM Step 1: Pull latest code
echo Step 1: Pulling from Git...
cd C:\Builds\MyProject
git pull origin main
if errorlevel 1 (
    echo ERROR: Git pull failed
    exit /b 1
)

REM Step 2: Prepare for AS 4.5
echo.
echo Step 2: Configuring for AS 4.5...
python C:\Tools\Selector\main.py ^
  -project-path "C:\Builds\MyProject" ^
  -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" ^
  -prepare-only ^
  -silent

if errorlevel 1 (
    echo ERROR: Project preparation failed
    exit /b 1
)

REM Step 3: Your build/test commands
echo.
echo Step 3: Running builds and tests...
REM Add your build commands here

echo.
echo ========================================
echo  Build completed successfully!
echo ========================================
```

### **Scenario 4: Nightly Build with Multiple Projects**

**Prepare multiple projects from different Git repos:**

```batch
@echo off
REM nightly_build.bat

echo ========================================
echo  Nightly Build Process
echo  Started: %DATE% %TIME%
echo ========================================

set SELECTOR=C:\Tools\Selector\main.py
set AS45=C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe

REM Project 1
echo.
echo [Project 1] Pulling from Git...
cd C:\Builds\Project1
git pull origin main
echo [Project 1] Preparing for AS 4.5...
python %SELECTOR% -project-path "C:\Builds\Project1" -studio-path "%AS45%" -prepare-only -silent
if errorlevel 1 echo [Project 1] ✗ FAILED & goto END
echo [Project 1] ✓ SUCCESS

REM Project 2
echo.
echo [Project 2] Pulling from Git...
cd C:\Builds\Project2
git pull origin main
echo [Project 2] Preparing for AS 4.5...
python %SELECTOR% -project-path "C:\Builds\Project2" -studio-path "%AS45%" -prepare-only -silent
if errorlevel 1 echo [Project 2] ✗ FAILED & goto END
echo [Project 2] ✓ SUCCESS

REM Project 3
echo.
echo [Project 3] Pulling from Git...
cd C:\Builds\Project3
git pull origin main
echo [Project 3] Preparing for AS 4.5...
python %SELECTOR% -project-path "C:\Builds\Project3" -studio-path "%AS45%" -prepare-only -silent
if errorlevel 1 echo [Project 3] ✗ FAILED & goto END
echo [Project 3] ✓ SUCCESS

echo.
echo ========================================
echo  All projects built successfully!
echo  Completed: %DATE% %TIME%
echo ========================================

:END
```

---

## 🔧 Jenkins Configuration

### **Jenkins Job Setup:**

#### **1. Source Code Management:**
- **Git Repository**: Your project repository URL
- **Branch**: main/master
- **Checkout to**: `${WORKSPACE}`

#### **2. Build Environment:**
- **Delete workspace before build**: Recommended for clean builds

#### **3. Build Steps (Windows Batch):**

```batch
@echo off
echo Configuring project for Automation Studio...

REM Use Jenkins workspace variable
python C:\Tools\AutomationStudioSelector\main.py ^
  -project-path "%WORKSPACE%" ^
  -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" ^
  -prepare-only ^
  -silent

REM Check result
if %errorlevel% neq 0 (
    echo FAILED: Project preparation failed
    exit /b 1
)

echo SUCCESS: Project prepared for AS 4.5
echo Project ready at: %WORKSPACE%\OCB.apj

REM Continue with your build/test steps...
```

#### **4. Post-Build Actions:**
- **Archive artifacts**: `OCB.apj`, `Physical.pkg`, etc.
- **Publish test results**: Your test outputs
- **Email notifications**: On build success/failure

---

## 🎯 PowerShell Version (For Modern CI/CD)

### **PowerShell Script for Jenkins:**

```powershell
# jenkins_build.ps1

param(
    [string]$ProjectPath = $env:WORKSPACE,
    [string]$ASVersion = "45"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Automation Studio Build Pipeline" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Define paths
$SelectorPath = "C:\Tools\Selector\main.py"
$AS45Path = "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe"
$AS6Path = "C:\Program Files (x86)\BRAutomation\AS6\bin-en\AutomationStudio.exe"

# Select AS version
$ASPath = if ($ASVersion -eq "45") { $AS45Path } else { $AS6Path }

Write-Host "Project Path: $ProjectPath" -ForegroundColor Yellow
Write-Host "AS Version: $ASVersion" -ForegroundColor Yellow
Write-Host ""

# Prepare project
Write-Host "Preparing project..." -ForegroundColor White
python $SelectorPath `
  -project-path "$ProjectPath" `
  -studio-path "$ASPath" `
  -prepare-only `
  -silent

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Project preparation failed" -ForegroundColor Red
    exit 1
}

Write-Host "SUCCESS: Project prepared for AS $ASVersion" -ForegroundColor Green
Write-Host ""

# Continue with build/tests
Write-Host "Project ready for build operations" -ForegroundColor Green
exit 0
```

**Usage in Jenkins:**
```bash
powershell -ExecutionPolicy Bypass -File jenkins_build.ps1 -ASVersion "45"
```

---

## 📊 Complete Examples

### **Example 1: Fresh Git Clone to Ready Project**

```batch
@echo off
REM fresh_clone_to_ready.bat
REM Complete workflow from nothing to ready project

echo ========================================
echo  Complete Setup from Git Clone
echo ========================================

REM Step 1: Clone repository
echo Step 1: Cloning repository...
cd C:\Temp
git clone https://your-repo.git MyProject
cd MyProject

REM Step 2: Configure for AS 4.5
echo.
echo Step 2: Configuring for AS 4.5...
python C:\Tools\Selector\main.py ^
  -project-path "C:\Temp\MyProject" ^
  -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" ^
  -prepare-only ^
  -verbose

if errorlevel 1 (
    echo ERROR: Configuration failed
    exit /b 1
)

REM Step 3: Project is ready
echo.
echo ✓ Project is ready to use!
echo   Location: C:\Temp\MyProject\OCB.apj
echo   Configured for: AS 4.5
echo.
echo You can now:
echo   1. Double-click C:\Temp\MyProject\OCB.apj to open in AS 4.5
echo   2. Run your build/test tools on the project
echo   3. Make changes and commit back to Git

pause
```

### **Example 2: Automated Nightly Build**

```batch
@echo off
REM nightly_build.bat
REM Schedule this with Windows Task Scheduler

set LOG_FILE=C:\Logs\nightly_build_%DATE:~-4,4%%DATE:~-10,2%%DATE:~-7,2%.log

echo ======================================== >> %LOG_FILE%
echo Nightly Build Started: %DATE% %TIME% >> %LOG_FILE%
echo ======================================== >> %LOG_FILE%

REM Pull latest code
cd C:\Projects\Production
git pull origin main >> %LOG_FILE% 2>&1

REM Prepare for AS 4.5
python C:\Tools\Selector\main.py ^
  -project-path "C:\Projects\Production" ^
  -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" ^
  -prepare-only ^
  -silent

if errorlevel 1 (
    echo ERROR: Build preparation failed >> %LOG_FILE%
    REM Send email alert
    exit /b 1
)

echo Success: Project prepared >> %LOG_FILE%

REM Add your build commands here

echo Build completed: %DATE% %TIME% >> %LOG_FILE%
```

### **Example 3: Multi-Branch Testing**

```batch
@echo off
REM test_all_branches.bat
REM Test multiple Git branches

set BASE_DIR=C:\Builds
set SELECTOR=python C:\Tools\Selector\main.py
set AS45=C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe

for %%B in (main develop feature-new-plc) do (
    echo.
    echo ========================================
    echo  Testing branch: %%B
    echo ========================================
    
    REM Clone branch
    cd %BASE_DIR%
    if exist %%B rd /s /q %%B
    git clone -b %%B https://your-repo.git %%B
    
    REM Prepare project
    %SELECTOR% -project-path "%BASE_DIR%\%%B" -studio-path "%AS45%" -prepare-only -silent
    
    if errorlevel 1 (
        echo [%%B] ✗ FAILED
    ) else (
        echo [%%B] ✓ PASSED
        REM Run tests here
    )
)

echo.
echo All branches tested
```

---

## 🎯 Command Syntax for Jenkins

### **Minimum Required Command:**

```bash
python main.py -project-path "PATH_TO_PROJECT" -studio-path "PATH_TO_AS_EXE" -prepare-only
```

### **Full Command with All Options:**

```bash
python main.py ^
  -project-path "C:\Jenkins\workspace\MyProject" ^
  -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" ^
  -prepare-only ^
  -silent ^
  -verbose
```

### **Common AS Executable Paths:**

**AS 4.5:**
```
C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe
C:\BrAutomation\AS410\Bin-en\AutomationStudio.exe
```

**AS 6:**
```
C:\Program Files (x86)\BRAutomation\AS6\bin-en\AutomationStudio.exe
C:\Program Files\BRAutomation\AS60\bin-en\AutomationStudio.exe
```

---

## 🔄 Different Build Server Scenarios

### **Scenario A: Fixed AS Version**

**You always use AS 4.5:**

```batch
REM Simple - hardcode everything
python main.py ^
  -project-path "%WORKSPACE%" ^
  -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" ^
  -prepare-only ^
  -silent
```

### **Scenario B: Parameterized Builds**

**Jenkins Build with Parameters:**

1. **Add String Parameter**: `AS_VERSION` (values: `45` or `6`)
2. **Use in script**:

```batch
@echo off
if "%AS_VERSION%"=="45" (
    set AS_PATH=C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe
) else (
    set AS_PATH=C:\Program Files (x86)\BRAutomation\AS6\bin-en\AutomationStudio.exe
)

python main.py ^
  -project-path "%WORKSPACE%" ^
  -studio-path "%AS_PATH%" ^
  -prepare-only ^
  -silent
```

### **Scenario C: Version from Git Tag/Branch**

**Automatically select AS version based on Git branch:**

```batch
@echo off
REM Get current branch name
for /f %%i in ('git rev-parse --abbrev-ref HEAD') do set BRANCH=%%i

REM Determine AS version from branch
if "%BRANCH%"=="as6-development" (
    set AS_PATH=C:\Program Files (x86)\BRAutomation\AS6\bin-en\AutomationStudio.exe
) else (
    set AS_PATH=C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe
)

echo Branch: %BRANCH%
echo Using AS: %AS_PATH%

python main.py -project-path "%CD%" -studio-path "%AS_PATH%" -prepare-only -silent
```

---

## 🎛️ Advanced Configurations

### **Environment Variables Setup:**

**Create `jenkins_env.bat`:**
```batch
@echo off
REM jenkins_env.bat - Set up environment variables

set SELECTOR_CLI=python C:\Tools\AutomationStudioSelector\main.py
set AS45_EXE=C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe
set AS6_EXE=C:\Program Files (x86)\BRAutomation\AS6\bin-en\AutomationStudio.exe
set BUILD_ROOT=C:\Jenkins\workspace

echo Jenkins environment configured
```

**Use in builds:**
```batch
@echo off
call jenkins_env.bat

%SELECTOR_CLI% -project-path "%BUILD_ROOT%\MyProject" -studio-path "%AS45_EXE%" -prepare-only -silent
```

### **PowerShell Function:**

```powershell
# automation_functions.ps1

function Prepare-ASProject {
    param(
        [string]$ProjectPath,
        [string]$ASVersion = "45"
    )
    
    $SelectorPath = "C:\Tools\Selector\main.py"
    $AS45 = "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe"
    $AS6 = "C:\Program Files (x86)\BRAutomation\AS6\bin-en\AutomationStudio.exe"
    
    $ASPath = if ($ASVersion -eq "45") { $AS45 } else { $AS6 }
    
    python $SelectorPath `
      -project-path $ProjectPath `
      -studio-path $ASPath `
      -prepare-only `
      -silent
    
    return $LASTEXITCODE -eq 0
}

# Usage:
# Prepare-ASProject -ProjectPath "C:\Builds\MyProject" -ASVersion "45"
```

---

## 🐛 Troubleshooting Jenkins Builds

### **Issue: "Python not found"**

**Solution:**
```batch
REM Use full Python path
C:\Python313\python.exe C:\Tools\Selector\main.py ...

REM Or add Python to Jenkins PATH
set PATH=C:\Python313;%PATH%
python main.py ...
```

### **Issue: "Project structure validation failed"**

**Checklist:**
- ✓ Project has `Logical` folder?
- ✓ Project has `Physical` folder?
- ✓ Project has `Libraries_45` or `Libraries_6` folders?
- ✓ Project has `Physical_45.pkg` or `Physical_6.pkg` files?
- ✓ Project has `OCB_as45.apj` or `OCB_as6.apj` files?

**Fix:**
```batch
REM Verify structure before running
dir "%WORKSPACE%\Logical"
dir "%WORKSPACE%\Physical"

REM Then run selector
python main.py -project-path "%WORKSPACE%" -studio-path "..." -prepare-only -verbose
```

### **Issue: "Permission denied"**

**Solution:**
```batch
REM Run as administrator or ensure Jenkins service has proper permissions
REM Check folder permissions

icacls "%WORKSPACE%" /grant Jenkins:(OI)(CI)F /T
```

---

## 📝 Complete Jenkins Pipeline Example

**Jenkinsfile (Declarative Pipeline):**

```groovy
pipeline {
    agent any
    
    parameters {
        choice(name: 'AS_VERSION', choices: ['45', '6'], description: 'Automation Studio Version')
    }
    
    environment {
        SELECTOR = 'C:\\Tools\\Selector\\main.py'
        AS45_PATH = 'C:\\BrAutomation\\AS45\\Bin-en\\AutomationStudio.exe'
        AS6_PATH = 'C:\\Program Files (x86)\\BRAutomation\\AS6\\bin-en\\AutomationStudio.exe'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://your-repo.git'
            }
        }
        
        stage('Configure AS Project') {
            steps {
                script {
                    def asPath = params.AS_VERSION == '45' ? env.AS45_PATH : env.AS6_PATH
                    
                    bat """
                        python ${env.SELECTOR} ^
                          -project-path "${env.WORKSPACE}" ^
                          -studio-path "${asPath}" ^
                          -prepare-only ^
                          -silent
                    """
                }
            }
        }
        
        stage('Build') {
            steps {
                echo 'Project configured and ready for build'
                // Add your build steps here
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running tests'
                // Add your test steps here
            }
        }
    }
    
    post {
        success {
            echo 'Build completed successfully!'
        }
        failure {
            echo 'Build failed!'
        }
    }
}
```

---

## ✅ Quick Start Checklist for QA/Jenkins

### **One-Time Setup:**
1. ☐ Install Automation Studio Selector on build server
2. ☐ Install Automation Studio (4.5 and/or 6) on build server
3. ☐ Note the paths to AS executables
4. ☐ Test CLI manually first

### **For Each Build:**
1. ☐ Git pull to workspace
2. ☐ Run selector CLI with `-project-path` and `-studio-path`
3. ☐ Use `-prepare-only` flag
4. ☐ Use `-silent` flag for clean logs
5. ☐ Check exit code
6. ☐ Proceed with build/tests

### **Test Command:**
```bash
python main.py -project-path "C:\Test\Project" -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" -prepare-only -verbose
```

---

## 🎯 Summary

### **The Key Insight:**

**You DON'T need GUI configuration for Jenkins/QA!**

Just use direct paths:
- `-project-path` instead of project name
- `-studio-path` instead of studio version

### **Jenkins Command Template:**

```batch
python main.py ^
  -project-path "%WORKSPACE%" ^
  -studio-path "C:\BrAutomation\AS45\Bin-en\AutomationStudio.exe" ^
  -prepare-only ^
  -silent
```

### **Benefits:**
- ✅ **No GUI needed** - Fully automated
- ✅ **No pre-configuration** - Works on fresh machines
- ✅ **Portable** - Same script works on any build server
- ✅ **Version control** - Paths in script are documented
- ✅ **CI/CD ready** - Perfect for Jenkins, TeamCity, Azure DevOps

---

**Created by Vitaly Grosman - Indigo R&D Division**

For more CLI options, see: CLI_TUTORIAL.md

