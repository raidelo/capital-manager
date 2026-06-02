# Guía de Diseño TUI para CapMan

## 1. ESTRUCTURA BÁSICA

Una buena TUI tiene esta estructura:

```
┌─────────────────────────────────────────────────────┐
│ HEADER (Título app + hora)                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  CONTENIDO PRINCIPAL (Paneles, Tablas, Gráficos)   │
│                                                     │
├─────────────────────────────────────────────────────┤
│ ACCIONES (Botones)                                  │
├─────────────────────────────────────────────────────┤
│ STATUS BAR (Mensajes de estado)                     │
├─────────────────────────────────────────────────────┤
│ FOOTER (Atajos: [Q] Salir | [?] Ayuda)             │
└─────────────────────────────────────────────────────┘
```

## 2. PALETA DE COLORES RECOMENDADA

### Opción 1: Profesional (Defecto Textual)
- **Fondo**: Negro/Gris oscuro (`$surface`)
- **Paneles**: Gris más claro (`$panel`)
- **Acento principal**: Cian/Azul (`$accent`)
- **Éxito**: Verde
- **Error/Alerta**: Rojo
- **Advertencia**: Amarillo

### Opción 2: Moderna
```python
CSS = """
Screen {
    background: $panel;
    color: $text;
}
```

## 3. COMPONENTES PRINCIPALES

### Header
```python
from textual.widgets import Header
yield Header(show_clock=True)
```
- Siempre en la parte superior
- Muestra título + reloj
- Ayuda con orientación

### Contenido (Layouts)
```python
# Disposición vertical (recomendada)
with Vertical():
    yield AccountListPanel()
    yield TransactionListPanel()

# Disposición horizontal (para pantallas anchas)
with Horizontal():
    yield AccountListPanel()
    yield TransactionListPanel()
```

### DataTable (Para listas)
```python
from textual.widgets import DataTable

table = DataTable()
table.add_columns("ID", "Nombre", "Saldo")
table.add_row("001", "Checking", "$1,000")
yield table
```

### Botones de Acción
```python
with Horizontal():
    yield Button("➕ Nueva Cuenta", id="new-account")
    yield Button("📝 Nueva Transacción", id="new-transaction")
```

### Barra de Estado
```python
class StatusBar(Static):
    message = reactive("Ready")
    
    def render(self):
        return f"[dim]{self.message}[/dim]"
```

## 4. PRINCIPIOS DE DISEÑO

### ✅ Haz esto:

1. **Usa Bordes y Espacios**
   ```python
   DEFAULT_CSS = """
   MyWidget {
       border: solid $accent;
       padding: 1;
   }
   """
   ```

2. **Separa Conceptos Visualmente**
   - Cuentas en un panel
   - Transacciones en otro
   - Acciones en una barra

3. **Usa Iconos Emoji**
   - 📊 Cuentas
   - 💳 Transacciones
   - ➕ Agregar
   - 🔍 Buscar
   - ⚙️ Configurar

4. **Feedback Visual**
   - Mensaje de estado cuando algo ocurre
   - Cambios de color en botones al hover
   - Indicadores de éxito/error

5. **Accesos Rápidos (Bindings)**
   ```python
   BINDINGS = [
       Binding("q", "quit", "Salir"),
       Binding("n", "new_account", "Nueva Cuenta"),
       Binding("?", "show_help", "Ayuda"),
   ]
   ```

### ❌ Evita esto:

1. **Demasiados colores** → Máximo 3-4
2. **Paneles sin bordes** → Sin estructura visual
3. **Texto sin espacios** → Difícil de leer
4. **Botones desorganizados** → Confusión en el usuario
5. **Sin feedback** → Usuario no sabe qué pasó

## 5. FLUJO DE INTERACCIÓN

```
Usuario inicia app
    ↓
Header + Status Bar muestra estado
    ↓
Usuario ve cuentas y transacciones
    ↓
Usuario presiona botón o atajo (ej: 'n')
    ↓
Modal abre para crear nueva cuenta
    ↓
Usuario completa datos
    ↓
API se llama (call REST)
    ↓
Status bar actualiza con resultado
    ↓
Tabla se refresca automáticamente
```

## 6. EJEMPLO: PANEL DE CUENTAS

```python
class AccountListPanel(Static):
    DEFAULT_CSS = """
    AccountListPanel {
        width: 1fr;
        height: 1fr;
        border: solid $accent;
        padding: 1;
    }
    """
    
    def compose(self) -> ComposeResult:
        # Título del panel
        yield Label("[bold]📊 Cuentas[/bold]")
        
        # Tabla con datos
        table = DataTable()
        table.add_columns("ID", "Nombre", "Saldo", "Estado")
        table.add_row("acc001", "Checking", "$2,450.00", "✓ Activa")
        yield table
```

**Análisis de diseño:**
- `border: solid $accent` → Separa visualmente
- `[bold]` → Hace el título importante
- Emoji al inicio → Contexto inmediato
- Columnas claras → Estructura
- Status con símbolo → Visual feedback

## 7. CONECTAR CON TU API REST

```python
from textual.binding import Binding

class CapManApp(App):
    BINDINGS = [
        Binding("n", "create_account", "Nueva Cuenta"),
    ]
    
    def action_create_account(self) -> None:
        """Abre modal para crear cuenta"""
        self.push_screen(NewAccountModal())
    
    def on_account_created(self, account_data) -> None:
        """Callback cuando se crea una cuenta"""
        # Llamar tu REST API
        response = requests.post(
            "http://localhost:8000/accounts",
            json=account_data
        )
        
        # Actualizar status
        status = self.query_one(StatusBar)
        status.message = f"✓ Cuenta '{account_data['name']}' creada"
        
        # Refrescar tabla
        self.refresh_accounts()
```

## 8. TEMA OSCURO vs CLARO

Textual por defecto usa tema oscuro (recomendado para terminal).

Si quieres modificar colores:

```python
CSS = """
Screen {
    background: $surface;
    color: $text;
}

Button {
    background: $accent;
    color: $text;
}

Button:hover {
    background: $warn;
}
"""
```

## 9. INSTALA TEXTUAL

```bash
pip install textual
```

Para ejecutar el ejemplo:
```bash
python capman_tui_example.py
```

## 10. CHECKLIST DE DISEÑO

- [ ] ¿Hay un Header claro?
- [ ] ¿Está dividido en secciones (paneles)?
- [ ] ¿Tienen bordes los paneles?
- [ ] ¿Hay espacios (padding) dentro de paneles?
- [ ] ¿Los botones están organizados?
- [ ] ¿Hay una barra de estado para feedback?
- [ ] ¿Hay un Footer con atajos?
- [ ] ¿Se ven iconos emoji para contexto?
- [ ] ¿Máximo 3-4 colores?
- [ ] ¿El contraste es legible?

---

**Tu siguiente paso:** Adapta el ejemplo a tu CLI `capman` con tus propios comandos y datos reales de la API REST.
