import asyncio
import typer
import shutil
import subprocess
from pathlib import Path
from typing import Optional, List, Set
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import qbittorrentapi
from asyncio import Semaphore

app = typer.Typer()
console = Console()


class TorrentDownloader:
    def __init__(self, output_dir: Path, proxy: Optional[str] = None):
        self.output_dir = output_dir
        self._ensure_qbittorrent_running()
        try:
            self.qbt_client = qbittorrentapi.Client(
                host="localhost",
                port=8080,
                username="admin",
                password="adminadmin",
                VERIFY_WEBUI_CERTIFICATE=False,
            )
            # Test connection
            self.qbt_client.auth_log_in()

            if proxy:
                self._setup_proxy(proxy)

        except qbittorrentapi.LoginFailed as e:
            console.print(f"Failed to login to qBittorrent: {str(e)}", style="red")
            raise typer.Exit(1)
        except qbittorrentapi.APIConnectionError:
            console.print(
                "Cannot connect to qBittorrent. Make sure it's running and Web UI is enabled.",
                style="red",
            )
            raise typer.Exit(1)

        self.semaphore = Semaphore(5)  # Limit to 5 concurrent downloads

    def _ensure_qbittorrent_running(self):
        """Ensure qBittorrent is running and Web UI is enabled."""
        import platform
        import time
        from pathlib import Path

        if platform.system() == "Darwin":  # macOS
            qbittorrent_path = (
                "/Applications/qBittorrent.app/Contents/MacOS/qbittorrent"
            )
            process_name = "qbittorrent"
            config_path = (
                Path.home() / "Library/Application Support/qBittorrent/qBittorrent.ini"
            )
        elif platform.system() == "Windows":
            qbittorrent_path = shutil.which("qbittorrent.exe")
            process_name = "qbittorrent.exe"
            config_path = Path.home() / "AppData/Roaming/qBittorrent/qBittorrent.ini"
        else:  # Linux and others
            qbittorrent_path = shutil.which("qbittorrent")
            process_name = "qbittorrent"
            config_path = Path.home() / ".config/qBittorrent/qBittorrent.conf"

        # Check if qbittorrent exists
        if not (
            Path(qbittorrent_path).exists()
            if platform.system() == "Darwin"
            else qbittorrent_path
        ):
            console.print(
                "qBittorrent is not installed. Please install it first:", style="red"
            )
            if platform.system() == "Darwin":
                console.print("  brew install qbittorrent", style="yellow")
            elif platform.system() == "Windows":
                console.print(
                    "  Download from: https://www.qbittorrent.org/download.php",
                    style="yellow",
                )
            else:
                console.print(
                    "  sudo apt install qbittorrent  # or your system's package manager",
                    style="yellow",
                )
            raise typer.Exit(1)

        # Start qBittorrent if not running
        try:
            if platform.system() == "Windows":
                check_cmd = ["tasklist", "/FI", f"IMAGENAME eq {process_name}"]
                is_running = process_name in subprocess.check_output(check_cmd).decode()
            else:
                check_cmd = ["pgrep", process_name]
                is_running = (
                    subprocess.run(check_cmd, capture_output=True).returncode == 0
                )

            if not is_running:
                console.print("Starting qBittorrent...", style="yellow")
                if platform.system() == "Windows":
                    subprocess.Popen(
                        [qbittorrent_path], creationflags=subprocess.CREATE_NO_WINDOW
                    )
                elif platform.system() == "Darwin":
                    subprocess.Popen(["open", "-a", "qBittorrent"])
                else:
                    subprocess.Popen(
                        [qbittorrent_path],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )

                # Wait for qBittorrent to start
                time.sleep(5)

            # Check and enable Web UI if needed
            if config_path.exists():
                with open(config_path, "r") as f:
                    config_content = f.read()

                if "WebUI\\Enabled=true" not in config_content:
                    console.print(
                        "Web UI is not enabled. Please enable it:", style="yellow"
                    )
                    console.print("1. Open qBittorrent", style="yellow")
                    console.print(
                        "2. Go to Tools -> Preferences (or press ⌘ + , on macOS)",
                        style="yellow",
                    )
                    console.print(
                        "3. Click on 'Web UI' in the left sidebar", style="yellow"
                    )
                    console.print(
                        "4. Check 'Web User Interface (Remote Control)'", style="yellow"
                    )
                    console.print(
                        "5. Set username to 'admin' and password to 'adminadmin'",
                        style="yellow",
                    )
                    console.print("6. Click Apply and OK", style="yellow")

                    # Ask user to confirm
                    if not typer.confirm("Have you enabled the Web UI?"):
                        raise typer.Exit(1)

                    # Kill and restart qBittorrent to apply changes
                    if platform.system() == "Windows":
                        subprocess.run(["taskkill", "/F", "/IM", process_name])
                    else:
                        subprocess.run(["pkill", process_name])

                    time.sleep(2)

                    # Start qBittorrent again
                    if platform.system() == "Windows":
                        subprocess.Popen(
                            [qbittorrent_path],
                            creationflags=subprocess.CREATE_NO_WINDOW,
                        )
                    elif platform.system() == "Darwin":
                        subprocess.Popen(["open", "-a", "qBittorrent"])
                    else:
                        subprocess.Popen(
                            [qbittorrent_path],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )

                    time.sleep(5)  # Wait for restart

        except Exception as e:
            console.print(f"Failed to start qBittorrent: {str(e)}", style="red")
            raise typer.Exit(1)

    def _setup_proxy(self, proxy: str):
        try:
            ip, port = proxy.split(":")
            # Set qBittorrent proxy settings
            self.qbt_client.app.preferences = {
                "proxy_type": 3,  # 3 = SOCKS5
                "proxy_ip": ip,
                "proxy_port": int(port),
                "proxy_peer_connections": True,
                "proxy_auth_enabled": False,
                "proxy_torrents_only": True,
            }
        except Exception as e:
            console.print(f"Failed to set proxy: {str(e)}", style="red")
            raise typer.Exit(1)

    async def download_from_magnet_async(
        self, magnet_link: str, progress: Progress, task_id: int
    ) -> None:
        async with self.semaphore:
            try:
                progress.update(task_id, description="Adding magnet link...")

                # Add the torrent and get its hash
                result = self.qbt_client.torrents_add(urls=[magnet_link])
                if not result == "Ok.":
                    raise Exception("Failed to add magnet link")

                progress.update(task_id, description="Waiting for metadata...")

                # Wait for metadata and get torrent info
                max_attempts = 30
                attempts = 0
                while attempts < max_attempts:
                    torrents = self.qbt_client.torrents_info()
                    for torrent in torrents:
                        if magnet_link in torrent.magnet_uri:
                            file_path = self.output_dir / f"{torrent.name}.torrent"

                            # Export .torrent file
                            torrent_data = self.qbt_client.torrents_export(torrent.hash)
                            with open(file_path, "wb") as f:
                                f.write(torrent_data)

                            # Remove the torrent from qBittorrent
                            self.qbt_client.torrents_delete(
                                delete_files=False, torrent_hashes=[torrent.hash]
                            )

                            progress.update(
                                task_id, description=f"✓ Saved {file_path.name}"
                            )
                            return

                    await asyncio.sleep(1)
                    attempts += 1

                raise Exception("Timeout waiting for metadata")

            except Exception as e:
                progress.update(task_id, description=f"✗ Failed: {str(e)}")
                raise


def deduplicate_magnet_links(file_path: Path) -> List[str]:
    """Read magnet links from file and remove duplicates while preserving order."""
    seen: Set[str] = set()
    unique_links: List[str] = []
    duplicates = 0

    with open(file_path, "r") as f:
        for line in f:
            magnet = line.strip()
            if magnet and magnet not in seen:
                seen.add(magnet)
                unique_links.append(magnet)
            elif magnet:
                duplicates += 1

    if duplicates > 0:
        console.print(f"Removed {duplicates} duplicate magnet link(s)", style="yellow")

    return unique_links


async def process_magnets(downloader: TorrentDownloader, magnet_links: List[str]):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        # Create all tasks upfront
        tasks = {
            magnet: progress.add_task(description="Waiting to start...", total=None)
            for magnet in magnet_links
        }

        # Create and gather all download tasks
        download_tasks = [
            asyncio.create_task(
                downloader.download_from_magnet_async(magnet, progress, task_id)
            )
            for magnet, task_id in tasks.items()
        ]

        # Wait for all tasks to complete
        try:
            await asyncio.gather(*download_tasks)
        except Exception as e:
            console.print(f"An error occurred: {str(e)}", style="red")
            pass


@app.command()
def download(
    input_file: Path = typer.Option(
        ..., "--input", "-i", help="Path to text file containing magnet links"
    ),
    output_dir: Path = typer.Option(
        ..., "--output", "-o", help="Output directory for torrent files"
    ),
    proxy: Optional[str] = typer.Option(
        None, "--proxy", "-p", help="SOCKS5 proxy in format ip:port"
    ),
):
    """Download torrent files from magnet links listed in a text file."""
    if not input_file.exists():
        typer.echo(f"Error: Input file {input_file} does not exist", err=True)
        raise typer.Exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)
    downloader = TorrentDownloader(output_dir, proxy)
    magnet_links = deduplicate_magnet_links(input_file)

    console.print(f"Processing {len(magnet_links)} unique magnet links...")
    asyncio.run(process_magnets(downloader, magnet_links))
    console.print("\nDownload complete!", style="green")


if __name__ == "__main__":
    app()
