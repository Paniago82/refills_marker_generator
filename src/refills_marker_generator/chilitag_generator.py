#  Copyright (C) 2018-2019, Georg Bartels <georg.bartels@cs.uni-bremen.de>.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import subprocess
import rospkg
import os


class ChilitagGenerator(object):
    def __init__(self, num):
        self.num = num

        # setting up some path names
        r = rospkg.RosPack()
        self.pkg_dir = r.get_path("refills_marker_generator")
        self.current_dir = os.getcwd() +"/"
        self.templates_path = self.pkg_dir + '/templates/'

        # where is the SVG template?
        self.name_svg_template = 'left.svg' if self.is_left() else 'right.svg'
        self.path_svg_template = self.templates_path + self.name_svg_template

        # where is should the chilitag PNG be?
        self.name_chilitag_png = '{}.png'.format(self.num)
        self.path_chilitag_png = self.current_dir + self.name_chilitag_png

        # where should the output SVG go?
        self.name_output_svg = '{}.svg'.format(self.num)
        self.path_output_svg = self.current_dir + self.name_output_svg

        # where should the final PNG go?
        self.name_final_png = self.name_output_svg + ".png"
        self.path_final_png = self.current_dir + self.name_final_png

    def run(self):
        print "Generating Chilitag #{} at {}".format(self.num, os.getcwd())
        self.generate_chiltag_png()
        self.write_output_svg(self.replace_svg_placeholders(self.load_svg_template()))
        self.call_inkscape()
        self.clean_up()

    def generate_chiltag_png(self):
        arguments = "{}/../../devel/bin/chilitags-creator {} 111 n".format(self.pkg_dir, self.num)
        # About the params:
        # '111' scales the Marker up to 1110x1110 pixels, and 'n' removes any white margin
        # About calling executable:
        # https://stackoverflow.com/questions/2473655/how-to-make-a-call-to-an-executable-from-python-script
        popen = subprocess.Popen(arguments.split(), stdout=subprocess.PIPE)
        popen.wait()
        # output = popen.stdout.read()

    def load_svg_template(self):
        with open(self.path_svg_template, 'r') as f:
            return f.read()

    def replace_svg_placeholders(self, svg_template):
        output_svg = svg_template.replace('NUM', '{}'.format(self.num))
        output_svg = output_svg.replace('RELATIVE-CHILITAGS-PNG', self.name_chilitag_png)
        return output_svg.replace('ABSOLUTE-CHILITAGS-PNG', self.path_chilitag_png)

    def write_output_svg(self, output_svg):
        with open(self.path_output_svg, 'w') as f:
            f.write(output_svg)

    def call_inkscape(self):
        arguments = "inkscape -e {} {} -d 600".format(self.path_final_png, self.path_output_svg).split()
        # About calling executable:
        # https://stackoverflow.com/questions/2473655/how-to-make-a-call-to-an-executable-from-python-script
        popen = subprocess.Popen(arguments, stdout=subprocess.PIPE)
        popen.wait()

    def clean_up(self):
        os.remove(self.path_output_svg)
        os.remove(self.path_chilitag_png)

    def side(self):
        if self.num % 2 == 0:
            return 'right'
        else:
            return 'left'

    def is_left(self):
        return self.side() == 'left'

    def is_right(self):
        return self.side() == 'right'
