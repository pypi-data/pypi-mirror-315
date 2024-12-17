from typing import List, Optional

from yattag import Doc
from math import ceil

from quid.passager.CitationSource import CitationSource
from quid.visualization.Info import Info
import re

from quid.visualization.Markup import Markup
from quid.visualization.MarkupSpan import MarkupSpan
from quid.visualization.TargetHtml import TargetHtml
from quid.visualization.TargetTextWithContent import TargetTextWithContent
from quid.visualization.Visualization import Visualization
import html


# noinspection PyMethodMayBeStatic
class Visualizer:

    def __init__(self, censor: bool = False, keep_range: int = 25):
        self.censor = censor
        self.keep_range = keep_range

    def visualize(self, title, author, year, source_content: str, citation_sources: List[CitationSource],
                  citation_source_links, target_texts_with_content: List[TargetTextWithContent],
                  markups: List[Markup] = None) -> Visualization:

        info = self.__generate_info_json(title, author, year)
        source_html = self.__generate_source_html(source_content, citation_sources, citation_source_links, markups)
        targets_html = self.__generate_target_html(target_texts_with_content)

        return Visualization(info, source_html, targets_html)

    def __generate_info_json(self, title, author, year) -> Info:
        return Info(title, author, year)

    def __calculate_max_target_texts_count(self, citation_source_links) -> int:
        max_citation_sources = 0

        for citation_source_link in citation_source_links:
            max_citation_sources = max(max_citation_sources, len(citation_source_link.target_location_selections))

        return max_citation_sources

    def __calculate_max_segment_frequency(self, citation_sources: List[CitationSource]) -> int:
        max_segment_frequency = 0

        for citation_source in citation_sources:
            for source_segment in citation_source.source_segments:
                max_segment_frequency = max(max_segment_frequency, source_segment.frequency)

        return max_segment_frequency

    def __get_klasses_string(self, markup_spans: List[MarkupSpan], current_markup: Optional[Markup]) -> str:

        klasses = ''
        for ms in markup_spans:
            if klasses:
                klasses += ' '

            if ms.klass == 'scene':
                if ms.used:
                    klasses += 'scene_end'
                else:
                    if current_markup and current_markup.klass == 'scene':
                        klasses += 'scene'
                    else:
                        klasses += 'scene_start'
            else:
                if not ms.used:
                    klasses += f'{ms.klass}'
                else:
                    klasses += f'{ms.klass}_con'

        return klasses

    def __generate_source_html(self, source_content: str, citation_sources: List[CitationSource],
                               citation_source_links, markups: List[Markup]) -> str:

        max_target_texts_count = self.__calculate_max_target_texts_count(citation_source_links)
        max_segment_frequency = self.__calculate_max_segment_frequency(citation_sources)

        doc, tag, text = Doc().tagtext()

        markup_spans = []
        content_spans = []
        content = ''
        citation_source_start_pos = 0
        segments = []

        for char_pos in range(0, len(source_content) + 1):
            if markups:
                for mr in markups:
                    if mr.start == mr.end == char_pos:
                        if content:
                            klasses = self.__get_klasses_string(markup_spans, None)
                            content_spans.append((content, klasses))

                            for ms in markup_spans:
                                ms.used = True

                            content = ''

                        content_spans.append(('', mr.klass))
                    elif mr.start == char_pos:
                        if content:
                            klasses = self.__get_klasses_string(markup_spans, None)
                            content_spans.append((content, klasses))

                            for ms in markup_spans:
                                ms.used = True

                        markup_spans.append(MarkupSpan(mr.klass))
                        content = ''

                    elif mr.end == char_pos:
                        klasses = self.__get_klasses_string(markup_spans, mr)
                        content_spans.append((content, klasses))

                        for ms in markup_spans:
                            ms.used = True
                            if ms.klass == mr.klass:
                                ms.closed = True

                        markup_spans = list(filter(lambda ms: not ms.closed, markup_spans))
                        content = ''

            finished = False
            for citation_source_pos in range(citation_source_start_pos, len(citation_sources)):
                citation_source = citation_sources[citation_source_pos]

                for segment_pos in range(0, len(citation_source.source_segments)):
                    segment = citation_source.source_segments[segment_pos]

                    if char_pos < segment.start:
                        finished = True
                        break

                    if segment.start == char_pos:
                        if content:
                            klasses = ''
                            if len(markup_spans) > 0:
                                klasses = self.__get_klasses_string(markup_spans, None)
                                for ms in markup_spans:
                                    ms.used = True

                            content_spans.append((content, klasses))
                            content = ''

                        citation_source_start_pos = citation_source_pos

                        if segment_pos == 0:
                            if len(content_spans) > 0:
                                spos = 0
                                while spos < len(content_spans):
                                    if content_spans[spos][1] == 'scene_empty':
                                        with tag('span', klass=cs[1]):
                                            doc.asis('')
                                        spos += 1
                                    else:
                                        with tag('span', klass='text_standard'):
                                            sub_cnt = 0
                                            for sub_pos in range(spos, len(content_spans)):
                                                cs = content_spans[sub_pos]
                                                if cs[1] == 'scene_empty':
                                                    break

                                                sub_cnt += 1
                                                if cs[1]:
                                                    with tag('span', klass=cs[1]):
                                                        doc.asis(cs[0])
                                                else:
                                                    doc.asis(cs[0])

                                            spos += sub_cnt

                            segments.clear()
                        else:
                            segments.append(('asis', content_spans.copy()))

                        content_spans.clear()
                        finished = True
                        break
                    elif segment.end == char_pos or (segment_pos == len(citation_source.source_segments) - 1 and
                                                     char_pos == len(source_content) - 1):
                        citation_count = self.__calculate_target_text_count(citation_source, citation_source_links)
                        segment_frequency = segment.frequency
                        citation_count_percentage = \
                            int((ceil((citation_count / max_target_texts_count) * 10.0) / 10.0) * 10)
                        segment_frequency_percentage = \
                            int((ceil((segment_frequency / max_segment_frequency) * 10.0) / 10.0) * 10)
                        klass_background = f'source_segment_background_o{citation_count_percentage}'
                        klass_font = f'source_segment_font_s{segment_frequency_percentage}'
                        klass = f'source_segment {klass_background} {klass_font}'
                        tag_id = f'sourceSegment_{citation_source.my_id}_{segment.my_id}'

                        klasses = ''
                        if len(markup_spans) > 0:
                            klasses = self.__get_klasses_string(markup_spans, None)
                            for ms in markup_spans:
                                ms.used = True

                        content_spans.append((content, klasses))
                        content = ''

                        segments.append(('span', content_spans.copy(), klass, tag_id, segment.token_length))
                        content_spans.clear()
                        finished = True

                        if segment_pos == len(citation_source.source_segments) - 1:
                            citation_source_start_pos += 1
                            with tag('span', klass='citation_source_container', id=str(citation_source.my_id)):
                                for segment in segments:
                                    if segment[0] == 'asis':
                                        if segment[1]:
                                            with tag('span', klass='text_standard'):
                                                for cs in segment[1]:
                                                    if cs[1]:
                                                        with tag('span', klass=cs[1]):
                                                            doc.asis(cs[0])
                                                    else:
                                                        doc.asis(cs[0])
                                    else:
                                        with tag('span', ('data-token-count', segment[4]), klass=segment[2], id=segment[3]):
                                            for cs in segment[1]:
                                                if cs[1]:
                                                    with tag('span', klass=cs[1]):
                                                        doc.asis(cs[0])
                                                else:
                                                    doc.asis(cs[0])
                        break

                if finished:
                    break

            if char_pos < len(source_content):
                if source_content[char_pos] == '\n':
                    content += '<br>'
                else:
                    content += html.escape(source_content[char_pos])

        if len(content_spans) > 0:
            with tag('span', klass='text_standard'):
                for cs in content_spans:
                    if cs[1]:
                        with tag('span', klass=cs[1]):
                            doc.asis(cs[0])
                    else:
                        doc.asis(cs[0])

        return doc.getvalue()

    def __calculate_target_text_count(self, citation_source, citation_source_links):
        for citation_source_link in citation_source_links:
            if citation_source_link.citation_source_id == citation_source.my_id:
                return len(citation_source_link.target_location_selections)

        return None

    def __generate_target_html(self, target_texts_with_content: List[TargetTextWithContent]) -> List[TargetHtml]:

        result: List[TargetHtml] = []

        for target_text_with_content in target_texts_with_content:
            target_text = target_text_with_content.target_text
            target_content = target_text_with_content.content
            doc, tag, text = Doc().tagtext()

            content = ''
            location_start_pos = 0
            for char_pos in range(0, len(target_content)):
                for location_pos in range(location_start_pos, len(target_text.target_locations)):
                    location = target_text.target_locations[location_pos]

                    if char_pos < location.start:
                        break

                    if location.start == char_pos:
                        location_start_pos = location_pos
                        if self.censor:
                            if len(content) < self.keep_range * 2:
                                doc.asis(content)
                            else:
                                start = 0

                                if location_pos > 0:
                                    start = self.keep_range

                                content_replaced = re.sub('[A-Za-z0-9ÄÖÜäüöß]', 'x', content[start:-self.keep_range])
                                doc.asis(content[0:start])
                                with tag('span', klass='censored'):
                                    doc.asis(content_replaced)
                                doc.asis(content[-self.keep_range:])
                        else:
                            doc.asis(content)
                        content = ''
                        break
                    elif location.end == char_pos:
                        with tag('span', klass='target_location', id=str(location.my_id)):
                            doc.asis(content)
                        content = ''
                        break

                if target_content[char_pos] == '\n':
                    content += '<br>'
                else:
                    content += html.escape(target_content[char_pos])

            if len(content) > 0:
                if self.censor:
                    if len(content) < self.keep_range:
                        doc.asis(content)
                    else:
                        doc.asis(content[0:self.keep_range])
                        content = re.sub('[A-Za-z0-9ÄÖÜäüöß]', 'x', content[self.keep_range:])
                        with tag('span', klass='censored'):
                            doc.asis(content)
                else:
                    doc.asis(content)

            result.append(TargetHtml(target_text.filename, doc.getvalue()))

        return result
