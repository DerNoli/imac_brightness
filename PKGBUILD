pkgname=autobrightness
pkgver=1.0
pkgrel=1
pkgdesc="Automatic screen brightness adjustment using ambient light sensor"
arch=('any')
license=('MIT')
depends=(
    'python'
    'python-dbus'
    'brightnessctl'
    'dbus'
    'systemd'
    'iio-sensor-proxy'
)
source=(
    'autobrightness.py'
    'autobrightness.service'
    'autobrightness.conf'
    '90-backlight.rules'
)
sha256sums=('SKIP' 'SKIP' 'SKIP' 'SKIP')

package() {
    install -Dm755 "$srcdir/autobrightness.py" "$pkgdir/usr/bin/autobrightness"
    install -Dm644 "$srcdir/autobrightness.service" "$pkgdir/usr/lib/systemd/system/autobrightness.service"
    install -Dm644 "$srcdir/autobrightness.conf" "$pkgdir/etc/autobrightness.conf"
    install -Dm644 "$srcdir/90-backlight.rules" "$pkgdir/etc/udev/rules.d/90-backlight.rules"
}

post_install() {
    echo "Reloading udev rules..."
    udevadm control --reload-rules
    udevadm trigger

    echo "Enabling autobrightness.service..."
    systemctl enable --now autobrightness.service >/dev/null 2>&1 || true
}

post_upgrade() {
    systemctl restart autobrightness.service >/dev/null 2>&1 || true
}

post_remove() {
    systemctl disable --now autobrightness.service >/dev/null 2>&1 || true
}
