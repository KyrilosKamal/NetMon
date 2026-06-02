# Maintainer: Your Name <you@example.com>
pkgname=netmon
pkgver=2.0.0
pkgrel=1
pkgdesc="Modern PySide6 network monitor: speed test, bandwidth, connections, and open ports for Arch Linux"
arch=('x86_64' 'aarch64' 'i686')
url="https://github.com/YOUR_USERNAME/netmon"
license=('MIT')
depends=(
    'python'
    'python-pyside6'
    'python-psutil'
    'python-speedtest-cli'
    'python-pyqtgraph'
    'python-pyside6-fluent-widgets'
    'qt6-wayland'
    'hicolor-icon-theme'
)
makedepends=(
    'python-build'
    'python-installer'
    'python-setuptools'
    'python-wheel'
    'git'
)
optdepends=(
    'sudo: To view all system connections (required for full functionality)'
)
provides=(${pkgname})
conflicts=(${pkgname})
source=("netmon-$pkgver.tar.gz::$url/archive/v$pkgver.tar.gz"
        "netmon.desktop")
sha256sums=('SKIP'
            'SKIP')

build() {
    cd "$srcdir/$pkgname-$pkgver"
    python -m build --wheel --no-isolation --outdir="$srcdir/dist"
}

package() {
    cd "$srcdir/$pkgname-$pkgver"
    python -m installer --destdir="$pkgdir" --compile-bytecode=1 "$srcdir/dist"/*.whl

    install -Dm644 "netmon.desktop" "$pkgdir/usr/share/applications/netmon.desktop"
    
    install -Dm644 "src/netmon/resources/netmon.svg" "$pkgdir/usr/share/icons/hicolor/scalable/apps/netmon.svg"

    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"

    find "$pkgdir" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
}
