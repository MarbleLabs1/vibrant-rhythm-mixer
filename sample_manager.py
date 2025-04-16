
import os
import json
from PyQt6.QtCore import QObject, pyqtSignal

class SampleManager(QObject):
    """
    Manages audio samples for the DJ pad application.
    Handles loading, saving, and organizing samples and sample banks.
    """
    samples_loaded = pyqtSignal(list)
    sample_bank_changed = pyqtSignal(str)
    
    def __init__(self, samples_directory="resources/samples"):
        super().__init__()
        self.samples_directory = samples_directory
        self.current_bank = "Default"
        self.banks = {}
        self.sample_pads = {}  # Maps pad index to sample data
        
        # Create samples directory if it doesn't exist
        os.makedirs(self.samples_directory, exist_ok=True)
        
        # Create default sample bank
        self.create_default_bank()
        
        # Load stored sample banks
        self.load_sample_banks()
    
    def create_default_bank(self):
        """Create a default sample bank with empty pads"""
        self.banks["Default"] = {
            "name": "Default Bank",
            "pads": {}
        }
        
        # Initialize with empty sample pads
        for i in range(16):
            pad_name = ""
            if i % 4 == 0:
                pad_name = f"KICK {(i // 4) + 1}"
            elif i % 4 == 1:
                pad_name = f"SNARE {(i // 4) + 1}"
            elif i % 4 == 2:
                pad_name = f"HAT {(i // 4) + 1}"
            elif i % 4 == 3:
                pad_name = f"CLAP {(i // 4) + 1}"
                
            self.banks["Default"]["pads"][str(i)] = {
                "name": pad_name,
                "file_path": "",
                "color": i % 8  # Use this as color index reference
            }
        
        # Save the default bank
        self.save_sample_banks()
    
    def load_sample_banks(self):
        """Load sample banks from JSON file"""
        banks_file = os.path.join(self.samples_directory, "sample_banks.json")
        
        if os.path.exists(banks_file):
            try:
                with open(banks_file, 'r') as f:
                    self.banks = json.load(f)
                print(f"Loaded {len(self.banks)} sample banks")
                
                # Set current bank
                if self.current_bank not in self.banks:
                    self.current_bank = next(iter(self.banks.keys()))
                    
                # Load current bank's samples
                self.load_bank(self.current_bank)
            except Exception as e:
                print(f"Error loading sample banks: {str(e)}")
                # Fallback to default bank
                self.create_default_bank()
        else:
            # Create default bank file
            self.save_sample_banks()
    
    def save_sample_banks(self):
        """Save sample banks to JSON file"""
        banks_file = os.path.join(self.samples_directory, "sample_banks.json")
        
        try:
            with open(banks_file, 'w') as f:
                json.dump(self.banks, f, indent=2)
            print("Sample banks saved successfully")
        except Exception as e:
            print(f"Error saving sample banks: {str(e)}")
    
    def load_bank(self, bank_name):
        """Load a specific sample bank"""
        if bank_name in self.banks:
            self.current_bank = bank_name
            self.sample_pads = self.banks[bank_name]["pads"]
            print(f"Loaded sample bank: {bank_name}")
            
            # Notify that bank has changed
            self.sample_bank_changed.emit(bank_name)
            
            # Emit loaded samples
            self.samples_loaded.emit(list(self.sample_pads.items()))
            return True
        else:
            print(f"Sample bank '{bank_name}' not found")
            return False
    
    def create_bank(self, bank_name):
        """Create a new sample bank"""
        if bank_name in self.banks:
            print(f"Sample bank '{bank_name}' already exists")
            return False
        
        self.banks[bank_name] = {
            "name": bank_name,
            "pads": {}
        }
        
        # Initialize empty pads
        for i in range(16):
            self.banks[bank_name]["pads"][str(i)] = {
                "name": f"Pad {i+1}",
                "file_path": "",
                "color": i % 8
            }
        
        # Save banks
        self.save_sample_banks()
        
        return True
    
    def delete_bank(self, bank_name):
        """Delete a sample bank"""
        if bank_name == "Default":
            print("Cannot delete the default sample bank")
            return False
        
        if bank_name in self.banks:
            del self.banks[bank_name]
            
            # If current bank was deleted, switch to default
            if self.current_bank == bank_name:
                self.load_bank("Default")
            
            # Save banks
            self.save_sample_banks()
            
            return True
        else:
            print(f"Sample bank '{bank_name}' not found")
            return False
    
    def assign_sample(self, pad_index, file_path, name=None):
        """Assign a sample to a pad in the current bank"""
        pad_index_str = str(pad_index)
        
        if pad_index_str not in self.sample_pads:
            print(f"Invalid pad index: {pad_index}")
            return False
        
        # Extract filename if name not provided
        if name is None:
            name = os.path.basename(file_path)
        
        # Update pad data
        self.sample_pads[pad_index_str]["file_path"] = file_path
        self.sample_pads[pad_index_str]["name"] = name
        
        # Update bank data
        self.banks[self.current_bank]["pads"] = self.sample_pads
        
        # Save changes
        self.save_sample_banks()
        
        # Notify that samples have changed
        self.samples_loaded.emit(list(self.sample_pads.items()))
        
        return True
    
    def get_sample_path(self, pad_index):
        """Get the file path for a sample pad"""
        pad_index_str = str(pad_index)
        
        if pad_index_str in self.sample_pads:
            return self.sample_pads[pad_index_str]["file_path"]
        else:
            return None
    
    def get_sample_name(self, pad_index):
        """Get the name for a sample pad"""
        pad_index_str = str(pad_index)
        
        if pad_index_str in self.sample_pads:
            return self.sample_pads[pad_index_str]["name"]
        else:
            return f"Pad {pad_index+1}"
    
    def get_sample_color(self, pad_index):
        """Get the color index for a sample pad"""
        pad_index_str = str(pad_index)
        
        if pad_index_str in self.sample_pads:
            return self.sample_pads[pad_index_str]["color"]
        else:
            return pad_index % 8
    
    def set_pad_color(self, pad_index, color_index):
        """Set the color for a sample pad"""
        pad_index_str = str(pad_index)
        
        if pad_index_str in self.sample_pads:
            self.sample_pads[pad_index_str]["color"] = color_index
            
            # Update bank data
            self.banks[self.current_bank]["pads"] = self.sample_pads
            
            # Save changes
            self.save_sample_banks()
            
            # Notify that samples have changed
            self.samples_loaded.emit(list(self.sample_pads.items()))
            
            return True
        else:
            return False
    
    def get_all_banks(self):
        """Get list of all sample banks"""
        return list(self.banks.keys())
    
    def get_bank_info(self, bank_name=None):
        """Get information about a specific bank or current bank"""
        if bank_name is None:
            bank_name = self.current_bank
            
        if bank_name in self.banks:
            return self.banks[bank_name]
        else:
            return None
