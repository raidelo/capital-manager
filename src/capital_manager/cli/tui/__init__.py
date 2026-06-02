"""
CapMan TUI - Un ejemplo de interfaz terminal bien diseñada con Textual.

Principios aplicados:
1. Estructura clara: Header + Content + Footer
2. Paleta limitada: Verde (éxito), Rojo (error), Azul (info)
3. Bordes y espacios para separar secciones
4. Acciones claramente etiquetadas
"""

from textual.app import ComposeResult, RenderableType
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual.widgets import Button, DataTable, Footer, Header, Label, Static


class TitleBox(Static):
    """Caja de título estilizada"""

    DEFAULT_CSS = """
    TitleBox {
        width: 100%;
        height: auto;
        background: $panel;
        border: thick $accent;
        padding: 1 2;
        text-align: center;
    }
    """

    def __init__(self, title: str):
        super().__init__()
        self.title_text = title

    def render(self) -> RenderableType:
        return f"[bold cyan]▶[/bold cyan] {self.title_text}"


class StatusBar(Static):
    """Barra de estado inferior"""

    message = reactive("Ready")

    DEFAULT_CSS = """
    StatusBar {
        width: 100%;
        height: 1;
        background: $panel;
        border-top: solid $accent;
        padding: 0 2;
        text-align: left;
    }
    """

    def render(self) -> RenderableType:
        return f"[dim]{self.message}[/dim]"


class AccountListPanel(Static):
    """Panel que muestra la lista de cuentas"""

    DEFAULT_CSS = """
    AccountListPanel {
        width: 1fr;
        height: 1fr;
        border: solid $accent;
        padding: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("[bold]📊 Cuentas[/bold]")

        # Tabla simulada
        table = DataTable()
        yield table

        # Agregar columnas
        table.add_columns("ID", "Nombre", "Saldo", "Estado")

        # Datos de ejemplo
        table.add_row("acc001", "Checking", "$2,450.00", "✓ Activa")
        table.add_row("acc002", "Savings", "$15,800.50", "✓ Activa")
        table.add_row("acc003", "Investment", "$45,320.00", "⚠ Pendiente")


class TransactionListPanel(Static):
    """Panel que muestra transacciones"""

    DEFAULT_CSS = """
    TransactionListPanel {
        width: 1fr;
        height: 1fr;
        border: solid $accent;
        padding: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("[bold]💳 Transacciones Recientes[/bold]")

        table = DataTable()
        yield table

        table.add_columns("Fecha", "Descripción", "Monto", "Tipo")
        table.add_row("2025-04-19", "Depósito", "+$500.00", "[green]IN[/green]")
        table.add_row("2025-04-18", "Compra en línea", "-$89.99", "[red]OUT[/red]")
        table.add_row("2025-04-17", "Transferencia", "+$1,200.00", "[green]IN[/green]")


class ActionsPanel(Static):
    """Panel de acciones/controles"""

    DEFAULT_CSS = """
    ActionsPanel {
        width: 100%;
        height: auto;
        border: solid $accent;
        padding: 1;
    }
    
    ActionsPanel Button {
        margin: 0 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("[bold cyan]Acciones[/bold cyan]")
        with Horizontal():
            yield Button("➕ Nueva Cuenta", id="new-account")
            yield Button("📝 Nueva Transacción", id="new-transaction")
            yield Button("🔍 Buscar", id="search")
            yield Button("⚙️ Configurar", id="settings")


class CapManTUI(ComposeResult):
    """Aplicación principal CapMan"""

    BINDINGS = [
        Binding("q", "quit", "Salir"),
        Binding("?", "show_help", "Ayuda"),
    ]

    CSS = """
    Screen {
        background: $surface;
        color: $text;
    }
    
    Header {
        background: $panel;
        border-bottom: thick $accent;
    }
    
    Footer {
        background: $panel;
        border-top: thick $accent;
    }
    
    Label {
        margin: 1 0;
    }
    """

    def compose(self) -> ComposeResult:
        """Componer la interfaz"""
        yield Header(show_clock=True)

        with Container():
            # Título
            yield TitleBox("CapMan - Gestor de Finanzas")

            # Panel principal con dos columnas
            with Horizontal():
                yield AccountListPanel()
                yield TransactionListPanel()

            # Panel de acciones
            yield ActionsPanel()

            # Barra de estado
            yield StatusBar()

        yield Footer()

    def on_mount(self) -> None:
        """Al iniciar la aplicación"""
        status = self.query_one(StatusBar)
        status.message = "✓ Aplicación iniciada. Presiona [?] para ayuda"

    def action_show_help(self) -> None:
        """Mostrar ayuda"""
        status = self.query_one(StatusBar)
        status.message = "Q: Salir | ?: Ayuda | Usa Tab para navegar"


def app():
    from textual.app import App

    class CapManApp(App):
        """Wrapper para ejecutar la aplicación"""

        BINDINGS = [
            Binding("q", "quit", "Salir"),
            Binding("?", "show_help", "Ayuda"),
        ]

        CSS = """
        Screen {
            background: $surface;
            color: $text;
        }
        """

        def compose(self) -> ComposeResult:
            yield Header(show_clock=True)

            with Container():
                yield TitleBox("CapMan - Gestor de Finanzas")

                with Horizontal():
                    yield AccountListPanel()
                    yield TransactionListPanel()

                yield ActionsPanel()
                yield StatusBar()

            yield Footer()

        def on_mount(self) -> None:
            status = self.query_one(StatusBar)
            status.message = "✓ Aplicación iniciada. Presiona [?] para ayuda"

        def action_show_help(self) -> None:
            status = self.query_one(StatusBar)
            status.message = "Q: Salir | ?: Ayuda | Usa Tab para navegar"

    app = CapManApp()
    app.run()


if __name__ == "__main__":
    app()
