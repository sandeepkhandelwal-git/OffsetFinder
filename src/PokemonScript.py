import re

def extract_data(file_path):
    """
    Extracts classes, methods, offsets, return types, and parameter types from the given file.
    """
    functions = []
    offsets = []
    igp_functions = []
    igp_protos = []
    current_class = None
    current_offset = None

    # Regex patterns
    class_pattern = re.compile(r'class\s+([a-zA-Z0-9_<>]+)')  # Match class definitions
    offset_pattern = re.compile(r'Offset:\s+(0x[0-9a-fA-F]+)')  # Match offset
    method_pattern = re.compile(r'(public|private|protected)?\s*(\w+)\s+(\w+)\s*\((.*?)\)\s*\{?')  # Match method declarations

    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        for line in file:
            # Match class
            class_match = class_pattern.search(line)
            if class_match:
                current_class = class_match.group(1)

            # Match offset
            offset_match = offset_pattern.search(line)
            if offset_match:
                current_offset = offset_match.group(1)
                offsets.append(current_offset)

            # Match method
            method_match = method_pattern.search(line)
            if method_match and current_class and current_offset:
                return_type = method_match.group(2)
                method_name = method_match.group(3)
                parameters = method_match.group(4)
                param_types = [param.split()[0] for param in parameters.split(",") if param.strip()]
                param_types = ["void *"] + param_types  # Include "this" pointer

                # Generate HOOK_FUNCTION format
                functions.append(f"HOOK_FUNCTION({current_offset}, {current_class}_{method_name});")

                # Generate APP_FUNCTION format for IGP_Functions.h
                formatted_params = ", ".join(param_types)
                igp_functions.append(f"APP_FUNCTION({current_offset}, {return_type}, {current_class}_{method_name}, ({formatted_params}));")

                # Generate PROTO_FUNCTION format for IGP_Protos.h
                igp_protos.append(f"PROTO_FUNCTION({current_offset}, void, Get_{method_name}, (void));")

                current_offset = None  # Reset after use

    return functions, offsets, igp_functions, igp_protos


def write_output(output_path, results):
    """
    Writes the extracted results to the specified file.
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(results))


def write_patches(output_path, offsets):
    """
    Writes all collected offsets to a single line in the specified file.
    """
    patches_line = ' '.join(f"-i {offset}" for offset in offsets)
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(patches_line)


def main():
    # File paths
    dump_file = ""
    igp_hooks_file = "IGP_Hooks.h"
    igp_patches_file = "IGP_Patches.h"
    igp_functions_file = "IGP_Functions.h"
    igp_protos_file = "IGP_Protos.h"

    # Extract data
    functions, offsets, igp_functions, igp_protos = extract_data(dump_file)

    # Write data to files
    write_output(igp_hooks_file, functions)
    write_patches(igp_patches_file, offsets)
    write_output(igp_functions_file, igp_functions)
    write_output(igp_protos_file, igp_protos)

    print(f"Extraction completed. Outputs saved to:")
    print(f" - {igp_hooks_file}")
    print(f" - {igp_patches_file}")
    print(f" - {igp_functions_file}")
    print(f" - {igp_protos_file}")


if __name__ == "__main__":
    main()
