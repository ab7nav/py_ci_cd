import os
import subprocess
import sys

REPO_URL = "https://github.com/ab7nav/py_ci_cd.git"  # The repo URL
REPO_DIR = "./py_ci_cd"  # The project repo
SCRIPT_NAME = "ci_cd_pipeline.py"
EXECUTABLE_NAME = "ci_cd_pipeline"
DIST_DIR = os.path.join(REPO_DIR, "dist")

def clone_or_pull_repo():
    if not os.path.exists(REPO_DIR):
        print("Cloning repository")
        subprocess.run(["git", "clone", REPO_URL, REPO_DIR], check=True)
    else:
        print("Pulling latest changes..")
        subprocess.run(["git", "-C", REPO_DIR, "pull"], check=True)

def build_executable():
    print("Building executable")
    subprocess.run(["pyinstaller", "--onefile", os.path.join(REPO_DIR, SCRIPT_NAME)], check=True)

def run_tests():
    executable_path = os.path.join(DIST_DIR, EXECUTABLE_NAME)
    print(executable_path)
    if not os.path.exists(executable_path):
        print("ERROR: Executable not found. Build may have failed")
        return False
    
    test_csv = os.path.join(REPO_DIR, "sample.csv")
    test_column = "Sales"
    print("Running test in executable")
    
    try:
        result = subprocess.run([executable_path, test_csv, test_column], capture_output=True, text=True)
        print("Test output: \n", result.stdout)
        
        if "Total sum " in result.stdout:
            print("Test passed!! ")
            return True
        else:
            print("Test failed. The output does not match expected format")
            return False
    except Exception as e:
        print(f"The test failed with the exception: {e}")
        return False

def clean_up():
    print("Cleaning up build artifacts...")
    if os.path.exists(os.path.join(REPO_DIR, "build")):
        subprocess.run(["rm", "-rf", os.path.join(REPO_DIR, "build")])
    if os.path.exists(DIST_DIR):
        subprocess.run(["rm", "-rf", DIST_DIR])
    if os.path.exists(os.path.join(REPO_DIR, EXECUTABLE_NAME + ".spec")):
        subprocess.run(["rm", os.path.join(REPO_DIR, EXECUTABLE_NAME + ".spec")])

def main():
    try:
        clone_or_pull_repo()
        build_executable()
        if run_tests():
            print("CI/CD pipeline executed successfully!")
        else:
            print("CI/CD pipeline failed in testing!")
    except subprocess.CalledProcessError as e:
        print(f"Error: A subprocess command failed with the following message:\n{e}")
    finally:
        clean_up()

if __name__ == "__main__":
    main()

