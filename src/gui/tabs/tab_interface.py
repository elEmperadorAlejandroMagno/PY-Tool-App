"""
Interfaz base para todas las pestañas de la aplicación.

Define la estructura común que deben seguir todas las implementaciones
de pestañas para mantener consistencia y facilitar el mantenimiento.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
import customtkinter as ctk


class TabInterface(ABC):
    """Interfaz abstracta para todas las pestañas de la aplicación."""
    
    def __init__(self, parent_frame: ctk.CTkFrame, app: Any, t: Dict[str, Any]) -> None:
        """
        Inicializa la pestaña.
        
        Args:
            parent_frame: El frame padre donde se renderizará la pestaña
            app: La instancia de la aplicación principal
            t: Diccionario de traducciones
        """
        self.parent_frame = parent_frame
        self.app = app
        self.t = t
        self.content_frame: ctk.CTkFrame = None
        
    @abstractmethod
    def render(self) -> None:
        """
        Renderiza el contenido de la pestaña.
        Debe ser implementado por cada pestaña específica.
        """
        pass
        
    def create_content_frame(self) -> ctk.CTkFrame:
        """
        Crea el frame principal de contenido con padding estándar.
        
        Returns:
            CTkFrame configurado con padding
        """
        content_frame = ctk.CTkFrame(self.parent_frame)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        return content_frame
        
    def create_language_menu(self, parent: ctk.CTkFrame, values: list, 
                           variable: ctk.StringVar, command: callable,
                           width: int = 200, height: int = 32) -> ctk.CTkOptionMenu:
        """
        Crea un menú de idiomas estandarizado.
        
        Args:
            parent: Frame padre
            values: Lista de valores para el menú
            variable: Variable StringVar asociada
            command: Función callback
            width: Ancho del menú
            height: Altura del menú
            
        Returns:
            CTkOptionMenu configurado
        """
        return ctk.CTkOptionMenu(
            parent,
            values=values,
            variable=variable,
            command=command,
            width=width,
            height=height,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        
    def create_label(self, parent: ctk.CTkFrame, text: str, 
                    size: int = 14, bold: bool = True) -> ctk.CTkLabel:
        """
        Crea una etiqueta estandarizada.
        
        Args:
            parent: Frame padre
            text: Texto de la etiqueta
            size: Tamaño de fuente
            bold: Si la fuente debe ser en negrita
            
        Returns:
            CTkLabel configurado
        """
        font_weight = "bold" if bold else "normal"
        return ctk.CTkLabel(
            parent, 
            text=text, 
            font=ctk.CTkFont(size=size, weight=font_weight)
        )
        
    def create_textbox(self, parent: ctk.CTkFrame, width: int = 700, 
                      height: int = 120, font_size: int = 16,
                      font_family: str = None) -> ctk.CTkTextbox:
        """
        Crea un textbox estandarizado.
        
        Args:
            parent: Frame padre
            width: Ancho del textbox
            height: Altura del textbox
            font_size: Tamaño de fuente
            font_family: Familia de fuente opcional
            
        Returns:
            CTkTextbox configurado
        """
        font_kwargs = {"size": font_size}
        if font_family:
            font_kwargs["family"] = font_family
            
        return ctk.CTkTextbox(
            parent, 
            width=width, 
            height=height, 
            font=ctk.CTkFont(**font_kwargs)
        )
        
    def create_button(self, parent: ctk.CTkFrame, text: str, command: callable,
                     width: int = 200, height: int = 40, 
                     font_size: int = 14, bold: bool = True) -> ctk.CTkButton:
        """
        Crea un botón estandarizado.
        
        Args:
            parent: Frame padre
            text: Texto del botón
            command: Función callback
            width: Ancho del botón
            height: Altura del botón
            font_size: Tamaño de fuente
            bold: Si la fuente debe ser en negrita
            
        Returns:
            CTkButton configurado
        """
        font_weight = "bold" if bold else "normal"
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            width=width,
            height=height,
            font=ctk.CTkFont(size=font_size, weight=font_weight)
        )