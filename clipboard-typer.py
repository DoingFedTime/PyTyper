import keyboard
import pyperclip
import time
import threading
import random
import tkinter as tk
from tkinter import ttk
import json
import os

class ClipboardTyper:
    def __init__(self):
        self.typing = False
        
        # Default settings - these are fallback values only
        self.settings = {
            'min_delay': 0.05,
            'max_delay': 0.15,
            'start_delay': 0.5,
            'hotkey': 'ctrl+shift+t',
            'stop_key': 'esc',
            'theme': 'light'
        }
        
        print("Starting ClipboardTyper...")
        
        # Theme colors
        self.themes = {
            'light': {
                'bg': '#f0f0f0',
                'fg': '#000000',
                'button': '#e0e0e0',
                'highlight': '#0078d7',
                'frame': '#e9e9e9'
            },
            'dark': {
                'bg': '#2d2d2d',
                'fg': '#ffffff',
                'button': '#3d3d3d',
                'highlight': '#0078d7',
                'frame': '#383838'
            },
            'hacker': {
                'bg': '#0a0a0a',
                'fg': '#00ff41',  # Matrix green
                'button': '#222222',
                'highlight': '#9600ff',  # Cyberpunk purple
                'frame': '#1a1a1a'
            }
        }
        
        # Load settings BEFORE creating GUI
        self.load_settings()
        
        # Create the GUI - this creates the variables and entry fields
        self.create_gui()
        
        # Register hotkeys AFTER GUI is created and populated
        self.register_hotkeys()
    
    def load_settings(self):
        """Load settings from a JSON file if it exists."""
        settings_file = 'clipboard_typer_settings.json'
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    
                    print(f"Settings loaded from file: {loaded_settings}")
                    
                    # Check for required keys
                    required_keys = ['hotkey', 'stop_key', 'min_delay', 'max_delay']
                    missing_keys = [key for key in required_keys if key not in loaded_settings]
                    
                    if missing_keys:
                        print(f"Warning: Missing required keys in settings file: {missing_keys}")
                    else:
                        # Update settings
                        self.settings.update(loaded_settings)
                        print(f"Applied settings: {self.settings}")
            except Exception as e:
                print(f"Error loading settings from {settings_file}: {e}")
        else:
            print(f"Settings file {settings_file} not found. Using defaults: {self.settings}")
    
    def register_hotkeys(self):
        """Register hotkeys with proper error handling."""
        # First, completely unhook ALL keyboard hooks
        try:
            keyboard.unhook_all()
            print("Unhooked all keyboard hooks for clean registration")
        except Exception as e:
            print(f"Error unhooking all keys: {e}")
            
        # Now register the hotkeys
        try:
            print(f"Registering main hotkey: {self.settings['hotkey']}")
            # Make sure hotkey is valid
            if not self.settings['hotkey'] or '+' not in self.settings['hotkey']:
                print("Invalid hotkey format, defaulting to ctrl+shift+t")
                self.settings['hotkey'] = 'ctrl+shift+t'
                
            # Register the hotkey with direct function reference and ensure it's suppressed
            keyboard.add_hotkey(self.settings['hotkey'], self.toggle_typing, suppress=True)
            print(f"Successfully registered hotkey '{self.settings['hotkey']}' with toggle_typing function")
            self.status_var.set(f"Hotkey '{self.settings['hotkey']}' registered")
        except Exception as e:
            print(f"Error registering hotkey: {e}")
            self.status_var.set(f"Error registering hotkey: {str(e)}")
            
        try:
            print(f"Registering stop key: {self.settings['stop_key']}")
            keyboard.add_hotkey(self.settings['stop_key'], self.stop_typing, suppress=True)
            print(f"Successfully registered stop key '{self.settings['stop_key']}' with stop_typing function")
        except Exception as e:
            print(f"Error registering stop key: {e}")
            self.status_var.set(f"Error registering stop key: {str(e)}")
            
    def save_settings(self):
        """Save current settings to a JSON file."""
        settings_file = 'clipboard_typer_settings.json'
        try:
            # Make a copy of settings for writing to file to avoid race conditions
            settings_to_save = self.settings.copy()
            
            print(f"Saving settings to file: {settings_to_save}")
            
            with open(settings_file, 'w') as f:
                json.dump(settings_to_save, f)
                
            print(f"Settings saved successfully to {settings_file}")
        except Exception as e:
            print(f"Error saving settings: {e}")
            self.status_var.set(f"Error saving settings: {str(e)}")
    
    def create_gui(self):
        """Create the GUI for the application."""
        self.root = tk.Tk()
        self.root.title("Clipboard Typing Simulator")
        self.root.geometry("400x450")  # Increase height to ensure buttons are visible
        self.root.resizable(False, False)
        
        # Create a style object
        self.style = ttk.Style()
        
        # Status variable needs to be created early for error messages
        self.status_var = tk.StringVar(value="Ready")
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initialize theme variable
        self.theme_var = tk.StringVar(value=self.settings['theme'])
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Clipboard Typing Simulator", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Typing speed frame
        speed_frame = ttk.LabelFrame(main_frame, text="Typing Speed (seconds)")
        speed_frame.pack(fill=tk.X, pady=10)
        
        # Min delay
        min_delay_frame = ttk.Frame(speed_frame)
        min_delay_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(min_delay_frame, text="Min Delay:").pack(side=tk.LEFT)
        
        self.min_delay_var = tk.StringVar(value=str(self.settings['min_delay']))
        min_delay_entry = ttk.Entry(min_delay_frame, textvariable=self.min_delay_var, width=8)
        min_delay_entry.pack(side=tk.LEFT, padx=5)
        
        # Max delay
        max_delay_frame = ttk.Frame(speed_frame)
        max_delay_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(max_delay_frame, text="Max Delay:").pack(side=tk.LEFT)
        
        self.max_delay_var = tk.StringVar(value=str(self.settings['max_delay']))
        max_delay_entry = ttk.Entry(max_delay_frame, textvariable=self.max_delay_var, width=8)
        max_delay_entry.pack(side=tk.LEFT, padx=5)
        
        # Initial delay before typing starts
        start_delay_frame = ttk.Frame(speed_frame)
        start_delay_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(start_delay_frame, text="Start Delay:").pack(side=tk.LEFT)
        
        # Add start_delay to settings if it doesn't exist
        if 'start_delay' not in self.settings:
            self.settings['start_delay'] = 0.5
            
        self.start_delay_var = tk.StringVar(value=str(self.settings['start_delay']))
        start_delay_entry = ttk.Entry(start_delay_frame, textvariable=self.start_delay_var, width=8)
        start_delay_entry.pack(side=tk.LEFT, padx=5)
        
        # Hotkey frame
        hotkey_frame = ttk.LabelFrame(main_frame, text="Hotkeys")
        hotkey_frame.pack(fill=tk.X, pady=10)
        
        # Start/stop hotkey
        start_hotkey_frame = ttk.Frame(hotkey_frame)
        start_hotkey_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(start_hotkey_frame, text="Start/Stop:").pack(side=tk.LEFT)
        
        # Make sure hotkey string is loaded from settings
        self.hotkey_var = tk.StringVar(value=self.settings['hotkey'])
        print(f"Setting hotkey entry to: {self.settings['hotkey']}")
        self.hotkey_entry = ttk.Entry(start_hotkey_frame, textvariable=self.hotkey_var, width=15)
        self.hotkey_entry.pack(side=tk.LEFT, padx=5)
        
        self.record_hotkey_btn = ttk.Button(
            start_hotkey_frame, 
            text="Record", 
            command=self.record_hotkey
        )
        self.record_hotkey_btn.pack(side=tk.LEFT, padx=5)
        
        # Emergency stop key
        stop_key_frame = ttk.Frame(hotkey_frame)
        stop_key_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(stop_key_frame, text="Emergency Stop:").pack(side=tk.LEFT)
        
        # Make sure stop key is loaded from settings
        self.stop_key_var = tk.StringVar(value=self.settings['stop_key'])
        print(f"Setting stop key entry to: {self.settings['stop_key']}")
        self.stop_key_entry = ttk.Entry(stop_key_frame, textvariable=self.stop_key_var, width=15)
        self.stop_key_entry.pack(side=tk.LEFT, padx=5)
        
        self.record_stop_btn = ttk.Button(
            stop_key_frame, 
            text="Record", 
            command=self.record_stop_key
        )
        self.record_stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Theme selector frame
        theme_frame = ttk.LabelFrame(main_frame, text="Theme")
        theme_frame.pack(fill=tk.X, pady=10)
        
        theme_select_frame = ttk.Frame(theme_frame)
        theme_select_frame.pack(fill=tk.X, pady=5)
        
        # Create radio buttons for themes
        ttk.Radiobutton(
            theme_select_frame,
            text="Light",
            variable=self.theme_var,
            value="light",
            command=lambda: self.apply_theme("light")
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            theme_select_frame,
            text="Dark",
            variable=self.theme_var,
            value="dark",
            command=lambda: self.apply_theme("dark")
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            theme_select_frame,
            text="Hacker",
            variable=self.theme_var,
            value="hacker",
            command=lambda: self.apply_theme("hacker")
        ).pack(side=tk.LEFT, padx=5)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.save_btn = ttk.Button(
            button_frame, 
            text="Save Settings", 
            command=self.update_settings
        )
        self.save_btn.pack(side=tk.LEFT, padx=5, expand=True)
        
        self.start_btn = ttk.Button(
            button_frame, 
            text="Start Typing", 
            command=self.toggle_typing
        )
        self.start_btn.pack(side=tk.RIGHT, padx=5, expand=True)
        
        # Status frame
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=10)
        
        status_label = ttk.Label(
            status_frame, 
            textvariable=self.status_var,
            font=("Arial", 10)
        )
        status_label.pack(side=tk.LEFT)
        
        # Info text at the bottom
        info_text = f"Press {self.settings['hotkey']} to start/stop typing from clipboard.\nPress {self.settings['stop_key']} for emergency stop."
        info_label = ttk.Label(
            main_frame, 
            text=info_text,
            justify=tk.CENTER
        )
        info_label.pack(pady=10)
        
        # Make the window stay on top
        self.root.attributes('-topmost', True)
        
        # Apply the theme after all widgets are created
        self.apply_theme(self.settings['theme'])
        
        # Set up a protocol for when the window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Update UI periodically to show typing status
        self.update_ui()
    
    def record_hotkey(self):
        """Record a new hotkey."""
        self.record_hotkey_btn.config(text="Recording...")
        self.hotkey_entry.delete(0, tk.END)
        self.hotkey_entry.insert(0, "Press keys...")
        
        # Unhook all existing keyboard hooks for clean slate
        keyboard.unhook_all()
        
        # Track currently pressed keys
        pressed_keys = set()
        recording_complete = [False]  # Using list for mutable state
        
        # Function to handle key down
        def on_key_down(e):
            if recording_complete[0]:
                return
                
            key = e.name
            # Convert 'control' to 'ctrl' for consistency
            if key == 'control':
                key = 'ctrl'
            elif key == 'windows':
                key = 'win'
            
            # Add to pressed keys
            pressed_keys.add(key)
            
            # Update display
            sorted_keys = sorted([k for k in pressed_keys if k in ['ctrl', 'alt', 'shift', 'win']])
            other_keys = [k for k in pressed_keys if k not in ['ctrl', 'alt', 'shift', 'win']]
            
            hotkey_str = '+'.join(sorted_keys + other_keys)
            self.hotkey_entry.delete(0, tk.END)
            self.hotkey_entry.insert(0, hotkey_str)
        
        # Function to handle key up - finalize when a non-modifier key is released
        def on_key_up(e):
            if recording_complete[0]:
                return
                
            key = e.name
            # Convert for consistency
            if key == 'control':
                key = 'ctrl'
            elif key == 'windows':
                key = 'win'
            
            # Only stop recording if a non-modifier was released
            is_modifier = key in ['ctrl', 'alt', 'shift', 'win']
            
            if not is_modifier:
                # We have a non-modifier key released, finalize the hotkey
                recording_complete[0] = True
                
                sorted_keys = sorted([k for k in pressed_keys if k in ['ctrl', 'alt', 'shift', 'win']])
                other_keys = [k for k in pressed_keys if k not in ['ctrl', 'alt', 'shift', 'win']]
                
                # Limit to one non-modifier key
                if other_keys:
                    other_keys = [other_keys[0]]
                    
                # Make sure we have at least one modifier and one key
                if not sorted_keys:
                    sorted_keys = ['ctrl']  # Default to ctrl if no modifiers
                if not other_keys:
                    other_keys = ['t']  # Default to 't' if no non-modifier key
                
                final_hotkey = '+'.join(sorted_keys + other_keys)
                
                # Update the UI directly in the Entry widget
                self.hotkey_entry.delete(0, tk.END)
                self.hotkey_entry.insert(0, final_hotkey)
                
                # Clean up and finalize
                finalize_recording(final_hotkey)
        
        def finalize_recording(final_hotkey):
            # Clean up
            try:
                keyboard.unhook_all()
            except Exception as e:
                print(f"Error unhooking all keys: {e}")
            
            # Re-register main hotkeys - but don't update settings yet
            # to avoid overwriting before Save is clicked
            try:
                print(f"Re-registering original hotkeys: {self.settings['hotkey']} and {self.settings['stop_key']}")
                keyboard.add_hotkey(self.settings['hotkey'], self.toggle_typing)
                keyboard.add_hotkey(self.settings['stop_key'], self.stop_typing)
            except Exception as e:
                print(f"Error re-registering hotkeys after recording: {e}")
            
            # Change button text
            self.record_hotkey_btn.config(text="Record")
            
            print(f"Recorded hotkey: {final_hotkey}")
        
        # Hook both key down and key up events
        keyboard.on_press(on_key_down)
        keyboard.on_release(on_key_up)
        
        # Safety timeout (5 seconds)
        def timeout_handler():
            if not recording_complete[0] and self.record_hotkey_btn.cget('text') == "Recording...":
                recording_complete[0] = True
                self.record_hotkey_btn.config(text="Record")
                
                # Get whatever we have so far
                sorted_keys = sorted([k for k in pressed_keys if k in ['ctrl', 'alt', 'shift', 'win']])
                other_keys = [k for k in pressed_keys if k not in ['ctrl', 'alt', 'shift', 'win']]
                
                # Default values if nothing was pressed
                if not sorted_keys:
                    sorted_keys = ['ctrl']
                if not other_keys:
                    other_keys = ['t']
                
                final_hotkey = '+'.join(sorted_keys + other_keys)
                
                # Update the UI
                self.hotkey_entry.delete(0, tk.END)
                self.hotkey_entry.insert(0, final_hotkey)
                
                finalize_recording(final_hotkey)
        
        self.root.after(5000, timeout_handler)
    
    def record_stop_key(self):
        """Record a new emergency stop key."""
        self.record_stop_btn.config(text="Recording...")
        self.stop_key_entry.delete(0, tk.END)
        self.stop_key_entry.insert(0, "Press key...")
        
        # Unhook all keyboard hooks for clean slate
        keyboard.unhook_all()
        
        # Track if we've already processed a key
        key_processed = [False]  # Using list as a mutable container
        
        # Function to handle key press
        def on_key_press(e):
            if key_processed[0]:
                return False
                
            # Mark as processed to prevent multiple keys
            key_processed[0] = True
            
            # Get single key
            key = e.name
            
            # Update the Entry widget directly
            self.stop_key_entry.delete(0, tk.END)
            self.stop_key_entry.insert(0, key)
            
            # Finish recording
            finalize_recording(key)
            return False  # Stop propagation
            
        def finalize_recording(key):
            self.record_stop_btn.config(text="Record")
            
            try:
                keyboard.unhook_all()
            except Exception as e:
                print(f"Error unhooking all keys: {e}")
                
            # Re-register main hotkeys
            try:
                keyboard.add_hotkey(self.settings['hotkey'], self.toggle_typing)
                keyboard.add_hotkey(self.settings['stop_key'], self.stop_typing)
            except Exception as e:
                print(f"Error re-registering hotkeys after stop key recording: {e}")
                
            print(f"Recorded stop key: {key}")
        
        # Hook for a single key press
        keyboard.on_press(on_key_press, suppress=True)
        
        # Safety timeout (5 seconds)
        def timeout_handler():
            if not key_processed[0] and self.record_stop_btn.cget('text') == "Recording...":
                key_processed[0] = True
                # Default to esc if no key pressed
                self.stop_key_entry.delete(0, tk.END)
                self.stop_key_entry.insert(0, "esc")
                finalize_recording("esc")
        
        self.root.after(5000, timeout_handler)
    
    def update_settings(self):
        """Update settings from the GUI inputs."""
        try:
            min_delay = float(self.min_delay_var.get())
            max_delay = float(self.max_delay_var.get())
            start_delay = float(self.start_delay_var.get())
            
            if min_delay < 0 or max_delay < 0 or start_delay < 0:
                raise ValueError("Delays cannot be negative")
            
            if min_delay > max_delay:
                min_delay, max_delay = max_delay, min_delay
            
            # Directly read values from Entry widgets
            hotkey = self.hotkey_entry.get()
            stop_key = self.stop_key_entry.get()
            theme = self.theme_var.get()
            
            print(f"Reading from UI - hotkey: '{hotkey}', stop_key: '{stop_key}', start_delay: {start_delay}")
            
            # Validate hotkey format
            if not hotkey:
                hotkey = "ctrl+shift+t"  # Default if empty
                self.hotkey_entry.delete(0, tk.END)
                self.hotkey_entry.insert(0, hotkey)
            
            # Clean up hotkeys to ensure consistent format
            if '+' not in hotkey and len(hotkey) > 1:
                # This might be a space-separated hotkey, convert to + format
                hotkey = hotkey.replace(' ', '+')
                self.hotkey_entry.delete(0, tk.END)
                self.hotkey_entry.insert(0, hotkey)
            
            # First unhook ALL keyboard listeners to start clean
            keyboard.unhook_all()
            
            # Update settings dictionary
            self.settings['min_delay'] = min_delay
            self.settings['max_delay'] = max_delay
            self.settings['start_delay'] = start_delay
            self.settings['hotkey'] = hotkey
            self.settings['stop_key'] = stop_key
            self.settings['theme'] = theme
            
            print(f"Updated settings dictionary: {self.settings}")
            
            # Register new hotkeys with the updated settings
            try:
                keyboard.add_hotkey(hotkey, self.toggle_typing)
                print(f"Successfully registered new hotkey: '{hotkey}'")
                self.status_var.set(f"Hotkey '{hotkey}' registered")
            except Exception as e:
                print(f"Error registering new hotkey: {e}")
                self.status_var.set(f"Error registering hotkey: {str(e)}")
            
            try:
                keyboard.add_hotkey(stop_key, self.stop_typing)
                print(f"Successfully registered new stop key: '{stop_key}'")
            except Exception as e:
                print(f"Error registering new stop key: {e}")
                self.status_var.set(f"Error registering stop key: {str(e)}")
            
            # Save to file AFTER registering hotkeys
            self.save_settings()
            
            # Update the info text
            info_text = f"Press {hotkey} to start/stop typing from clipboard.\nPress {stop_key} for emergency stop."
            # Find the info label by traversing widget hierarchy more reliably
            for widget in self.root.winfo_children():
                if isinstance(widget, ttk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, ttk.Label) and child.cget('justify') == tk.CENTER:
                            child.config(text=info_text)
                            break
            
            self.status_var.set(f"Settings saved. Hotkey '{hotkey}' registered")
        except ValueError as e:
            self.status_var.set(f"Error: {str(e)}")
    
    def toggle_typing(self):
        """Toggle the typing simulation on/off."""
        print(f"Toggle typing called - current state: {self.typing}")
        try:
            # Ensure GUI exists before toggling
            if self.root and self.root.winfo_exists():
                if self.typing:
                    self.stop_typing()
                else:
                    self.start_typing()
            return False  # Returning False helps suppress the hotkey in some cases
        except Exception as e:
            print(f"Error in toggle_typing: {e}")
            return False
    
    def start_typing(self):
        """Start typing text from the clipboard."""
        print("Starting typing...")
        if not self.typing:
            clipboard_text = pyperclip.paste()
            if clipboard_text:
                self.typing = True
                self.status_var.set("Typing in progress...")
                self.start_btn.config(text="Stop Typing")
                
                # Start typing in a separate thread
                threading.Thread(target=self.type_text, args=(clipboard_text,), daemon=True).start()
            else:
                self.status_var.set("Error: Clipboard is empty")
    
    def stop_typing(self):
        """Stop the typing simulation."""
        print("Stopping typing...")
        if self.typing:
            self.typing = False
            self.status_var.set("Typing stopped")
            self.start_btn.config(text="Start Typing")
    
    def type_text(self, text):
        """Type out the given text with random delays."""
        # Use customizable delay before starting to type
        start_delay = self.settings['start_delay']
        print(f"Starting typing with {start_delay}s initial delay...")
        self.status_var.set(f"Starting in {start_delay}s...")
        time.sleep(start_delay)
        
        try:
            # Type each character with a random delay
            for char in text:
                if not self.typing:
                    break
                    
                # Type the character
                keyboard.write(char)
                
                # Random delay between characters
                delay = random.uniform(self.settings['min_delay'], self.settings['max_delay'])
                time.sleep(delay)
        except Exception as e:
            print(f"Error during typing: {e}")
            self.status_var.set(f"Error during typing: {str(e)}")
        finally:
            # Set typing to False when done
            self.typing = False
            if self.root and self.root.winfo_exists():
                self.status_var.set("Typing completed")
                self.start_btn.config(text="Start Typing")
    
    def update_ui(self):
        """Update the UI periodically."""
        try:
            # Check if root still exists
            if self.root and self.root.winfo_exists():
                # Update the start button text
                if self.typing:
                    self.start_btn.config(text="Stop Typing")
                else:
                    self.start_btn.config(text="Start Typing")
                
                # Schedule the next update
                self.root.after(100, self.update_ui)
        except tk.TclError:
            # Window was likely destroyed, no need to reschedule
            pass
    
    def apply_theme(self, theme_name):
        """Apply the selected theme to the UI."""
        if theme_name not in self.themes:
            theme_name = 'light'  # Fallback to light theme
            
        theme = self.themes[theme_name]
        
        # Update the theme variable
        self.theme_var.set(theme_name)
        
        try:
            # Configure the root window background
            self.root.configure(bg=theme['bg'])
            
            # Configure ttk styles
            self.style.configure('TFrame', background=theme['bg'])
            self.style.configure('TLabel', background=theme['bg'], foreground=theme['fg'])
            self.style.configure('TButton', background=theme['button'])
            self.style.configure('TLabelframe', background=theme['bg'])
            self.style.configure('TLabelframe.Label', background=theme['bg'], foreground=theme['fg'])
            self.style.configure('TRadiobutton', background=theme['bg'], foreground=theme['fg'])
            
            # Update the settings
            self.settings['theme'] = theme_name
        except tk.TclError as e:
            print(f"Error applying theme: {e}")
    
    def on_close(self):
        """Clean up and close the application."""
        print("Closing application...")
        self.stop_typing()
        
        # Remove all hotkeys and keyboard listeners
        try:
            print("Unhooking all keyboard hooks...")
            keyboard.unhook_all()
        except Exception as e:
            print(f"Error unhooking all hotkeys: {e}")
            
        # Save settings
        print("Saving settings...")
        self.save_settings()
        
        # Destroy the GUI
        try:
            self.root.destroy()
        except Exception as e:
            print(f"Error destroying root: {e}")
    
    def run(self):
        """Run the main application loop."""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Error in mainloop: {e}")

def main():
    try:
        # Create and run the application
        app = ClipboardTyper()
        
        # Print hotkey info on startup for debugging
        print(f"Starting with hotkey: {app.settings['hotkey']}")
        
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
