import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QLineEdit, QTabWidget, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the browser
        self.browser_tabs = QTabWidget()
        self.browser_tabs.setDocumentMode(True)
        self.browser_tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.browser_tabs.currentChanged.connect(self.current_tab_changed)
        self.browser_tabs.setTabsClosable(True)
        self.browser_tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setCentralWidget(self.browser_tabs)

        # Create the first tab
        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')

        # Create a navigation toolbar
        self.navbar = QToolBar()
        self.addToolBar(self.navbar)

        # Add a back button
        back_btn = QAction("Back", self)
        back_btn.triggered.connect(lambda: self.browser_tabs.currentWidget().back())
        self.navbar.addAction(back_btn)

        # Add a forward button
        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(lambda: self.browser_tabs.currentWidget().forward())
        self.navbar.addAction(forward_btn)

        # Add a reload button
        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(lambda: self.browser_tabs.currentWidget().reload())
        self.navbar.addAction(reload_btn)

        # Add a home button
        home_btn = QAction("Home", self)
        home_btn.triggered.connect(self.navigate_home)
        self.navbar.addAction(home_btn)

        # Add a URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navbar.addWidget(self.url_bar)

        # Add a new tab button
        new_tab_btn = QAction("New Tab", self)
        new_tab_btn.triggered.connect(lambda: self.add_new_tab(QUrl('http://www.google.com')))
        self.navbar.addAction(new_tab_btn)

        # Apply dark mode and custom styling
        self.apply_dark_mode()

        # Set window title and show the main window
        self.setWindowTitle("Kawser")
        self.show()

    def add_new_tab(self, qurl=None, label="Blank"):
        if not isinstance(qurl, QUrl):
            qurl = QUrl('http://www.google.com')

        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.browser_tabs.addTab(browser, label)
        self.browser_tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.browser_tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:  # No tab under the click
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.browser_tabs.currentWidget().url()
        print("Current tab changed:", qurl.toString())  # Debug print
        self.update_urlbar(qurl, self.browser_tabs.currentWidget())
        self.update_title(self.browser_tabs.currentWidget())

    def close_current_tab(self, i):
        if self.browser_tabs.count() > 1:
            self.browser_tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.browser_tabs.currentWidget():
            return

        title = self.browser_tabs.currentWidget().page().title()
        self.setWindowTitle(f"{title} - Kawser")

    def navigate_home(self):
        self.browser_tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.browser_tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser=None):
        if browser != self.browser_tabs.currentWidget():
            return

        print("Updating URL bar:", q.toString())  # Debug print
        if hasattr(self, 'url_bar'):
            self.url_bar.setText(q.toString())
            self.url_bar.setCursorPosition(0)
        else:
            print("Error: url_bar not found")  # Debug print

    def apply_dark_mode(self):
        dark_mode_style = """
            QMainWindow {
                background-color: #2b2b2b;
            }
            QToolBar {
                background-color: #3c3c3c;
                spacing: 5px;
            }
            QLineEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3c3c3c;
                padding: 2px;
            }
            QToolButton {
                background-color: #3c3c3c;
                color: #ffffff;
                border: none;
                padding: 5px;
            }
            QToolButton:pressed {
                background-color: #5c5c5c;
            }
            QTabWidget::pane { 
                border: 1px solid #3c3c3c; 
            }
            QTabBar::tab {
                background: #3c3c3c;
                color: #ffffff;
                padding: 10px;
            }
            QTabBar::tab:selected, QTabBar::tab:hover {
                background: #5c5c5c;
            }
        """
        self.setStyleSheet(dark_mode_style)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Kawser")
    window = Browser()
    sys.exit(app.exec_())
