# window.py
#
# Copyright 2023 Lorenzo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from time import sleep
import threading
import requests
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Adw, Gtk, GdkPixbuf, GLib  # noqa


class CatgalleryWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'CatgalleryWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_default_size(800,800)

        self.header = Adw.HeaderBar(hexpand=True)
        self.header.set_title_widget(Adw.WindowTitle.new('Cat Gallery', ''))

        self.set_title('Cat Gallery')
        self.set_decorated(True)

        grid = Gtk.Grid(row_spacing=20)
        grid.set_baseline_row(1)

        grid.attach(self.header, 0, 0,   1, 1)

        self.preview_image: Image = Gtk.Image.new_from_resource('/com/example/catgallery/assets/placeholder.png')
        self.preview_image.set_pixel_size(400)

        grid.attach(self.preview_image, 0, 1, 1, 1)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, halign=Gtk.Align.CENTER)

        self.next_button = Gtk.Button(label='Next')
        self.next_button.connect('clicked', self.on_next_button_clicked)

        self.prev_button = Gtk.Button(label='Back')
        self.prev_button.connect('clicked', self.on_prev_button_clicked)

        button_box.append(self.prev_button)
        button_box.append(self.next_button)

        set_wallpaper_button_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, halign=Gtk.Align.CENTER)

        self.set_wallpaper_button = Gtk.Button(css_classes=['suggested-action'])
        self.set_wallpaper_button_spinner = Gtk.Spinner(spinning=True, visible=False)
        self.set_wallpaper_button_label = Gtk.Label(label='Set as wallpaper')
        set_wallpaper_button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        set_wallpaper_button_box.append(self.set_wallpaper_button_spinner)
        set_wallpaper_button_box.append(self.set_wallpaper_button_label)

        self.set_wallpaper_button.set_child(set_wallpaper_button_box)

        set_wallpaper_button_row.append(self.set_wallpaper_button)

        grid.attach(button_box, 0, 2, 1, 1)
        grid.attach(set_wallpaper_button_row, 0, 3, 1, 1)

        counter_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, halign=Gtk.Align.CENTER)
        counter = Gtk.Button(label='0')
        counter.connect('clicked', lambda w: counter.set_label(str(int(counter.get_label()) + 1)))
        counter_row.append(counter)

        grid.attach(counter_row, 0, 4, 1, 1)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_child(grid)
        self.set_content(scrolled_window)

    def on_next_button_clicked(self, widget):
        self.on_image_load_start()

        # self.load_next_image()
        threading.Thread(target=self.load_next_image).start()

    def on_prev_button_clicked(self, widget):
        pass

    def load_next_image(self):
        sleep(3)

        response = requests.get('https://cataas.com/cat', timeout=10)
        response.raise_for_status()

        loader = GdkPixbuf.PixbufLoader()
        loader.write_bytes(GLib.Bytes.new(response.content))
        loader.close()

        # self.preview_image.set_from_pixbuf(loader.get_pixbuf())
        GLib.idle_add(self.on_image_load_end, (loader.get_pixbuf()))

    def on_image_load_start(self):
        self.set_wallpaper_button_spinner.set_visible(True)
        self.set_wallpaper_button_spinner.set_spinning(True)
        self.set_wallpaper_button_label.set_visible(False)

    def on_image_load_end(self, pixbuf):
        self.set_wallpaper_button_spinner.set_visible(False)
        self.set_wallpaper_button_label.set_visible(True)
        self.preview_image.set_from_pixbuf(pixbuf)
