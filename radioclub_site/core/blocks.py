from wagtail.blocks import (
    BooleanBlock,
    CharBlock,
    ChoiceBlock,
    ListBlock,
    RawHTMLBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    URLBlock,
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import PageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock


class HeadingBlock(StructBlock):
    """A heading block with selectable level (h2-h4)."""

    heading_level = ChoiceBlock(
        choices=[
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
        ],
        default="h2",
        help_text="Nivel del encabezado",
    )
    text = CharBlock(required=True, help_text="Texto del encabezado")

    class Meta:
        icon = "title"
        template = "core/blocks/heading_block.html"
        label = "Encabezado"


class ImageBlock(StructBlock):
    """An image block with optional caption and attribution."""

    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False, help_text="Pie de imagen")
    attribution = CharBlock(required=False, help_text="Atribución de la imagen")

    class Meta:
        icon = "image"
        template = "core/blocks/image_block.html"
        label = "Imagen"


class LinkBlock(StructBlock):
    """A link block with text, optional URL or page, and new tab option."""

    text = CharBlock(required=True, help_text="Texto del enlace")
    url = URLBlock(required=False, help_text="URL externa (opcional)")
    page = PageChooserBlock(required=False, help_text="Página interna (opcional)")
    open_in_new_tab = BooleanBlock(
        required=False, default=False, help_text="Abrir en nueva pestaña"
    )

    class Meta:
        icon = "link"
        label = "Enlace"


class CalloutBlock(StructBlock):
    """A callout/alert block with colored background."""

    text = RichTextBlock(
        features=["bold", "italic", "link"],
        help_text="Texto del aviso",
    )
    background_color = ChoiceBlock(
        choices=[
            ("info", "Información (azul)"),
            ("success", "Éxito (verde)"),
            ("warning", "Advertencia (amarillo)"),
            ("danger", "Peligro (rojo)"),
        ],
        default="info",
        help_text="Color de fondo del aviso",
    )

    class Meta:
        icon = "warning"
        template = "core/blocks/callout_block.html"
        label = "Aviso destacado"


class ButtonBlock(StructBlock):
    """A button block with style options."""

    text = CharBlock(required=True, help_text="Texto del botón")
    url = URLBlock(required=False, help_text="URL externa (opcional)")
    page = PageChooserBlock(required=False, help_text="Página interna (opcional)")
    open_in_new_tab = BooleanBlock(
        required=False, default=False, help_text="Abrir en nueva pestaña"
    )
    style = ChoiceBlock(
        choices=[
            ("primary", "Primario"),
            ("secondary", "Secundario"),
            ("outline", "Contorno"),
        ],
        default="primary",
        help_text="Estilo del botón",
    )

    class Meta:
        icon = "placeholder"
        template = "core/blocks/button_block.html"
        label = "Botón"


class CardBlock(StructBlock):
    """A card block with optional image, title, text, and link."""

    image = ImageChooserBlock(required=False)
    title = CharBlock(required=True, help_text="Título de la tarjeta")
    text = RichTextBlock(
        features=["bold", "italic", "link"],
        help_text="Contenido de la tarjeta",
    )
    link = LinkBlock(required=False)

    class Meta:
        icon = "doc-full"
        template = "core/blocks/card_block.html"
        label = "Tarjeta"


class BaseStreamBlock(StreamBlock):
    """The base StreamBlock used throughout the site."""

    heading = HeadingBlock()
    paragraph = RichTextBlock(
        features=[
            "bold",
            "italic",
            "ol",
            "ul",
            "hr",
            "link",
            "document-link",
            "image",
            "embed",
            "h2",
            "h3",
            "h4",
            "blockquote",
        ],
        icon="pilcrow",
        label="Párrafo",
    )
    image = ImageBlock()
    callout = CalloutBlock()
    button = ButtonBlock()
    cards = ListBlock(CardBlock(), icon="list-ul", label="Tarjetas")
    embed = EmbedBlock(
        icon="media",
        label="Contenido embebido",
        help_text="Inserta una URL de YouTube, Vimeo, etc.",
    )
    table = TableBlock(template="core/blocks/table_block.html", label="Tabla")
    raw_html = RawHTMLBlock(
        icon="code",
        label="HTML sin procesar",
        help_text="Usa con precaución. No se valida el contenido HTML.",
    )

    class Meta:
        label = "Contenido"
