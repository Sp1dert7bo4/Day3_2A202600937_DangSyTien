# -*- coding: utf-8 -*-
"""
OPTC Strategy System — Visual Demo Launcher
Opens the interactive web dashboard (src/demo.html) in the default web browser.
"""
import os
import sys
import webbrowser

# Get absolute path to demo.html
current_dir = os.path.dirname(os.path.abspath(__file__))
demo_path = os.path.join(current_dir, "demo.html")

print("=" * 60)
print("🏴‍☠️ OPTC Strategy System — LAUNCHING VISUAL DEMO")
print("=" * 60)
print(f"📁 Opening dashboard: {demo_path}")
print("🌐 Opening your default web browser...")
print("=" * 60)

# Open HTML file in browser
webbrowser.open(f"file:///{demo_path}")

print("✅ Success! Dashboard opened in your browser.")
print("=" * 60)
