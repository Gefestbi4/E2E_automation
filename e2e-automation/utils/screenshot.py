"""
Screenshot manager for E2E automation tests
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver
from utils.logger import TestLogger


class ScreenshotManager:
    """Manager for taking and organizing screenshots during tests"""

    def __init__(self):
        self.logger = TestLogger("ScreenshotManager")
        self.screenshots_dir = Path("/app/screenshots")
        self.screenshots_dir.mkdir(exist_ok=True)

        # Create subdirectories
        self.failure_dir = self.screenshots_dir / "failures"
        self.success_dir = self.screenshots_dir / "success"
        self.step_dir = self.screenshots_dir / "steps"

        for directory in [self.failure_dir, self.success_dir, self.step_dir]:
            directory.mkdir(exist_ok=True)

    def take_screenshot(
        self, driver: WebDriver, name: str = "screenshot", category: str = "step"
    ) -> str:
        """
        Take screenshot and save to appropriate directory

        Args:
            driver: WebDriver instance
            name: Screenshot name
            category: Category (failure, success, step)

        Returns:
            Path to saved screenshot
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"{name}_{timestamp}.png"

            # Select directory based on category
            if category == "failure":
                directory = self.failure_dir
            elif category == "success":
                directory = self.success_dir
            else:
                directory = self.step_dir

            screenshot_path = directory / filename

            # Take screenshot
            driver.save_screenshot(str(screenshot_path))

            self.logger.screenshot(str(screenshot_path))
            return str(screenshot_path)

        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
            raise

    def take_element_screenshot(
        self, driver: WebDriver, element, name: str = "element_screenshot"
    ) -> str:
        """
        Take screenshot of specific element

        Args:
            driver: WebDriver instance
            element: WebElement to screenshot
            name: Screenshot name

        Returns:
            Path to saved screenshot
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"{name}_{timestamp}.png"
            screenshot_path = self.step_dir / filename

            # Take element screenshot
            element.screenshot(str(screenshot_path))

            self.logger.screenshot(str(screenshot_path))
            return str(screenshot_path)

        except Exception as e:
            self.logger.error(f"Failed to take element screenshot: {str(e)}")
            raise

    def take_full_page_screenshot(
        self, driver: WebDriver, name: str = "full_page_screenshot"
    ) -> str:
        """
        Take full page screenshot (including scrolled content)

        Args:
            driver: WebDriver instance
            name: Screenshot name

        Returns:
            Path to saved screenshot
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"{name}_{timestamp}.png"
            screenshot_path = self.step_dir / filename

            # Get page dimensions
            total_width = driver.execute_script("return document.body.scrollWidth")
            total_height = driver.execute_script("return document.body.scrollHeight")

            # Set window size to full page
            driver.set_window_size(total_width, total_height)

            # Take screenshot
            driver.save_screenshot(str(screenshot_path))

            # Restore original window size
            driver.set_window_size(1920, 1080)

            self.logger.screenshot(str(screenshot_path))
            return str(screenshot_path)

        except Exception as e:
            self.logger.error(f"Failed to take full page screenshot: {str(e)}")
            raise

    def cleanup_old_screenshots(self, days: int = 7):
        """
        Clean up screenshots older than specified days

        Args:
            days: Number of days to keep screenshots
        """
        try:
            cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)

            for directory in [self.failure_dir, self.success_dir, self.step_dir]:
                for file_path in directory.iterdir():
                    if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                        file_path.unlink()
                        self.logger.debug(f"Deleted old screenshot: {file_path}")

        except Exception as e:
            self.logger.error(f"Failed to cleanup old screenshots: {str(e)}")

    def get_screenshot_count(self, category: str = "all") -> dict:
        """
        Get count of screenshots by category

        Args:
            category: Category to count (all, failure, success, step)

        Returns:
            Dictionary with screenshot counts
        """
        try:
            counts = {}

            if category == "all" or category == "failure":
                counts["failure"] = len(list(self.failure_dir.glob("*.png")))

            if category == "all" or category == "success":
                counts["success"] = len(list(self.success_dir.glob("*.png")))

            if category == "all" or category == "step":
                counts["step"] = len(list(self.step_dir.glob("*.png")))

            if category == "all":
                counts["total"] = sum(counts.values())

            return counts

        except Exception as e:
            self.logger.error(f"Failed to get screenshot count: {str(e)}")
            return {}

    def get_latest_screenshot(self, category: str = "step") -> Optional[str]:
        """
        Get path to latest screenshot in category

        Args:
            category: Category to search (failure, success, step)

        Returns:
            Path to latest screenshot or None
        """
        try:
            if category == "failure":
                directory = self.failure_dir
            elif category == "success":
                directory = self.success_dir
            else:
                directory = self.step_dir

            png_files = list(directory.glob("*.png"))
            if png_files:
                latest_file = max(png_files, key=lambda x: x.stat().st_mtime)
                return str(latest_file)

            return None

        except Exception as e:
            self.logger.error(f"Failed to get latest screenshot: {str(e)}")
            return None

    def create_screenshot_report(self) -> str:
        """
        Create HTML report of all screenshots

        Returns:
            Path to HTML report
        """
        try:
            report_path = self.screenshots_dir / "screenshot_report.html"

            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Screenshot Report</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    .category { margin-bottom: 30px; }
                    .category h2 { color: #333; border-bottom: 2px solid #ccc; }
                    .screenshot { margin: 10px 0; }
                    .screenshot img { max-width: 800px; border: 1px solid #ddd; }
                    .screenshot p { margin: 5px 0; font-size: 12px; color: #666; }
                </style>
            </head>
            <body>
                <h1>Screenshot Report</h1>
                <p>Generated: {timestamp}</p>
            """.format(
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            # Add screenshots by category
            for category, directory in [
                ("Failures", self.failure_dir),
                ("Success", self.success_dir),
                ("Steps", self.step_dir),
            ]:
                html_content += f'<div class="category"><h2>{category}</h2>'

                png_files = sorted(
                    directory.glob("*.png"),
                    key=lambda x: x.stat().st_mtime,
                    reverse=True,
                )

                for file_path in png_files:
                    relative_path = file_path.relative_to(self.screenshots_dir)
                    file_time = datetime.fromtimestamp(file_path.stat().st_mtime)

                    html_content += f"""
                    <div class="screenshot">
                        <img src="{relative_path}" alt="{file_path.name}">
                        <p>{file_path.name} - {file_time.strftime("%Y-%m-%d %H:%M:%S")}</p>
                    </div>
                    """

                html_content += "</div>"

            html_content += "</body></html>"

            with open(report_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            self.logger.info(f"Screenshot report created: {report_path}")
            return str(report_path)

        except Exception as e:
            self.logger.error(f"Failed to create screenshot report: {str(e)}")
            raise
