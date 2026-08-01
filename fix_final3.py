#!/usr/bin/env python3
"""Fix EMBEDDED_STORIES by reading stories.json and using JSON decoder to find array end"""
import json

# Read stories
with open('stories.json', 'r', encoding='utf-8') as f:
    stories = json.load(f)
print(f'stories.json: {len(stories)} stories')

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find const EMBEDDED_STORIES
marker = 'const EMBEDDED_STORIES'
idx = content.find(marker)
if idx == -1:
    print('ERROR: EMBEDDED_STORIES not found')
    exit(1)

# Find the opening [ of the array
arr_open = content.find('[', idx)
if arr_open == -1:
    print('ERROR: Array open not found')
    exit(1)

# Use JSON decoder to find the end of the array
# We'll try parsing from different positions until we find the correct one
decoder = json.JSONDecoder()

# Skip past the opening [
parse_start = arr_open + 1

# The first character after [ should be { (first object)
# Try to parse the array
try:
    # Use raw_decode to parse and get the end position
    obj, end_pos = decoder.raw_decode(content[arr_open:])
    print(f'Parsed! Type: {type(obj).__name__}, len: {len(obj)}')
    print(f'Array ends at char: {arr_open + end_pos}')
    print(f'Context after: {repr(content[arr_open + end_pos:arr_open + end_pos + 10])}')
except json.JSONDecodeError as e:
    print(f'Error: {e}')
    print(f'At pos: {e.pos}')
    print(f'Context: {repr(content[arr_open + e.pos - 20:arr_open + e.pos + 20])}')
    # Maybe the array has double [[?
    if content[arr_open:arr_open+2] == '[[':
        print('Found double [[, trying with single [...')
        try:
            obj, end_pos = decoder.raw_decode(content[arr_open+1:])
            print(f'Parsed with offset! len: {len(obj)}')
        except json.JSONDecodeError as e2:
            print(f'Error2: {e2}')
            exit(1)
    else:
        exit(1)

# Actually, the issue might be simpler - let me just split the file at known points
# Everything before "const EMBEDDED_STORIES" + new array + everything after the old array

# Find the end of the old array by looking for ]; followed by blank line or \n\n
search_start = arr_open
# Find ]; that closes the outer array
# The outer array contains nested objects with arrays inside them
# We need to track bracket depth properly

# Actually, let me try a different approach: just use the JSON decoder to find
# where the array ends

# Try parsing from the [
try:
    decoder = json.JSONDecoder()
    # The JSON might start with [[ if there's a double bracket
    if content[arr_open:arr_open+2] == '[[':
        print('Double bracket detected!')
        # Try parsing from second [
        obj, end = decoder.raw_decode(content[arr_open+1:])
        print(f'Parsed from second [: len={len(obj)}, end={end}')
        # The outer ]]] would be at arr_open + 1 + end
        # But we need to find the ]; that closes everything
        # The parsed object is the inner array, so the full thing is [...]
        # The end of the full declaration is arr_open + 1 + end + 1 (for outer ])
        full_end = arr_open + 1 + end + 1
        print(f'Full end: {full_end}')
        print(f'Context: {repr(content[full_end:full_end+10])}')
    else:
        obj, end = decoder.raw_decode(content[arr_open:])
        print(f'Parsed directly: len={len(obj)}, end={end}')
        full_end = arr_open + end
        print(f'Full end: {full_end}')
except json.JSONDecodeError as e:
    print(f'Parse error: {e}')
    # Try finding ]; by looking for the pattern
    # Actually the old array is probably small, let me find the last ]; before //
    pass

# Alternative approach: find the end of the array by finding ";\n\n// ====="
# This marks the start of the next section
end_marker = ';\n\n// ====='
end_pos = content.find(end_marker, idx)
if end_pos != -1:
    print(f'Found end marker at: {end_pos}')
    # The array declaration is from idx to end_pos + 1 (include ;)
    decl_end = end_pos + 1
    print(f'Declaration: {idx} to {decl_end}')
    print(f'Context after: {repr(content[decl_end:decl_end+20])}')
    
    # Generate new array
    new_arr = json.dumps(stories, ensure_ascii=False, indent=2)
    new_decl = f'const EMBEDDED_STORIES = {new_arr};'
    
    # Replace
    new_content = content[:idx] + new_decl + content[decl_end:]
    
    # Write
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f'Written! Size: {len(new_content)} bytes')
else:
    print('End marker not found')
