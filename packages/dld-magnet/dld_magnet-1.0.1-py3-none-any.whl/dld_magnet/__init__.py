import typer
import time
import subprocess
import shutil
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import qbittorrentapi

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
            console.print(
                "Failed to login to qBittorrent. Check your credentials.", style="red"
            )
            raise typer.Exit(1)
        except qbittorrentapi.APIConnectionError:
            console.print(
                "Cannot connect to qBittorrent. Make sure it's running and Web UI is enabled.",
                style="red",
            )
            raise typer.Exit(1)

    def _ensure_qbittorrent_running(self):
        """Ensure qBittorrent is running, start it if it's not."""
        # Check if qbittorrent is in PATH
        qbittorrent_path = shutil.which("qbittorrent")
        if not qbittorrent_path:
            console.print("qBittorrent is not installed or not in PATH", style="red")
            raise typer.Exit(1)

        # Check if qbittorrent is running
        try:
            if (
                subprocess.run(["pgrep", "qbittorrent"], capture_output=True).returncode
                != 0
            ):
                console.print("Starting qBittorrent...", style="yellow")
                # Start qbittorrent in background
                subprocess.Popen(
                    [qbittorrent_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                # Wait for it to start
                time.sleep(5)  # Give it some time to initialize
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

    def download_from_magnet(self, magnet_link: str) -> None:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task(description="Adding magnet link...", total=None)

            try:
                # Add the torrent and get its hash
                result = self.qbt_client.torrents_add(urls=[magnet_link])
                if not result == "Ok.":
                    raise Exception("Failed to add magnet link")

                progress.update(task, description="Waiting for metadata...")

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

                            # Remove the torrent from qBittorrent (but keep the .torrent file)
                            self.qbt_client.torrents_delete(
                                delete_files=False, torrent_hashes=[torrent.hash]
                            )

                            progress.update(
                                task, description=f"Saved torrent file to {file_path}"
                            )
                            return

                    time.sleep(1)
                    attempts += 1

                raise Exception("Timeout waiting for metadata")

            except Exception as e:
                raise Exception(f"Failed to process magnet link: {str(e)}")


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
    """
    Download torrent files from magnet links listed in a text file.
    """
    # Validate input file
    if not input_file.exists():
        typer.echo(f"Error: Input file {input_file} does not exist", err=True)
        raise typer.Exit(1)

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize downloader
    downloader = TorrentDownloader(output_dir, proxy)

    # Read and process magnet links
    with open(input_file, "r") as f:
        magnet_links = [line.strip() for line in f if line.strip()]

    with console.status(f"Found {len(magnet_links)} magnet links to process..."):
        for i, magnet in enumerate(magnet_links, 1):
            console.print(f"Processing magnet link {i}/{len(magnet_links)}")
            try:
                downloader.download_from_magnet(magnet)
            except Exception as e:
                console.print(
                    f"Error processing magnet link {i}: {str(e)}", style="red"
                )

    console.print("Download complete!", style="green")


if __name__ == "__main__":
    app()
