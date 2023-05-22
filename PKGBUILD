# This is an example PKGBUILD file. Use this as a start to creating your own,
# and remove these comments. For more information, see 'man PKGBUILD'.
# NOTE: Please fill out the license field for your package! If it is unknown,
# then please put 'unknown'.

# Maintainer: Julien Adlon <julien.aldon@epitech.eu>
pkgname=eeplanner-git
pkgver=151.b1be485
pkgrel=1
epoch=
pkgdesc="Epitech Event planner tool"
arch=('x86_64')
url="https://github.com/JulienAldon/EEPlanner"
license=('GPL')
groups=()
depends=('python3')
makedepends=()
checkdepends=()
optdepends=()
provides=()
conflicts=()
replaces=()
backup=()
options=()
install=
changelog=
source=()
noextract=()
md5sums=()
validpgpkeys=()

pkgver()
{
  cd "$_pkgname"
  echo $(git rev-list --count HEAD).$(git rev-parse --short HEAD)
}

package() {
        pip install .. --root="$pkgdir"
}
