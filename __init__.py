from back.createapp import create_app
from back.patch_update import new_patch_new_json


# Check for updates before creating the app
new_patch_new_json()

# Launching the app
app = create_app()

if __name__ == '__main__':
    app.run()
