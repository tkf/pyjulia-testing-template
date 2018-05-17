# Initialize $JULIA_PKGDIR, in case this is the first time the test is run:
Pkg.init()

# Update all installed packages to reflect upstream changes:
Pkg.update()

# Install dependencies:
info("Pkg.add(PyCall)")
Pkg.add("PyCall")

# Show Julia information in verbose mode:
versioninfo(true)
