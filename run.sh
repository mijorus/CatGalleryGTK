#! /usr/bin/bash
flatpak kill com.example.catgallery
flatpak-builder build/ com.example.catgallery.json --user --force-clean
flatpak-builder --run build/ com.example.catgallery.json catgallery
