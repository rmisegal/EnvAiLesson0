#!/usr/bin/env python3
"""
AI Environment Module v3.0.21
Date: 2025-08-13
Time: 14:00
"""

"""
AI Environment - Update Manager Module
Handles system updates from ZIP files in new_versions folder
"""

import os
import sys
import zipfile
import shutil
import subprocess
from pathlib import Path
import tempfile
import time

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    class Fore:
        GREEN = YELLOW = CYAN = WHITE = RED = MAGENTA = ""
    class Style:
        RESET_ALL = ""
    COLORAMA_AVAILABLE = False

class UpdateManager:
    """Manages system updates from ZIP files"""
    
    def __init__(self, ai_env_path):
        self.ai_env_path = Path(ai_env_path)
        self.new_versions_path = self.ai_env_path / "new_versions"
        self.backup_path = self.ai_env_path / "backup"
        
        # Ensure directories exist
        self.new_versions_path.mkdir(exist_ok=True)
        
    def scan_for_updates(self):
        """Scan new_versions folder for ZIP files"""
        try:
            if not self.new_versions_path.exists():
                return []
            
            zip_files = []
            for file_path in self.new_versions_path.iterdir():
                if file_path.is_file() and file_path.suffix.lower() == '.zip':
                    # Extract version info from filename if possible
                    filename = file_path.name
                    version = self._extract_version_from_filename(filename)
                    
                    zip_files.append({
                        'path': file_path,
                        'name': filename,
                        'version': version,
                        'size': file_path.stat().st_size
                    })
            
            # Sort by version if available, otherwise by name
            zip_files.sort(key=lambda x: (x['version'] or '', x['name']))
            return zip_files
            
        except Exception as e:
            print(f"{Fore.RED}Error scanning for updates: {e}{Style.RESET_ALL}")
            return []
    
    def _extract_version_from_filename(self, filename):
        """Extract version number from filename"""
        import re
        # Look for patterns like v3.0.21 or _v3.0.21_ or AI_Environment_v3.0.21
        version_patterns = [
            r'v(\d+\.\d+\.\d+)',
            r'_v(\d+\.\d+\.\d+)',
            r'(\d+\.\d+\.\d+)'
        ]
        
        for pattern in version_patterns:
            match = re.search(pattern, filename, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def display_available_updates(self):
        """Display available updates and allow selection"""
        zip_files = self.scan_for_updates()
        
        if not zip_files:
            print(f"{Fore.YELLOW}No ZIP files found in new_versions folder.{Style.RESET_ALL}")
            print(f"{Fore.CYAN}To add updates:{Style.RESET_ALL}")
            print(f"  1. Copy ZIP files to: {self.new_versions_path}")
            print(f"  2. Return to this menu to install them")
            return None
        
        print(f"\n{Fore.CYAN}📦 Available Updates:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        for i, zip_info in enumerate(zip_files, 1):
            size_mb = zip_info['size'] / (1024 * 1024)
            version_str = f" (v{zip_info['version']})" if zip_info['version'] else ""
            print(f"{i:2d}. {Fore.WHITE}{zip_info['name']}{version_str}{Style.RESET_ALL}")
            print(f"     Size: {size_mb:.1f} MB")
            print()
        
        print(f" 0. {Fore.YELLOW}Cancel and return to Version menu{Style.RESET_ALL}")
        print()
        
        try:
            choice = input(f"{Fore.WHITE}Select update to install (0-{len(zip_files)}): {Style.RESET_ALL}").strip()
            
            if choice == '0':
                return None
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(zip_files):
                return zip_files[choice_num - 1]
            else:
                print(f"{Fore.RED}Invalid choice. Please select 0-{len(zip_files)}.{Style.RESET_ALL}")
                return None
                
        except (ValueError, KeyboardInterrupt):
            print(f"{Fore.YELLOW}Update cancelled.{Style.RESET_ALL}")
            return None
    
    def install_update(self, zip_info):
        """Install selected update"""
        try:
            print(f"\n{Fore.CYAN}🔄 Installing Update: {zip_info['name']}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            
            # Confirm installation
            print(f"{Fore.YELLOW}⚠️  This will update your AI Environment system.{Style.RESET_ALL}")
            print(f"Current location: {self.ai_env_path}")
            print(f"Update file: {zip_info['name']}")
            if zip_info['version']:
                print(f"Version: {zip_info['version']}")
            print()
            
            confirm = input(f"{Fore.WHITE}Continue with installation? (y/N): {Style.RESET_ALL}").strip().lower()
            if confirm not in ['y', 'yes']:
                print(f"{Fore.YELLOW}Update cancelled by user.{Style.RESET_ALL}")
                return False
            
            # Create backup
            if not self._create_backup():
                print(f"{Fore.RED}Failed to create backup. Update cancelled.{Style.RESET_ALL}")
                return False
            
            # Extract and install
            if not self._extract_and_install(zip_info):
                print(f"{Fore.RED}Update installation failed.{Style.RESET_ALL}")
                self._restore_backup()
                return False
            
            # Handle run_ai_env.bat update if needed
            self._handle_batch_file_update()
            
            print(f"\n{Fore.GREEN}✅ Update installed successfully!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Changes will take effect on next restart.{Style.RESET_ALL}")
            
            # Clean up
            self._cleanup_backup()
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}Error during update installation: {e}{Style.RESET_ALL}")
            self._restore_backup()
            return False
    
    def _create_backup(self):
        """Create backup of current system"""
        try:
            print(f"{Fore.CYAN}📋 Creating backup...{Style.RESET_ALL}")
            
            # Remove old backup if exists
            if self.backup_path.exists():
                shutil.rmtree(self.backup_path)
            
            self.backup_path.mkdir(exist_ok=True)
            
            # Backup critical files
            critical_files = [
                'src/',
                'config/',
                'version_config.json',
                'run_ai_env.bat',
                'setup_python_env.bat',
                'check_versions.bat',
                'README.md',
                'PACKAGE_INFO.txt'
            ]
            
            for item in critical_files:
                source = self.ai_env_path / item
                if source.exists():
                    dest = self.backup_path / item
                    if source.is_dir():
                        shutil.copytree(source, dest)
                    else:
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source, dest)
            
            print(f"{Fore.GREEN}✅ Backup created successfully{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}Failed to create backup: {e}{Style.RESET_ALL}")
            return False
    
    def _extract_and_install(self, zip_info):
        """Extract ZIP and install files"""
        try:
            print(f"{Fore.CYAN}📦 Extracting update...{Style.RESET_ALL}")
            
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Extract ZIP to temporary directory
                with zipfile.ZipFile(zip_info['path'], 'r') as zip_ref:
                    zip_ref.extractall(temp_path)
                
                # Find the AI_Environment folder in extracted content
                ai_env_folder = None
                for item in temp_path.iterdir():
                    if item.is_dir() and item.name == 'AI_Environment':
                        ai_env_folder = item
                        break
                
                if not ai_env_folder:
                    print(f"{Fore.RED}Invalid update ZIP: AI_Environment folder not found{Style.RESET_ALL}")
                    return False
                
                # Copy files from extracted folder to current location
                print(f"{Fore.CYAN}📁 Installing files...{Style.RESET_ALL}")
                
                for item in ai_env_folder.iterdir():
                    if item.name in ['new_versions', 'backup']:
                        continue  # Skip these folders
                    
                    dest = self.ai_env_path / item.name
                    
                    if item.is_dir():
                        if dest.exists():
                            shutil.rmtree(dest)
                        shutil.copytree(item, dest)
                        print(f"  ✓ Updated folder: {item.name}")
                    else:
                        if dest.exists():
                            dest.unlink()
                        shutil.copy2(item, dest)
                        print(f"  ✓ Updated file: {item.name}")
                
                print(f"{Fore.GREEN}✅ Files installed successfully{Style.RESET_ALL}")
                return True
                
        except Exception as e:
            print(f"{Fore.RED}Failed to extract and install: {e}{Style.RESET_ALL}")
            return False
    
    def _handle_batch_file_update(self):
        """Handle updating batch files while system is running"""
        try:
            print(f"{Fore.CYAN}🔄 Checking batch file updates...{Style.RESET_ALL}")
            
            # Check if run_ai_env.bat was updated
            run_ai_env = self.ai_env_path / "run_ai_env.bat"
            if run_ai_env.exists():
                print(f"{Fore.YELLOW}ℹ️  run_ai_env.bat has been updated{Style.RESET_ALL}")
                print(f"{Fore.CYAN}   Changes will take effect on next restart{Style.RESET_ALL}")
            
            # Note: We can't restart the batch file while it's running
            # The user will need to restart manually
            
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not check batch file updates: {e}{Style.RESET_ALL}")
    
    def _restore_backup(self):
        """Restore from backup if update fails"""
        try:
            if not self.backup_path.exists():
                return False
            
            print(f"{Fore.CYAN}🔄 Restoring from backup...{Style.RESET_ALL}")
            
            for item in self.backup_path.iterdir():
                dest = self.ai_env_path / item.name
                
                if dest.exists():
                    if dest.is_dir():
                        shutil.rmtree(dest)
                    else:
                        dest.unlink()
                
                if item.is_dir():
                    shutil.copytree(item, dest)
                else:
                    shutil.copy2(item, dest)
            
            print(f"{Fore.GREEN}✅ System restored from backup{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}Failed to restore backup: {e}{Style.RESET_ALL}")
            return False
    
    def _cleanup_backup(self):
        """Clean up backup after successful update"""
        try:
            if self.backup_path.exists():
                shutil.rmtree(self.backup_path)
        except Exception:
            pass  # Ignore cleanup errors
    
    def show_update_info(self):
        """Show information about the update system"""
        print(f"\n{Fore.CYAN}🔄 AI Environment Update System{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print()
        print(f"{Fore.WHITE}How to use:{Style.RESET_ALL}")
        print(f"  1. Copy new AI Environment ZIP files to:")
        print(f"     {Fore.CYAN}{self.new_versions_path}{Style.RESET_ALL}")
        print(f"  2. Select this Update option")
        print(f"  3. Choose which ZIP file to install")
        print(f"  4. Confirm installation")
        print()
        print(f"{Fore.WHITE}Safety features:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Automatic backup before update")
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Rollback on failure")
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Version detection from filenames")
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Confirmation before installation")
        print()
        print(f"{Fore.WHITE}Update folder:{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}{self.new_versions_path}{Style.RESET_ALL}")
        
        # Show current contents
        zip_files = self.scan_for_updates()
        if zip_files:
            print(f"\n{Fore.WHITE}Currently available updates: {len(zip_files)}{Style.RESET_ALL}")
            for zip_info in zip_files:
                version_str = f" (v{zip_info['version']})" if zip_info['version'] else ""
                print(f"  • {zip_info['name']}{version_str}")
        else:
            print(f"\n{Fore.YELLOW}No update files found in new_versions folder{Style.RESET_ALL}")

def main():
    """Main function for standalone execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Environment Update Manager')
    parser.add_argument('--ai-env-path', default='.', 
                       help='Path to AI Environment directory')
    parser.add_argument('--scan', action='store_true',
                       help='Scan for available updates')
    parser.add_argument('--info', action='store_true',
                       help='Show update system information')
    
    args = parser.parse_args()
    
    manager = UpdateManager(args.ai_env_path)
    
    if args.scan:
        zip_files = manager.scan_for_updates()
        print(f"Found {len(zip_files)} update files")
        for zip_info in zip_files:
            print(f"  {zip_info['name']}")
    elif args.info:
        manager.show_update_info()
    else:
        # Interactive mode
        selected = manager.display_available_updates()
        if selected:
            manager.install_update(selected)

if __name__ == "__main__":
    main()

