#!/usr/bin/env python2.7
#
# pypopro - A Jitsi-meet audio postprocessing tool
# Copyright (C) 2015  Julien Pivotto
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import os.path
import json

class PostProcessing:
    def __init__(self, metadata_file):
        self.metadata_file = metadata_file

    def sanity_checks(self):
        if not os.path.isfile(self.metadata_file):
            raise Exception('"%s" is not a file' % self.metadata_file)

    def load_file(self):
        with open(self.metadata_file, 'r') as f:
            return json.load(f)

    def get_speaker_list(self, data):
        speaker_list = set()
        for d in data:
            speaker_list.add(d['ssrc'])
        return speaker_list

    def get_first_instant(self, data):
        return data[0]['instant']

    def tmp_filename(self, filename):
        return '%s-padded.wav' % (filename[:-4])

    def final_filename(self, filename):
        return 'final%s.wav' % (filename[:-4])

    def process_speaker(self, speaker, data):
        print '# Speaker %s' % speaker
        chunks = []
        for chunk in [d for d in data if d['ssrc'] == speaker]:
            assert d['type'] == 'RECORDING_STARTED'
            f = chunk['filename']
            if os.path.getsize(f) >= 2048:
                tmp_f = self.tmp_filename(f)
                instant = (chunk['instant'] - self.first_instant)/1000.
                print 'sox %s %s pad %s' % (f, tmp_f, instant)
                chunks.append(tmp_f)
        print 'sox --combine mix-power %s final_%s.wav' % (' '.join(chunks), speaker)
        for chunk in [d for d in data if d['ssrc'] == speaker]:
            f = chunk['filename']
            if os.path.getsize(f) >= 2048:
                tmp_f = self.tmp_filename(f)
                print 'rm %s' % (tmp_f)
                chunks.append(tmp_f)
        print

    def run(self):
        self.sanity_checks()
        file_data = self.load_file()
        data = file_data['audio']
        self.first_instant = self.get_first_instant(data)
        print '#!/bin/bash -x'
        print '# Script generated by pypopro'
        for speaker in self.get_speaker_list(data):
            self.process_speaker(speaker, data)
        print '''
# The files are final_*.wav, one per speaker
'''


if __name__ == '__main__':
    PostProcessing('metadata.json').run()

