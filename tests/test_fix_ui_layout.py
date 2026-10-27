"""
Regression test for Issue #17: UI Layout & Sticky Footer Fix
"""
import os
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def test_layout_css_does_not_contain_absolute_footer():
    layout_css_path = os.path.join(REPO_ROOT, "Views", "Shared", "_Layout.cshtml.css")
    assert os.path.exists(layout_css_path), f"{layout_css_path} must exist"
    
    with open(layout_css_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Verify absolute positioning has been removed from footer
    assert "position: absolute;" not in content, "Footer must not use position: absolute"
    # Verify white-space nowrap has been replaced
    assert "white-space: nowrap;" not in content, "Footer must not force white-space: nowrap"
    # Verify navbar-brand does not break letters abruptly
    assert "word-break: break-all;" not in content, "Navbar brand should not use break-all"


def test_site_css_implements_flex_sticky_footer():
    site_css_path = os.path.join(REPO_ROOT, "wwwroot", "css", "site.css")
    assert os.path.exists(site_css_path), f"{site_css_path} must exist"
    
    with open(site_css_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    assert "display: flex;" in content, "site.css body must use flexbox"
    assert "flex-direction: column;" in content, "site.css body must use flex-direction: column"
    assert "min-height: 100vh;" in content, "site.css body must have min-height: 100vh"
    assert "margin-bottom: 60px;" not in content, "site.css must remove fixed margin-bottom: 60px"


class TestFixUiLayout(unittest.TestCase):
    def test_layout_css_does_not_contain_absolute_footer(self):
        test_layout_css_does_not_contain_absolute_footer()

    def test_site_css_implements_flex_sticky_footer(self):
        test_site_css_implements_flex_sticky_footer()


if __name__ == "__main__":
    unittest.main()
