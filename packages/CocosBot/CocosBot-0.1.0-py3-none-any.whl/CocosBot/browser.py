from playwright.sync_api import sync_playwright
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PlaywrightBrowser:

    DEFAULT_TIMEOUT = 10000

    def __init__(self, headless=False):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.page = self.browser.new_page()
        logger.info("Navegador y página iniciados.")

    def __enter__(self):
        """Método para usar la clase con 'with'."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra el navegador al salir del bloque 'with'."""
        self.close_browser()

    def close_browser(self):
        """Cierra el navegador y el contexto Playwright."""
        self.browser.close()
        self.playwright.stop()
        logger.info("Navegador cerrado.")

    def go_to(self, url, log_message=None):  # Agrega log_message
        """Navega a una URL específica."""
        self.page.goto(url)
        if log_message:
            logger.info(log_message)
        else:
            logger.info(f"Navegado a {url}")

    def wait_for_element(self, selector, log_message=None, timeout=None):
        """Espera a que un elemento sea visible."""
        timeout = timeout or self.DEFAULT_TIMEOUT
        self.page.wait_for_selector(selector, timeout=timeout, state="visible")
        logger.info(f"Elemento encontrado: {selector}")
        if log_message:
            logger.info(log_message)

    def click_element(self, selector, log_message=None, timeout=None):
        """Espera a que un elemento sea visible y hace clic en él."""
        self.wait_for_element(selector, timeout)
        self.page.click(selector)
        logger.info(f"Clic en el elemento: {selector}")
        if log_message:
            logger.info(log_message)

    def fill_input(self, selector, value, log_message=None, timeout=None):
        """Espera a que un input sea visible y lo llena con un valor."""
        self.wait_for_element(selector, timeout)
        self.page.fill(selector, value)
        logger.info(f"Input {selector} llenado con el valor: {value}")
        if log_message:
            logger.info(log_message)

    def get_text_content(self, selector, timeout=None):
        """Obtiene el contenido de texto de un elemento."""
        self.wait_for_element(selector, timeout)
        text = self.page.text_content(selector)
        logger.info(f"Contenido de texto del elemento {selector}: {text}")
        return text

    def take_screenshot(self, filename="screenshot.png"):
        """Toma una captura de pantalla de la página actual."""
        self.page.screenshot(path=filename)
        logger.info(f"Captura de pantalla guardada en: {filename}")