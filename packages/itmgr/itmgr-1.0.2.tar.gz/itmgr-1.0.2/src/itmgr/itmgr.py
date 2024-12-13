# type: ignore[import]
# pyright: ignore[import]
# pylint: disable=import-error
# ruff: noqa: F401, E402
# mypy: ignore-errors
# flake8: noqa: F401



import os
import importlib
import subprocess
import sys
import builtins


def install_and_import(*modules: list[tuple[str, bool | list[str] | str | tuple[str], bool | str]]) -> None:
    """
    Installe et importe des bibliothèques selon les instructions fournies.

    `modules`: Liste de tuples contenant les informations pour chaque bibliothèque.
    
    Chaque tuple doit être de la forme : (nom_installation, mode_importation, alias ou False)

        - nom_installation : nom pour pip install

        - mode_importation : True pour "from module import attr", str ou list[str] ou tuple[str] pour "from module import attr"

        - alias : False pour pas d'alias ou str pour alias avec "as ..."
    """
    
    caller_globals = sys._getframe(1).f_globals
    
    for module_tpl in modules:
        module_name, from_imports, alias = module_tpl
        from_imports = [from_imports] if type(from_imports) == str and type(from_imports) != bool else \
            [i for i in from_imports] if type(from_imports) == tuple and type(from_imports) != bool \
                else from_imports

        try:
            if module_name not in sys.modules:
                __import__(module_name)   
            
            module = sys.modules[module_name]

            if alias is False:
                if len(module_name.split(".")) > 1 and from_imports == True:
                    alias = module_name.split(".")[-1]
                elif from_imports != True and from_imports != False:
                    alias = from_imports  # Utilise le nom du module comme alias par défaut
                else:
                    alias = module_name

            if from_imports == True:
                # Ajouter le module lui-même à l'espace de noms global avec l'alias
                caller_globals[alias] = module

            elif from_imports != True and from_imports != False:
                # Importer des éléments spécifiques
                for name in from_imports:
                    caller_globals[name] = getattr(module, name)
            else:
                raise ValueError("La seconde valeur doit être True ou une liste de noms d'attributs et pas False.")
            
        except ImportError:
            # Tenter l'installation si le module n'existe pas
            print(f"{module_name} non trouvé. Installation en cours...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
            
            # Réessayer l'import après installation
            try:
                if module_name not in sys.modules:
                    __import__(module_name)   
                
                module = sys.modules[module_name]

                if alias is False:
                    if len(module_name.split(".")) > 1 and from_imports == True:
                        alias = module_name.split(".")[-1]
                    elif from_imports != True and from_imports != False:
                        alias = from_imports  # Utilise le nom du module comme alias par défaut
                    else:
                        alias = module_name

                if from_imports == True:
                    # Ajouter le module lui-même à l'espace de noms global avec l'alias
                    caller_globals[alias] = module

                elif from_imports != True and from_imports != False:
                    # Importer des éléments spécifiques
                    for name in from_imports:
                        caller_globals[name] = getattr(module, name)
                else:
                    raise ValueError("La seconde valeur doit être True ou une liste de noms d'attributs et pas False.")
            except ImportError:
                print(f"Erreur : échec de l'installation de {module_name}")
        except Exception as e:
            print(f"Erreur lors de l'importation de {module_name}: {str(e)}")


def install(*modules) -> None:
    """
    Installe des bibliothèques Python en utilisant pip.
    -------------------
    - modules : modules à installer.
    """
    for module in modules:
        try:
            print(f"Installation de {module}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            print(f"{module} installé avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'installation de {module}: {str(e)}")


def importation(*modules : tuple[str, bool | list[str] | str | tuple[str], bool | str]) -> None:
    """
    Importe des bibliothèques Python.
    -------------------
    modules : modules à importer contenant :

        - module : nom du module à importer
        - mode : True pour "import module", str ou list[str] ou tuple[str] pour "from module import attr"
        - alias : False pour pas d'alias ou str pour alias avec "as ..."
    """
    caller_globals = sys._getframe(1).f_globals


    for module_tpl in modules:
        module_name, from_imports, alias = module_tpl
        from_imports = [from_imports] if type(from_imports) == str and type(from_imports) != bool else \
            [i for i in from_imports] if type(from_imports) == tuple and type(from_imports) != bool \
                else from_imports

        try:
            if module_name not in sys.modules:
                __import__(module_name)                

            module = sys.modules[module_name]
            
            if alias is False:
                if len(module_name.split(".")) > 1 and from_imports == True:
                    alias = module_name.split(".")[-1]
                elif from_imports != True and from_imports != False:
                    alias = from_imports  # Utilise le nom du module comme alias par défaut
                else:
                    alias = module_name

            if from_imports == True:
                # Ajouter le module lui-même à l'espace de noms global avec l'alias
                caller_globals[alias] = module

            elif from_imports != True and from_imports != False:
                # Importer des éléments spécifiques
                for name in from_imports:
                    caller_globals[name] = getattr(module, name)
            else:
                raise ValueError("La seconde valeur doit être True ou une liste de noms d'attributs et pas False.")

        except Exception as e:
            print(f"Erreur lors de l'importation de {module_name}: {str(e)}")


def uninstall(*modules) -> None:
    """
    Désinstalle des bibliothèques Python.
    -------------------
    - modules : modules à désinstaller.
    """
    for module in modules:
        print(f"Désinstallation de {module}...")
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", module])
        print(f"{module} désinstallé avec succès.")


def remove_module(*modules) -> None:
    """
    Enlève des bibliothèques Python dans le programme actuel.
    -------------------
    modules : tuple du module à enlever sous la forme :

        - nom_module : nom du module

        - mode_importation : True pour "from module import attr", str ou list[str] ou tuple[str] pour "from module import attr"

        - alias : False pour pas d'alias ou str pour alias avec "as ..."
    """
    
    caller_globals = sys._getframe(1).f_globals
    
    for module_tpl in modules:
        module_name, from_imports, alias = module_tpl
        from_imports = [from_imports] if type(from_imports) == str and type(from_imports) != bool else \
            [i for i in from_imports] if type(from_imports) == tuple and type(from_imports) != bool \
                else from_imports
    
    try:
            if module_name not in sys.modules:
                __import__(module_name)   
            
            module = sys.modules[module_name]

            if alias is False:
                if len(module_name.split(".")) > 1 and from_imports == True:
                    alias = module_name.split(".")[-1]
                elif from_imports != True and from_imports != False:
                    alias = from_imports  # Utilise le nom du module comme alias par défaut
                else:
                    alias = module_name

            if from_imports == True:
                # Ajouter le module lui-même à l'espace de noms global avec l'alias
                 del caller_globals[alias]

            elif from_imports != True and from_imports != False:
                # Importer des éléments spécifiques
                for name in from_imports:
                    del caller_globals[name]
            else:
                raise ValueError("La seconde valeur doit être True ou une liste de noms d'attributs et pas False.")

            print(f"{module} enlevé avec succès.")
    except Exception as e:
        print(f"Erreur : {module} n'est pas installé et ne peut pas être enlevé. \n{e}")
        result = input("Voulez-vous l'installer ? (y/n) : ")
        install(module) if result.lower() == 'y' else print("Annulé.")

      
if __name__ == "__main__":

    # install_and_import(('PIL.Image', True, 'Image'), ('customtkinter', True, 'ctk'), ('pathlib', 'Path', False), ('os', True, 'os'),
    #                   (colorsys, True, False))


    # image = Image.new('RGB', (100, 100), color='red')
    # image.show()  # Affiche l'image rouge
    # path = Path(__file__).parent.absolute() / "img.png"
    # image.save(path)

    # # Créer une nouvelle image (en mode RGB, 100x100 pixels, couleur rouge)
    # root = ctk.CTk()
    # root.geometry("300x200")
    # root.title("Hello World")
    # label = ctk.CTkLabel(root, text="Hello World")
    # label.pack()
    # root.mainloop()

    # os.system(f"start {path}")

    importation(("customtkinter", True, "ctk"), ("colorsys", True, False))

    color_window = ctk.CTkToplevel()
    color_window.title("Choisir une couleur")
    color_window.geometry("800x500")
    color_window.resizable(False, False)

     # Organisation générale avec Frames
    main_frame = ctk.CTkFrame(color_window)
    main_frame.pack(padx=10, pady=10, fill="both")

    left_frame = ctk.CTkFrame(main_frame)
    left_frame.grid(row=0, column=0, sticky="n")

    canvas = ctk.CTkCanvas(left_frame, width=600, height=200)
    for x in range(600):
        for y in range(200):
            hue = x / 600
            sat = y / 200
            r, g, b = colorsys.hls_to_rgb(hue, 0.5, sat)
            color = f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'
            canvas.create_line(x, y, x + 1, y, fill=color)    