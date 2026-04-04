let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-25.11";
  pkgs = import <nixpkgs> { config = {}; overlays = []; };
in
  
  pkgs.mkShell {
	packages = [
      (pkgs.python3.withPackages (python-pkgs: [
		python-pkgs.numpy
		python-pkgs.numba
		python-pkgs.matplotlib
		python-pkgs.pytest
      ]))
	];
  }
