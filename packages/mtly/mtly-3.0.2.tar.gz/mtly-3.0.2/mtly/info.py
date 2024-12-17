from mtly import motley


def info() -> str:
    return f"""
        {motley(text="info", style="bold_italic", color_combo="night")}: 
             {motley(text="colors", style="bold_italic")}: (
                {motley(text="green", color="green")}, {motley(text="dark_green", color="dark_green")}, {motley(text="light_blue", color="light_blue")}, {motley(text="blue", color="blue")}, {motley(text="dark_blue", color="dark_blue")}, 
                {motley(text="yellow", color="yellow")}, {motley(text="orange", color="orange")}, {motley(text="red", color="red")}, {motley(text="purple", color="purple")}, {motley(text="dark_purple", color="dark_purple")}, 
                {motley(text="black", color="black")}, {motley(text="grey", color="grey")}
            {motley(text=")")}
             {motley(text="styles", style="bold_italic")}: (
                {motley(text="italic", style="italic")}, {motley(text="bold", style="bold")}, {motley(text="bold_italic", style="bold_italic")}
            )
            {motley(text="color_combos", style="bold_italic")}: (
                {motley(text="volcano", color_combo="volcano")} {motley(text="(volcano)")}, {motley(text="fresh", color_combo="fresh")} {motley(text="(fresh)")}, {motley(text="night", color_combo="night")} {motley(text="(night)")}
            {motley(text=")")}

        {motley(text="author", style="bold_italic", color_combo="volcano")}: {motley(text="Hspu1", style="bold_italic", color_combo="fresh")}
    """
