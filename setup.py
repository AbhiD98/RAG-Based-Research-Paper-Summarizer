import os
import subprocess
import sys

def check_pip():
    """Check if pip is available"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"], stdout=subprocess.DEVNULL)
        return True
    except:
        return False

def install_requirements():
    """Install required packages"""
    if not check_pip():
        print("❌ pip not found in current Python installation")
        print("\n💡 Solutions:")
        print("1. Use regular Python instead of MSYS2:")
        print("   - Download from https://python.org")
        print("   - Or use: py -m pip install -r requirements.txt")
        print("\n2. Install pip in MSYS2:")
        print("   pacman -S mingw-w64-ucrt-x86_64-python-pip")
        print("\n3. Manual installation:")
        print("   pip install streamlit boto3 PyPDF2 numpy scikit-learn")
        return False
    
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    return True

def setup_aws_credentials():
    """Guide user to set up AWS credentials"""
    print("\n🔧 AWS Setup Required:")
    print("1. Set environment variables:")
    print("   set AWS_ACCESS_KEY_ID=your_access_key")
    print("   set AWS_SECRET_ACCESS_KEY=your_secret_key")
    print("\n2. Or configure AWS CLI:")
    print("   aws configure")
    print("\n3. Ensure your AWS account has Bedrock access to Claude Sonnet")

def main():
    print("🚀 Setting up Research Paper Q&A System...")
    
    if install_requirements():
        print("✅ Dependencies installed successfully!")
        setup_aws_credentials()
        print("\n🎉 Setup complete!")
        print("\nTo run the application:")
        print("streamlit run app.py")
    else:
        print("\n⚠️  Please install dependencies manually and run again")

if __name__ == "__main__":
    main()