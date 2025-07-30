#!/usr/bin/env python3
"""
Fix line length issues in geometry_engine.py by applying consistent formatting
"""

import re

def fix_long_lines(content):
    """Fix lines that are too long"""
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        if len(line) <= 88:
            fixed_lines.append(line)
            continue
            
        # Try to break long f-strings
        if 'f"' in line and len(line) > 88:
            # Look for natural break points in f-strings
            if ' = ' in line and 'f"' in line:
                parts = line.split(' = ', 1)
                if len(parts) == 2:
                    indent = len(parts[0]) - len(parts[0].lstrip())
                    spaces = ' ' * indent
                    if len(parts[1]) > 40:
                        # Break the f-string
                        fixed_lines.append(parts[0] + ' = (')
                        # Find a good break point
                        fstring = parts[1].strip()
                        if 'Volume=' in fstring and 'Surface Area=' in fstring:
                            fixed_lines.append(spaces + '    f"' + fstring.split('Volume=')[0] + 'Volume={volume:.6f}, "')
                            fixed_lines.append(spaces + '    f"Surface Area={surface:.6f}"')
                            fixed_lines.append(spaces + ')')
                        else:
                            fixed_lines.append(spaces + '    ' + fstring)
                            fixed_lines.append(spaces + ')')
                    else:
                        fixed_lines.append(line)
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

# Read the file
with open('geometry_engine.py', 'r') as f:
    content = f.read()

# Apply fixes
fixed_content = fix_long_lines(content)

# Write back
with open('geometry_engine.py', 'w') as f:
    f.write(fixed_content)

print("Line length fixes applied to geometry_engine.py")