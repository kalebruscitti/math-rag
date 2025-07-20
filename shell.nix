{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {

  # py3 is a reference to the current version of python
  packages = [
    (pkgs.python3.withPackages(py3: with py3; [
      # put nix-managed packages here
    ]))
  ];

  env.LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath[
    pkgs.stdenv.cc.cc.lib
    pkgs.libz
  ];

  shellHook = ''
    zsh
  '';
}


