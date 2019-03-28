
import os
import rospkg


# GENERIC PATHS

def output_dir():
    return os.getcwd()


def output_path(filename):
    return '{}/{}'.format(output_dir(), filename)


def templates_dir():
    return '{}/templates'.format(rospkg.RosPack().get_path("refills_marker_generator"))


def templates_path(filename):
    return '{}/{}'.format(templates_dir(), filename)


# PATHS RELATED TO TAGS

def name_tag_svg(tag_id):
    return '{}.svg'.format(tag_id)


def path_tag_svg(tag_id):
    return output_path(name_tag_svg(tag_id))


def name_tag_png(tag_id):
    return '{}.png'.format(name_tag_svg(tag_id))


def path_tag_png(tag_id):
    return output_path(name_tag_png(tag_id))


# PATHS RELATED TO BATCH PAGES

def name_batch_svg(page_id):
    return 'batch_{}.svg'.format(page_id)


def name_batch_pdf(page_id):
    return '{}.pdf'.format(name_batch_svg(page_id))


def path_batch_svg(page_id):
    return output_path(name_batch_svg(page_id))


def path_batch_pdf(page_id):
    return output_path(name_batch_pdf(page_id))


def path_batch_template():
    return templates_path('batch.svg')

