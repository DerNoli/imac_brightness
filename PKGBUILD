pkgname=autobrightness
pkgver=1.0
pkgrel=1
pkgdesc="Automatic screen brightness adjustment using ambient light sensor"
arch=('any')
license=('MIT')
depends=(
    'python'
    'python-dbus'
    'dbus'
    'systemd'
    'iio-sensor-proxy'
)
source=(
    'autobrightness.py'
    'autobrightness.service'
    'autobrightness.conf'
    '90-backlight.rules'
    'autobrightness.install'
)
sha256sums=('SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP')

prepare() {
    # Ensure Arch-compliant Python shebang
    sed -i 's|#!/usr/bin/env python3|#!/usr/bin/python|' "$srcdir/autobrightness.py"
}

package() {
    install -Dm755 "$srcdir/autobrightness.py" "$pkgdir/usr/bin/autobrightness"
    install -Dm644 "$srcdir/autobrightness.service" "$pkgdir/usr/lib/systemd/system/autobrightness.service"
    install -Dm644 "$srcdir/autobrightness.conf" "$pkgdir/etc/autobrightness.conf"
    install -Dm644 "$srcdir/90-backlight.rules" "$pkgdir/etc/udev/rules.d/90-backlight.rules"
}
