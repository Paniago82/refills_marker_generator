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
import math
import os

from refills_marker_generator.chilitag_generator import ChilitagGenerator
from refills_marker_generator.paths import path_batch_svg, output_dir, path_batch_template, name_tag_png, path_tag_png, \
    path_batch_pdf


class BatchPageGenerator(object):
    def __init__(self, first_tag_id, last_tag_id, mode):
        self.first_tag_id = first_tag_id
        self.last_tag_id = last_tag_id
        self.mode = mode
        self.tags_per_page = 9

    def run(self):
        for page_id in range(0, self.num_of_pages()):
            print "Generating batch page #{} at {}".format(page_id+1, output_dir())
            self.gen_tags_for_page(page_id)
            self.gen_batch_page(page_id)

    def gen_tags_for_page(self, page_id):
        for marker_offset in range(0, self.tags_per_page):
            current_tag_id = self.calc_tag_id(page_id, marker_offset)
            if  current_tag_id <= self.last_tag_id:
                if self.mode == 0:
                    tag_generator = ChilitagGenerator(current_tag_id,0)
                    tag_generator.run()
                else:
                    tag_generator = ChilitagGenerator(current_tag_id,1)
                    tag_generator.run()

    def load_svg_template(self):
        with open(path_batch_template(), 'r') as f:
            return f.read()

    def write_output_svg(self, output_svg, page_id):
        with open(path_batch_svg(page_id), 'w') as f:
            f.write(output_svg)

    def get_replacements(self, page_id):
        replacements = {}
        for marker_offset in range(0, self.tags_per_page):
            current_tag_id = self.calc_tag_id(page_id, marker_offset)
            if  current_tag_id <= self.last_tag_id:
                replacements['REL-MARKER-PNG{}'.format(marker_offset+1)] = name_tag_png(current_tag_id)
                replacements['ABS-MARKER-PNG{}'.format(marker_offset+1)] = path_tag_png(current_tag_id)
        return replacements

    def replace_svg_placeholders(self, svg_template, replacements):
        """

        :param svg_template:
        :param replacements:
        :type replacements: dict
        :return:
        """
        output_svg = svg_template
        for old, new in replacements.iteritems():
            output_svg = output_svg.replace(old, new)
        return output_svg

    def gen_batch_page(self, page_id):
        output_svg = self.replace_svg_placeholders(self.load_svg_template(), self.get_replacements(page_id))
        self.write_output_svg(output_svg, page_id)
        self.call_inkscape(path_batch_pdf(page_id), path_batch_svg(page_id))
        self.clean_up(page_id)

    def call_inkscape(self, path_pdf, path_svg):
        arguments = "inkscape -A {} -f {} -d 600".format(path_pdf, path_svg).split()
        # About calling executable:
        # https://stackoverflow.com/questions/2473655/how-to-make-a-call-to-an-executable-from-python-script
        popen = subprocess.Popen(arguments, stdout=subprocess.PIPE)
        popen.wait()

    def clean_up(self, page_id):
        print "Cleaning up..."
        os.remove(path_batch_svg(page_id))
        for marker_offset in range(0, self.tags_per_page):
            current_tag_id = self.calc_tag_id(page_id, marker_offset)
            if current_tag_id <= self.last_tag_id:
                os.remove(path_tag_png(current_tag_id))
        print "done."

    def num_of_pages(self):
        return int(math.ceil(self.num_tags() / float(self.tags_per_page)))

    def num_tags(self):
        return self.last_tag_id - self.first_tag_id + 1

    def calc_tag_id(self, page_id, tag_offset):
        return self.tags_per_page*page_id + tag_offset + self.first_tag_id
