def replace_env_variables(text: str, context: dict) -> str:
    env_variable_marker = "$"
    for k, v in context.items():
        text = text.replace(f"{env_variable_marker}{k}", str(v))
        text = text.replace(f"{env_variable_marker}{{{k}}}", str(v))

    return text
