# Copyright 2022 Aleksandar Erkalović, Gwyn Vales
# This program is free software: you can redistribute it and/or modify it under
# the terms of the Affero GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the Affero GNU General Public License for more
# details.
# You should have received a copy of the Affero GNU General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/agpl-3.0.en.html>
#
# 'ebooklib', authored by Aleksandar Erkalović, is licensed under the AGPL, and we
# are linking to it, therefore AGPL applies to this module as well. You may NOT
# distirubte derivatives using this module (i.e. epub.py) without also
# distributing the source code, even over a network, and any modifications to
# either epub.py or ebooklib must be licensed under the AGPL as well.
# non-commerical private use is explicitly permitted.
# WORK IN PROGRESS
from uuid import uuid4

import reCBZ.config as config
from ebooklib import epub
from reCBZ.util import mylog

POP_COVER = True


def single_chapter_epub(name: str, pages: list) -> str:
    book = epub.EpubBook()

    # attempt to distinguish author / title
    if ' - ' in name:
        title, author = name.split(' - ', 1)
    else:
        title = name
        author = 'reCBZ'
    book.set_title(title)
    book.add_author(author)
    book.set_language('en')
    book.set_identifier(str(uuid4()))

    # repacking the same file many times over would lead to additional copies
    # if we did include it
    if POP_COVER:
        cover = pages.pop(0)
    else:
        cover = pages[0]
    covert_ops = f'cover{cover.fmt.ext[0]}'
    with open(cover.fp, 'rb') as cover_file:
        book.set_cover(covert_ops, cover_file.read())

    spine = []
    for page_i, page in enumerate(pages, start=1):
        static_dest = f'static/{page_i}{page.fmt.ext[0]}'
        mime_type = page.fmt.mime
        if config.ebook_profile is not None:
            if page.landscape:
                height, width = config.ebook_profile.size
            else:
                width, height = config.ebook_profile.size
        else:
            width, height = page.size
        size_str = f'width={width} height={height}'
        mylog(f'writing {page.fp} to {static_dest} as {mime_type}')

        item = epub.EpubHtml(title=f'Page {page_i}',
                             file_name=f'page_{page_i}.xhtml', lang='en')
        item.content = f'''<html>
                            <head></head>
                            <body>
                                <img src="{static_dest}" {size_str}'/>
                            </body>
                         </html>'''

        with open(page.fp, 'rb') as image_file:
            image_content = image_file.read()
        # store read content relative to zip
        static_img = epub.EpubImage(uid=f'image_{page_i}', file_name=static_dest,
                                    media_type=mime_type, content=image_content)
        book.add_item(item)
        book.add_item(static_img)
        spine.append(item)
    book.toc.append(spine[0])

    # add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = (page for page in spine)

    if config.right_to_left is True:
        book.set_direction('rtl')

    if config.ebook_profile is not None:
        for tag in config.ebook_profile.epub_properties:
            book.add_metadata(*tag)
        source_fp = f'{name}{config.ebook_profile.epub_ext}'
    else:
        source_fp = f'{name}.epub'

    epub.write_epub(source_fp, book, {})
    return source_fp