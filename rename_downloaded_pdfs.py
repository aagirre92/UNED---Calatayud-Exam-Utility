import os
from datetime import datetime

def parse_filename(filename):
    """Parse the filename to extract information"""
    if not filename.endswith('.pdf'):
        return None
    
    special_case=False
    
    if '-' in filename:
        print(f"Special case: {filename}")
        special_case=True
        parts = filename.split('-')
        if len(parts) != 2:
            return None
        
        code = parts[1][:-4]
        if len(code) != 4:
            return None
        
        info = {}
        info['is_solution'] = filename.startswith('S')
        
        year = code[:2]
        month_code = code[2]
        week_code = code[3]
        
        info['year'] = f'20{year}'
        
        info['model'] = "na"
        
        month_map = {
            'F': 'February',
            'S': 'September',
            'J': 'June',
        }
        
        info['month'] = month_map.get(month_code, None)
        if info['month'] is None:
            return None
        
        if month_code == 'S' and week_code == 'O':
            info['week'] = None
        elif month_code == 'S' and week_code == 'R':
            info['week'] = 'R'
        elif week_code and week_code.isdigit():
            info['week'] = week_code
        else:
            info['week'] = None
        return info
    
        
    if not special_case:
        filename_no_pdf = filename[:-4]
        code = filename_no_pdf[-5:]
        print(f"Filename: {filename_no_pdf}")
        print(f"Code: {code}")
        
        try:
            info = {}
            info['is_solution'] = filename.startswith('S')
            
            model = code[0]
            year = code[1:3]
            month_code = code[3] if len(code) > 3 else None
            week_code = code[4] if len(code) > 4 else None
            
            if model not in ['A', 'B', 'C', 'D', 'E']:
                return None
                
            info['model'] = model
            info['year'] = f'20{year}'
            
            month_map = {
                'F': 'February',
                'S': 'September',
                'J': 'June',
                
            }
            
            info['month'] = month_map.get(month_code, None)
            if info['month'] is None:
                return None
                
            if month_code == 'S' and week_code == 'O':
                info['week'] = None
            elif month_code == 'S' and week_code == 'R':
                info['week'] = 'R'
            elif week_code and week_code.isdigit():
                info['week'] = week_code
            else:
                info['week'] = None
                
            return info
            
        except Exception as e:
            print(f"Error parsing {filename}: {str(e)}")
            return None

def rename_pdf_files(folder_path):
    """Rename PDF files according to the specified pattern"""
    print(f"Scanning folder: {folder_path}")
    
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found")
        return
    
    renamed_count = 0
    errors_count = 0
    
    for filename in os.listdir(folder_path):
        if not filename.lower().endswith('.pdf'):
            continue
            
        try:
            info = parse_filename(filename)
            if not info:
                print(f"Skipping {filename} - doesn't match expected pattern")
                continue
            
            prefix = "Solution_" if info['is_solution'] else ""
            if info['week'] is None:
                new_filename = f"{prefix}{info['year']}_{info['month']}_Model{info['model']}.pdf"
            elif info['week'] == 'R':
                new_filename = f"{prefix}{info['year']}_{info['month']}_Revision_Model{info['model']}.pdf"
            else:
                new_filename = f"{prefix}{info['year']}_{info['month']}_Week{info['week']}_Model{info['model']}.pdf"
            
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_filename)
            
            if os.path.exists(new_path):
                print(f"Error: Cannot rename {filename} - {new_filename} already exists")
                errors_count += 1
                continue
            
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_filename}")
            renamed_count += 1
            
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            errors_count += 1
    
    print(f"\nSummary:")
    print(f"Files renamed successfully: {renamed_count}")
    print(f"Errors encountered: {errors_count}")

if __name__ == "__main__":
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_folder = os.path.join(script_dir, "downloaded_pdfs")
        rename_pdf_files(pdf_folder)
    except Exception as e:
        print(f"Script execution failed: {str(e)}")
    