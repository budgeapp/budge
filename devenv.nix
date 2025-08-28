{ pkgs, ... }:
{
  packages = with pkgs; [
    git
  ];

  languages.python = {
    enable = true;
    uv.enable = true;
    uv.sync.enable = true;
    venv.enable = true;
  };
}
