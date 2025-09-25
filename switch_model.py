#!/usr/bin/env python3
"""
Easy Model Switcher for SmartWebBot
Usage: python switch_model.py [fast|accurate]
"""

import sys
import requests

def switch_model(model_type):
    """Switch the AI model via API"""
    
    if model_type not in ['fast', 'accurate']:
        print("❌ Error: Model type must be 'fast' or 'accurate'")
        print("Usage: python switch_model.py [fast|accurate]")
        return False
    
    try:
        # API endpoint
        url = "http://127.0.0.1:8000/api/intelligent-chat/switch-model"
        
        # Make the request
        response = requests.post(f"{url}?model_type={model_type}", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['message']}")
            print(f"📊 Benefits: {data['benefits']}")
            return True
        else:
            print(f"❌ Failed to switch model: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Server not running. Start your backend server first!")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def get_current_model():
    """Get current model information"""
    
    try:
        url = "http://127.0.0.1:8000/api/intelligent-chat/current-model"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            current = data['current_model']
            info = data['model_info']
            
            print(f"🔍 Current Model: {current}")
            print(f"📝 Type: {info['type']}")
            print(f"💡 Description: {info['description']}")
            print(f"💾 Size: {info['size']}")
            
            print(f"\n🔄 Available Models:")
            for model_name, model_info in data['available_models'].items():
                indicator = "👉" if model_name == current else "  "
                print(f"{indicator} {model_name} ({model_info['type']}) - {model_info['description']}")
            
            return True
        else:
            print(f"❌ Failed to get current model: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Server not running. Start your backend server first!")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🤖 SmartWebBot Model Switcher")
    print("=" * 40)
    
    if len(sys.argv) == 1:
        # No arguments - show current model
        get_current_model()
        print(f"\n💡 Usage: python {sys.argv[0]} [fast|accurate]")
        
    elif len(sys.argv) == 2:
        model_type = sys.argv[1].lower()
        
        if model_type in ['status', 'current', 'info']:
            get_current_model()
        else:
            print(f"🔄 Switching to {model_type} model...")
            if switch_model(model_type):
                print("🎉 Model switched successfully!")
                print("ℹ️  You can now test the faster/more accurate responses!")
            else:
                print("❌ Model switch failed. Check server logs.")
    else:
        print("❌ Usage: python switch_model.py [fast|accurate|status]")
        sys.exit(1)

if __name__ == "__main__":
    main()
