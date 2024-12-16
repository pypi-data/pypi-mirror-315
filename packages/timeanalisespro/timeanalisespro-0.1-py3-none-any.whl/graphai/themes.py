def set_theme(theme_name="default"):
    if theme_name == "dark":
        plt.style.use("dark_background")
    else:
        plt.style.use("default")
