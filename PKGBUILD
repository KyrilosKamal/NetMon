# Maintainer: Kyrillos Kamal <kyrillos@example.com>
pkgname=netmon-gui
pkgver=2.0.0
pkgrel=1
pkgdesc="Modern network monitor for Arch Linux with PySide6 GUI"
arch=('any')
url="https://github.com/KyrilosKamal/NetMon"
license=('MIT')
depends=(
    'python>=3.11'
    'pyside6'
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
)
source=(
    "$pkgname-$pkgver.tar.gz::$url/archive/v$pkgver.tar.gz"
    "netmon-gui.desktop"
    "netmon-gui.sh"
)
sha256sums=('922a818cbdd81ab05e20aa90ab62dad7089a301a1db327a146f31a86a4288a10'
            '41b16eeb54510cbaaa0397399cdc607558b9092064122ecedb0bbf9cc9d13709'
            'fe80d4007ef98553bde7a68b3405ff81aa7279aea083f4d8bfd070824b5a2015')

build() {
    cd "$srcdir/$pkgname-$pkgver"
    python -m build --wheel --no-isolation
}

package() {
    cd "$srcdir/$pkgname-$pkgver"
    python -m installer --destdir="$pkgdir" dist/*.whl
    
    install -Dm644 "$srcdir/netmon-gui.desktop" \
        "$pkgdir/usr/share/applications/netmon-gui.desktop"

    install -Dm755 "$srcdir/netmon-gui.sh" \
        "$pkgdir/usr/bin/netmon-gui"
    
    if [ -f LICENSE ]; then
        install -Dm644 LICENSE \
            "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
    fi
}
