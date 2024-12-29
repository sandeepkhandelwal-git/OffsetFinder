# Extractor Script for Offset Finder

## Overview

This script is designed to process a large `dump.cs` file and extract specific information about classes, methods, offsets, and parameters. It generates four distinct output files, each in a specific format, as required.

### Features

1. **`IGP_Hooks.h`**:
   - Contains a list of functions with their offsets and class names in the format:
     ```
     HOOK_FUNCTION(Offset, ClassName_MethodName);
     ```

2. **`IGP_Patches.h`**:
   - Contains all the offsets extracted from `dump.cs` in a single line with the format:
     ```
     -i Offset1 -i Offset2 -i Offset3
     ```

3. **`IGP_Functions.h`**:
   - Contains function definitions with return types, function names, and parameters (including the `this` pointer) in the format:
     ```
     APP_FUNCTION(Offset, ReturnType, ClassName_MethodName, (void *, ParamType1, ParamType2));
     ```

4. **`IGP_Protos.h`**:
   - Contains function prototypes with a `Get_` prefix added to the method names and a `void` return type in the format:
     ```
     PROTO_FUNCTION(0, void, Get_MethodName);
     ```

---

## Requirements

- Python 3.x
- A `dump.cs` file with structured class and method information.

---

## Setup and Usage

### 1. Configure File Locations
Modify the file paths in the `main()` function to match the location of your `dump.cs` file and desired output files:
```python
dump_file = "path/to/dump.cs"  # Location of the input file
igp_hooks_file = "path/to/IGP_Hooks.h"  # Location of the IGP_HOOK file
igp_patches_file = "path/to/IGP_Patches.h"  # Location of the IGP_Patches file
igp_functions_file = "path/to/IGP_Functions.h"  # Location of the IGP_Functions file
igp_protos_file = "path/to/IGP_Protos.h"  # Location of the IGP_Protos file
